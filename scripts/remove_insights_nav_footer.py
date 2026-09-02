"""remove_insights_nav_footer.py - Reverse of add_insights_nav.py.

After 2026-09-02 user decision: top-nav + footer no longer expose Insights.
The page insights.html stays; news page carries an upgraded card as entry-point.
This script removes the four offending lines across all *.html.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NAV_PATTERN = re.compile(
    r'^\s*<a href="insights\.html"(?: class="active")?>Insights</a>\s*\n',
    re.M,
)
FOOTER_PATTERN = re.compile(
    r'^\s*<li><a href="insights\.html">Insights</a></li>\s*\n',
    re.M,
)
A_404_PATTERN = re.compile(
    r'^\s*<a href="/insights\.html">Insights</a>\s*\n',
    re.M,
)
A_404_COLUMN_PATTERN = re.compile(
    r'^\s*<a href="/insights\.html"><small>Column</small>Insights &amp; Perspectives</a>\s*\n',
    re.M,
)

total_nav = 0
total_footer = 0
total_404 = 0
touched = []
for html in sorted(ROOT.glob("*.html")):
    text = html.read_text(encoding="utf-8")
    new, n1 = NAV_PATTERN.subn('', text)
    new, n2 = FOOTER_PATTERN.subn('', new)
    new, n3a = A_404_PATTERN.subn('', new)
    new, n3b = A_404_COLUMN_PATTERN.subn('', new)
    if n1 + n2 + n3a + n3b:
        html.write_text(new, encoding="utf-8")
        total_nav += n1
        total_footer += n2
        total_404 += n3a + n3b
        touched.append(f"{html.name}: nav={n1} footer={n2} 404={n3a+n3b}")

print("Touched files:")
for t in touched:
    print(f"  {t}")
print("---")
print(f"NAV lines removed: {total_nav}")
print(f"FOOTER lines removed: {total_footer}")
print(f"404 lines removed: {total_404}")

# Verify zero leftover
leftover_count = 0
for html in sorted(ROOT.glob("*.html")):
    t = html.read_text(encoding="utf-8")
    if re.search(r'href=["\'][/]?insights\.html["\']', t):
        leftover_count += 1
        # print offending lines for debug
        for ln in t.splitlines():
            if 'href="insights.html"' in ln or "href='/insights.html'" in ln:
                print(f"  LEFTOVER in {html.name}: {ln.strip()[:120]}")
print(f"\nFiles still referencing insights.html: {leftover_count}")
