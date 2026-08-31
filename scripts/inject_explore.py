#!/usr/bin/env python3
"""Insert 'Continue Exploring' related grid before <footer> in 5 pages.

Targets: about.html, portfolio.html, speaking.html, research.html, contact.html
Skips pages that already have rel-card / related.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGES = ["about.html","portfolio.html","speaking.html","research.html","contact.html"]

BLOCK = """
<!-- ============ CONTINUE EXPLORING ============ -->
<section class="explore-block">
  <span class="kicker">Continue Exploring</span>
  <h2>More from Sean Own</h2>
  <div class="explore-grid">
    <a href="news.html" class="explore-card">
      <span class="ex-kicker">Latest</span>
      <h3>News &amp; Press</h3>
      <span class="ex-read">Read →</span>
    </a>
    <a href="bay-youth-ai.html" class="explore-card">
      <span class="ex-kicker">Event</span>
      <h3>Bay Youth AI Connects The World</h3>
      <span class="ex-read">Read →</span>
    </a>
    <a href="global-influencer-festival.html" class="explore-card">
      <span class="ex-kicker">Event</span>
      <h3>Global Chinese Influencer Festival</h3>
      <span class="ex-read">Read →</span>
    </a>
    <a href="gba-leadership.html" class="explore-card">
      <span class="ex-kicker">Council</span>
      <h3>GBA E-Commerce Leadership</h3>
      <span class="ex-read">Read →</span>
    </a>
  </div>
</section>
"""

def inject(p):
    txt = p.read_text(encoding="utf-8")
    if 'explore-block' in txt:
        return False
    needle = '<footer class="footer">'
    if needle not in txt:
        print(f"  SKIP {p.name}: no footer anchor")
        return False
    new = txt.replace(needle, BLOCK + "\n" + needle, 1)
    p.write_text(new, encoding="utf-8")
    print(f"  OK   {p.name}: explore-block inserted")
    return True

if __name__ == "__main__":
    n = sum(inject(ROOT / name) for name in PAGES)
    print(f"[done] {n} pages updated")