#!/usr/bin/env python3
"""make_event.py — 一鍵生成符合英文站鐵規的活動報導頁 + 注入 news 卡。

用法:
    python scripts/make_event.py --spec scripts/sample-event.json

spec (JSON) 欄位:
    slug         活動 slug（決定 SLUG.html 與 img/og/SLUG.jpg）
    title        頁面標題（英文）
    kicker       hero 上方小標（英文，例: Event / Forum）
    summary      一句英文摘要（meta + news 卡共用）
    date_blur    模糊日期（例: "Aug 2026" / "2026"）
    venue_name   場地名（英文）
    venue_addr   場地地址（英文）
    stats        [{num, label}, ...]  數字卡
    gallery      ["img/SLUG-g01.webp", ...]  活動照牆（grid 直排）
    sources      [{name, url}, ...]    真實媒體連結（沒有就給空陣列）
    cover        news 卡封面圖路徑
    news_blurb  news 卡一句摘要（英文）

鐵規: 全英文前台、零 JS、藍金 Gary 風、照片無 caption、列表 grid 直排。
產出後請再跑 `python scripts/enhance_heads.py` 確保 head 標記一致，並手動加 sitemap.xml。
"""
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 內聯樣式（與 about.html 一致；確保新頁視覺統一、自包含、零外部依賴）
STYLE = """
  :root{
    --color-primary:#003262; --color-primary-hover:#001B3A; --color-accent:#FDB515;
    --color-accent-hover:#FC9313; --color-blue-dark:#010133; --color-blue-medium:#004AAE;
    --color-gold-dark:#C4820E; --color-founders:#3B7EA1; --color-white:#FFFFFF;
    --color-surface-alt:#F4F4F4; --color-gray-mid:#9A9A9A; --color-gray-deep:#2B2B2B;
    --color-border:#E0E0E0; --color-ink:#0A0A0A;
    --shadow-color-sm:rgba(1,27,58,0.08); --shadow-color-md:rgba(1,27,58,0.12); --shadow-color-lg:rgba(1,27,58,0.18);
    --font-display:"Bebas Neue","Arial Narrow",Impact,sans-serif; --font-body:"Inter","Helvetica Neue",Arial,sans-serif;
    --font-alt:"Open Sans","Helvetica Neue",Arial,sans-serif; --font-condensed:"Oswald","Arial Narrow",sans-serif;
    --space-1:8px;--space-2:16px;--space-3:24px;--space-4:32px;--space-5:48px;--space-6:64px;--space-7:96px;--space-8:128px;
    --container:1200px;
  }
  *{margin:0;padding:0;box-sizing:border-box;}
  html{scroll-behavior:smooth;}
  body{font-family:var(--font-body);color:var(--color-primary);background:var(--color-white);line-height:1.6;-webkit-font-smoothing:antialiased;}
  .container{max-width:var(--container);margin:0 auto;padding:0 var(--space-3);}
  .display{font-family:var(--font-display);text-transform:uppercase;line-height:0.92;letter-spacing:0.01em;font-weight:400;}
  a{text-decoration:none;}
  .nav{background:var(--color-primary);color:var(--color-white);position:sticky;top:0;z-index:100;}
  .nav-inner{display:flex;align-items:center;justify-content:space-between;height:64px;}
  .logo{font-family:var(--font-display);font-size:30px;color:var(--color-white);letter-spacing:0.04em;}
  .logo span{color:var(--color-accent);}
  .nav-links{display:flex;align-items:center;gap:var(--space-3);}
  .nav-links a{color:var(--color-white);font-weight:700;text-transform:uppercase;letter-spacing:0.04em;font-size:13px;transition:color .15s;}
  .nav-links a:hover{color:var(--color-accent);}
  .nav-links a.active{color:var(--color-accent);}
  .nav-toggle{display:none;} .nav-burger{display:none;}
  .btn{display:inline-block;padding:14px 28px;font-family:var(--font-body);font-weight:800;font-size:15px;text-transform:uppercase;letter-spacing:0.04em;border:2px solid transparent;cursor:pointer;border-radius:0;transition:background-color .15s,color .15s,border-color .15s;}
  .btn-accent{background:var(--color-accent);color:var(--color-primary);border-color:var(--color-accent);}
  .btn-accent:hover{background:var(--color-accent-hover);border-color:var(--color-accent-hover);color:var(--color-blue-dark);}
  .btn-primary{background:var(--color-primary);color:var(--color-white);border-color:var(--color-primary);}
  .btn-primary:hover{background:var(--color-primary-hover);border-color:var(--color-primary-hover);}
  .hero{background:var(--color-primary);color:var(--color-white);padding:var(--space-8) 0;}
  .eyebrow{font-family:var(--font-condensed);font-weight:600;text-transform:uppercase;letter-spacing:0.18em;color:var(--color-accent);font-size:14px;margin-bottom:var(--space-2);}
  .hero h1{font-size:clamp(56px,9vw,120px);margin-bottom:var(--space-3);}
  .hero .gold-line{color:var(--color-accent);font-family:var(--font-condensed);font-weight:600;text-transform:uppercase;letter-spacing:0.04em;font-size:clamp(16px,2vw,22px);max-width:680px;margin-bottom:var(--space-5);}
  .section{padding:var(--space-7) 0;}
  .section.alt{background:var(--color-surface-alt);}
  .section-head{margin-bottom:var(--space-5);}
  .section-head .kicker{font-family:var(--font-condensed);font-weight:600;text-transform:uppercase;letter-spacing:0.18em;color:var(--color-accent);font-size:13px;}
  .section-head h2{font-family:var(--font-display);font-size:clamp(40px,6vw,72px);text-transform:uppercase;line-height:0.95;margin-top:var(--space-1);}
  .lead{max-width:820px;font-size:18px;color:var(--color-gray-deep);}
  .lead p{margin-bottom:var(--space-3);}
  .stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--space-3);margin:32px 0;}
  .stat-card{background:var(--color-primary);color:var(--color-white);padding:var(--space-4);text-align:center;}
  .stat-num{font-family:var(--font-display);font-size:64px;color:var(--color-accent);line-height:1;}
  .stat-label{font-family:var(--font-condensed);font-weight:600;text-transform:uppercase;letter-spacing:0.06em;font-size:13px;margin-top:var(--space-1);}
  .gallery{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:32px 0;}
  .gallery > img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;border:1px solid var(--color-border);}
  figure.venue{margin:24px 0;}
  figure.venue img{width:100%;display:block;border:1px solid var(--color-border);}
  .source-link{margin:32px 0;font-family:var(--font-condensed);font-weight:600;text-transform:uppercase;letter-spacing:0.04em;font-size:13px;}
  .source-link a{color:var(--color-gold-dark);margin-left:6px;}
  .source-link a:hover{color:var(--color-primary);}
  .cta{background:var(--color-accent);color:var(--color-primary);padding:var(--space-8) 0;text-align:center;}
  .cta blockquote{font-family:var(--font-display);font-size:clamp(40px,7vw,96px);text-transform:uppercase;line-height:0.92;max-width:900px;margin:0 auto var(--space-5);}
  .cta .btn-primary{background:var(--color-primary);color:var(--color-white);border-color:var(--color-primary);}
  .cta .btn-primary:hover{background:var(--color-blue-dark);border-color:var(--color-blue-dark);}
  .footer{background:var(--color-primary);color:var(--color-white);padding:var(--space-7) 0 var(--space-4);}
  .footer-grid{display:grid;grid-template-columns:1.2fr 1fr 1.4fr;gap:var(--space-5);}
  .footer h4{font-family:var(--font-condensed);font-weight:700;text-transform:uppercase;letter-spacing:0.1em;font-size:15px;color:var(--color-accent);margin-bottom:var(--space-3);}
  .footer p,.footer li{color:#cfd9e6;font-size:14px;line-height:1.9;list-style:none;}
  .footer a{color:#cfd9e6;} .footer a:hover{color:var(--color-accent);}
  .copyright{border-top:1px solid rgba(255,255,255,0.15);margin-top:var(--space-6);padding-top:var(--space-3);font-size:12px;letter-spacing:0.1em;text-transform:uppercase;color:#9fb3c8;}
  @media(max-width:900px){.stat-grid{grid-template-columns:repeat(2,1fr);}.footer-grid{grid-template-columns:1fr 1fr;}.gallery{grid-template-columns:repeat(2,1fr);}}
  @media(max-width:560px){.nav-toggle{position:absolute;opacity:0;width:1px;height:1px;}.nav-burger{display:flex;flex-direction:column;justify-content:center;gap:5px;width:30px;height:30px;cursor:pointer;margin-left:auto;}.nav-burger span{display:block;height:3px;width:100%;background:var(--color-white);transition:background .15s;}.nav-burger:hover span{background:var(--color-accent);}.nav-links{display:none;position:absolute;top:64px;left:0;right:0;flex-direction:column;background:var(--color-primary);padding:var(--space-2) var(--space-3);gap:0;box-shadow:0 8px 24px var(--shadow-color-lg);}.nav-links a{padding:14px 0;border-bottom:1px solid rgba(255,255,255,.15);font-size:15px;}.nav-links a.btn{margin-top:var(--space-2);text-align:center;border-bottom:none;}.nav-toggle:checked ~ .nav-links{display:flex;}.stat-grid{grid-template-columns:1fr;}.footer-grid{grid-template-columns:1fr;}.gallery{grid-template-columns:1fr;}}
"""

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Sean Own</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;500;700;800&family=Open+Sans:wght@400;600;700&family=Oswald:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/components.css">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta name="description" content="{summary}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Sean Own">
<meta property="og:title" content="{title} — Sean Own">
<meta property="og:description" content="{summary}">
<meta property="og:image" content="https://ownsean.com/img/og/{slug}.jpg">
<meta property="og:url" content="https://ownsean.com/{slug}.html">
<link rel="canonical" href="https://ownsean.com/{slug}.html">
<link rel="alternate" hreflang="en" href="https://ownsean.com/{slug}.html">
<link rel="alternate" hreflang="zh-Hant" href="https://seanown.org/">
<link rel="alternate" hreflang="x-default" href="https://ownsean.com/">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} — Sean Own">
<meta name="twitter:description" content="{summary}">
<meta name="twitter:image" content="https://ownsean.com/img/og/{slug}.jpg">
<script defer data-domain="ownsean.com" src="https://plausible.io/js/script.js"></script>
<style>{style}</style>
</head>
<body>
"""

NAV = """<nav class="nav">
  <div class="container nav-inner">
    <a href="index.html" class="logo" style="text-decoration:none;">SEAN<span>OWN</span></a>
    <input type="checkbox" id="nav-toggle" class="nav-toggle" aria-hidden="true">
    <label for="nav-toggle" class="nav-burger" aria-label="Toggle menu"><span></span><span></span><span></span></label>
    <div class="nav-links">
      <a href="index.html">Home</a>
      <a href="about.html">About</a>
      <a href="news.html">News</a>
      <a href="insights.html">Insights</a>
      <a href="portfolio.html">Work</a>
      <a href="speaking.html">Speaking</a>
      <a href="contact.html">Contact</a>
      <a href="index.html#subscribe" class="btn btn-accent">Subscribe</a>
    </div>
  </div>
</nav>
"""

EXPLORE = """<section class="explore-block">
  <span class="kicker">Continue Exploring</span>
  <h2>More from Sean Own</h2>
  <div class="explore-grid">
    <a href="news.html" class="explore-card"><span class="ex-kicker">Latest</span><h3>News &amp; Press</h3><span class="ex-read">Read →</span></a>
    <a href="bay-youth-ai.html" class="explore-card"><span class="ex-kicker">Event</span><h3>Bay Youth AI Connects The World</h3><span class="ex-read">Read →</span></a>
    <a href="global-influencer-festival.html" class="explore-card"><span class="ex-kicker">Event</span><h3>Global Chinese Influencer Festival</h3><span class="ex-read">Read →</span></a>
    <a href="gba-leadership.html" class="explore-card"><span class="ex-kicker">Council</span><h3>GBA E-Commerce Leadership</h3><span class="ex-read">Read →</span></a>
  </div>
</section>
"""

FOOTER = """<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div><h4>About</h4><p>Sean Own (OWN ZHEN XUAN) is a Macau-based entrepreneur, investor, author, and curator — building China's digital services going-global and a global stage for Chinese culture.</p></div>
      <div><h4>Social</h4><ul><li><a href="https://www.linkedin.com/in/sean-own-36b3108/">LinkedIn</a></li></ul></div>
      <div><h4>Go</h4><ul>
        <li><a href="portfolio.html">Work &amp; Ventures</a></li>
        <li><a href="speaking.html">Speaking</a></li>
        <li><a href="news.html">News &amp; Writing</a></li>
        <li><a href="insights.html">Insights</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul></div>
    </div>
    <div class="copyright">© 2026 Sean Own · Built Static · All Rights Reserved</div>
  </div>
</footer>
</body>
</html>
"""


def render_event(spec: dict) -> str:
    slug = spec["slug"]
    title = spec["title"]
    summary = spec["summary"]
    head = HEAD.format(title=title, summary=summary, slug=slug, style=STYLE)
    hero = (
        f'<header class="hero"><div class="container">'
        f'<div class="eyebrow">{spec.get("kicker","Event")}</div>'
        f'<h1 class="display">{title}</h1>'
        f'<p class="gold-line">{summary}</p></div></header>\n'
    )
    # intro
    intro = '<section class="section"><div class="container"><div class="lead">'
    intro += f'<p>{spec.get("intro","")}</p></div></div></section>\n'
    # stats
    stats_html = '<section class="section alt"><div class="container"><div class="section-head"><div class="kicker">By the numbers</div><h2 class="display">What happened</h2></div><div class="stat-grid">'
    for s in spec.get("stats", []):
        stats_html += f'<div class="stat-card"><div class="stat-num">{s["num"]}</div><div class="stat-label">{s["label"]}</div></div>'
    stats_html += "</div></div></section>\n"
    # gallery
    gal = '<section class="section"><div class="container"><h2 class="display">On the floor</h2><div class="gallery">'
    for img in spec.get("gallery", []):
        alt = f"{title} — {img.split('/')[-1]}"
        gal += f'<img loading="lazy" src="{img}" alt="{alt}">'
    gal += "</div></div></section>\n"
    # venue
    vname = spec.get("venue_name", "")
    vaddr = spec.get("venue_addr", "")
    vslug = spec.get("venue_slug", slug)
    venue = (
        '<section class="section alt"><div class="container"><h2 class="display">Venue</h2>'
        f'<figure class="venue"><img loading="lazy" src="img/map/{vslug}.webp" '
        f'alt="{vname} venue map, {vaddr}, Macao — host of {title}"></figure></div></section>\n'
    )
    # sources
    src = '<div class="source-link">Sources:'
    for s in spec.get("sources", []):
        src += f' <a href="{s["url"]}" target="_blank" rel="noopener">{s["name"]} →</a> &nbsp;'
    src += "</div>\n" if spec.get("sources") else ""
    # cta
    cta = '<section class="cta"><div class="container"><blockquote class="display">"Wealth Grows From The Right Way; Profit Comes Through What Is Just."</blockquote><a href="contact.html" class="btn btn-primary">Work With Me</a></div></section>\n'
    return head + NAV + hero + intro + stats_html + gal + venue + cta + (f"<article>{src}</article>\n" if src.strip() else "") + EXPLORE + FOOTER


def news_card(spec: dict) -> str:
    slug = spec["slug"]
    return (
        f'<a class="news-card" href="{slug}.html">\n'
        f'  <div class="cover"><img loading="lazy" src="{spec.get("cover","")}" alt="{spec["title"]} cover"></div>\n'
        f'  <div class="body"><div class="meta">{spec.get("date_blur","2026")} · Event</div>\n'
        f'  <h3>{spec["title"]}</h3>\n'
        f'  <p>{spec.get("news_blurb", spec.get("summary",""))}</p>\n'
        f'  <span class="read">Read →</span></div>\n</a>'
    )


def inject_news_card(news_path: Path, spec: dict):
    html = news_path.read_text(encoding="utf-8")
    if spec["slug"] in html:
        print("  news.html already has this event — skip injection.")
        return
    marker = '<div class="news-grid">'
    if marker not in html:
        print("  WARN: .news-grid not found in news.html — manual insert needed.")
        return
    card = news_card(spec)
    html = html.replace(marker, marker + "\n  " + card + "\n", 1)
    news_path.write_text(html, encoding="utf-8")
    print("  injected news card into news.html")


def gen_og(slug: str, title: str):
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("generate_og", ROOT / "scripts" / "generate_og.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.PAGES[slug] = title
        mod.gen(slug, title)
        print(f"  OG image: img/og/{slug}.jpg")
    except Exception as e:
        print(f"  WARN: OG generation skipped ({e}). Run scripts/generate_og.py manually.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, help="path to event JSON spec")
    args = ap.parse_args()
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    slug = spec["slug"]
    out = ROOT / f"{slug}.html"
    if out.exists():
        print(f"SKIP: {out.name} already exists. Delete it first to regenerate.")
    else:
        out.write_text(render_event(spec), encoding="utf-8")
        print(f"WROTE {out.name}")
    gen_og(slug, spec["title"])
    inject_news_card(ROOT / "news.html", spec)
    print("DONE. Then run: python scripts/enhance_heads.py  (and add sitemap.xml entry)")


if __name__ == "__main__":
    main()
