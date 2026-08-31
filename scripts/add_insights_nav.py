#!/usr/bin/env python3
"""add_insights_nav.py — 把 'Insights' 接入全站（#C SEO 内容矩阵扩张）。

- 在主 NAV 的 News 連結後插入 <a href="insights.html">Insights</a>
- 在 footer 'Go' 區塊的 </ul> 前插入 <li><a href="insights.html">Insights</a></li>
- 冪等：檔案已含 insights.html 則跳過（insights.html 本身已寫好）
- 不動任何 JS / 設計系統
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NAV_RE = re.compile(r'(<a href="news\.html"[^>]*>News</a>)')
FOOTER_RE = re.compile(r'(</ul>\s*(?:</div>\s*)+<div class="copyright">)')
INSIGHTS_NAV = '<a href="insights.html">Insights</a>'
INSIGHTS_LI = '          <li><a href="insights.html">Insights</a></li>'

def process(path: Path):
    text = path.read_text(encoding="utf-8")
    original = text
    actions = []
    # NAV: skip this page's own nav if it already carries the Insights link
    if '<a href="insights.html"' not in text and NAV_RE.search(text):
        text = NAV_RE.sub(lambda m: m.group(1) + "\n      " + INSIGHTS_NAV, text, count=1)
        actions.append("nav")
    # FOOTER: skip if the Insights <li> is already present
    if '<li><a href="insights.html">Insights</a></li>' not in text and FOOTER_RE.search(text):
        text = FOOTER_RE.sub(lambda m: INSIGHTS_LI + "\n" + m.group(1), text, count=1)
        actions.append("footer")
    if actions:
        path.write_text(text, encoding="utf-8")
        print(f"  updated {path.name}: {', '.join(actions)}")
    elif text != original:
        path.write_text(text, encoding="utf-8")
        print(f"  touched {path.name}")
    else:
        print(f"  no change {path.name}")

def main():
    targets = [p for p in sorted(ROOT.glob("*.html")) if p.name != "insights.html"]
    print(f"Wiring Insights into {len(targets)} pages...")
    for p in targets:
        process(p)
    print("DONE.")

if __name__ == "__main__":
    main()
