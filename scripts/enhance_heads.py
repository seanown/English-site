#!/usr/bin/env python3
"""Site-wide <head> enhancement for all *.html.

Idempotent: safe to re-run. Handles:
  #2 preconnect (googleapis + gstatic) -> inserted before Google Fonts <link>
  #3 og:image / twitter:image           -> replaced with per-page branded OG
  #5 Person + Organization JSON-LD     -> added to index.html only
  #6 hreflang en / zh-Hant / x-default -> inserted after <link rel=canonical>
  #8 Plausible (no-cookie analytics)   -> inserted before </head>
  #A  components.css link              -> inserted after Google Fonts <link>
"""
import re, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = {p.stem: p.stem for p in ROOT.glob("*.html")}
SLUG["404"] = "index"   # 404 fallback uses index OG

def og_url(stem):
    return f"https://ownsean.com/img/og/{SLUG[stem]}.jpg"

PLAUSIBLE = '<script defer data-domain="ownsean.com" src="https://plausible.io/js/script.js"></script>'
COMPONENTS = '<link rel="stylesheet" href="css/components.css">'

PRECONNECT_GAPI = '<link rel="preconnect" href="https://fonts.googleapis.com">'
PRECONNECT_GSTA = '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'

JSON_LD_INDEX = (
    '<script type="application/ld+json">\n'
    + json.dumps({
        "@context":"https://schema.org",
        "@graph":[
            {
                "@type":"Person","@id":"https://ownsean.com/#sean",
                "name":"Sean Own",
                "alternateName":"OWN ZHEN XUAN",
                "jobTitle":"President, Greater Bay Area Electronic Commerce Association",
                "url":"https://ownsean.com/",
                "worksFor":{"@id":"https://ownsean.com/#gbaeca"},
                "knowsAbout":["Cross-border e-commerce","Cultural IP","Greater Bay Area","AI","Silk culture"]
            },
            {
                "@type":"Organization","@id":"https://ownsean.com/#gbaeca",
                "name":"Greater Bay Area Electronic Commerce Association",
                "url":"https://ownsean.com/gba-leadership.html",
                "member":{"@id":"https://ownsean.com/#sean"},
                "areaServed":"Greater Bay Area"
            }
        ]
    }, indent=2)
    + '\n</script>'
)

def add_preconnects(html):
    pat = re.compile(r'(<link[^>]+href="https://fonts\.googleapis\.com/css2[^"]*"[^>]*rel="stylesheet"[^>]*>)')
    m = pat.search(html)
    if not m:
        return html, False
    fonts_link = m.group(1)
    insertion = ""
    if 'rel="preconnect"' not in html[:m.start()] or 'fonts.googleapis.com' not in html[:m.start()]:
        # crude check: ensure both preconnect lines not already before fonts link
        prefix = html[:m.start()]
        if 'fonts.googleapis.com' not in prefix:
            insertion += PRECONNECT_GAPI + "\n"
        if 'fonts.gstatic.com' not in prefix:
            insertion += PRECONNECT_GSTA + "\n"
    if insertion:
        return html.replace(fonts_link, insertion + fonts_link, 1), True
    return html, False

def add_components(html):
    if 'href="css/components.css"' in html:
        return html, False
    pat = re.compile(r'(<link[^>]+href="https://fonts\.googleapis\.com/css2[^"]*"[^>]*rel="stylesheet"[^>]*>)')
    m = pat.search(html)
    if not m:
        return html, False
    return html.replace(m.group(1), m.group(1) + "\n" + COMPONENTS, 1), True

def add_hreflang(html, stem):
    if 'rel="alternate"' in html and 'hreflang' in html:
        return html, False
    url_self = f"https://ownsean.com/{stem}.html" if stem != "index" else "https://ownsean.com/"
    block = (
        f'<link rel="alternate" hreflang="en" href="{url_self}">\n'
        '<link rel="alternate" hreflang="zh-Hant" href="https://seanown.org/">\n'
        '<link rel="alternate" hreflang="x-default" href="https://ownsean.com/">'
    )
    pat = re.compile(r'(<link rel="canonical"[^>]+>)')
    m = pat.search(html)
    if not m:
        return html, False
    return html.replace(m.group(1), m.group(1) + "\n" + block, 1), True

def add_plausible(html):
    if 'plausible.io/js/script.js' in html:
        return html, False
    return html.replace("</head>", PLAUSIBLE + "\n</head>", 1), True

def set_og(html, stem):
    url = og_url(stem)
    changed = False
    # og:image
    pat = re.compile(r'(<meta\s+property="og:image"\s+content=")[^"]*(")')
    new, n = pat.subn(lambda m: m.group(1) + url + m.group(2), html)
    if n: changed = True; html = new
    # twitter:image
    pat = re.compile(r'(<meta\s+name="twitter:image"\s+content=")[^"]*(")')
    new, n = pat.subn(lambda m: m.group(1) + url + m.group(2), html)
    if n: changed = True; html = new
    return html, changed

def add_jsonld_index(html):
    if '"@context":"https://schema.org"' in html or 'application/ld+json' in html:
        return html, False
    return html.replace("</head>", JSON_LD_INDEX + "\n</head>", 1), True

def process(path):
    txt = path.read_text(encoding="utf-8")
    orig = txt
    stem = path.stem
    actions = []
    txt, ok = add_preconnects(txt); actions.append(("preconnect", ok))
    txt, ok = add_components(txt);   actions.append(("components.css", ok))
    txt, ok = add_hreflang(txt, stem); actions.append(("hreflang", ok))
    txt, ok = set_og(txt, stem);     actions.append(("og:image", ok))
    txt, ok = add_plausible(txt);    actions.append(("plausible", ok))
    if stem == "index":
        txt, ok = add_jsonld_index(txt); actions.append(("jsonld", ok))
    if txt != orig:
        path.write_text(txt, encoding="utf-8")
    parts = []
    for name, result in actions:
        parts.append(f"{name}={'Y' if result else 'skip'}")
    print(f"  {path.name}: " + ", ".join(parts))
    return txt != orig

def main():
    changed = 0
    for p in sorted(ROOT.glob("*.html")):
        if process(p):
            changed += 1
    print(f"[done] {changed} files updated")

if __name__ == "__main__":
    main()