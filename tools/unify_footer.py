#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ownsean.com — footer 統一化工具（安全版）

政策（全站單一真源＝ABOUT_TXT / SOCIAL_TXT / GO_LINKS / COPYRIGHT_TXT）：
  · About / Social 兩欄統一
  · Go 欄連結集統一為 GO_LINKS
  · 版權行統一（含 Privacy 連結）

安全範圍（刻意「不動」）：
  · index.html     —— 第三欄是 Netlify 訂閱表單（data-netlify），覆蓋會弄壞訂閱功能
                     → 只統一 About/Social/版權行，保留 Subscribe 欄原樣
  · gba-leadership —— 淺色簡易版是刻意設計（呼應文章調性）→ 僅補齊 Privacy 連結
  · 404 / eci / article —— 錯誤頁與跳轉中轉頁，無標準 footer → 維持原樣
  · capital-culture-civilisation / macau-five-year-plan-3rd —— 現為 Index 欄，改為 Go

用法：
    python tools/unify_footer.py            # dry-run
    python tools/unify_footer.py --apply    # 寫入
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# ── 全站單一真源 ────────────────────────────────────────────
ABOUT_TXT = ("Sean Own (OWN ZHEN XUAN) is a Macau-based entrepreneur, investor, "
             "author, and curator — building China's digital services going-global "
             "and a global stage for Chinese culture. Let's build what outlasts "
             "beyond profit.")

LINKEDIN = "https://www.linkedin.com/in/sean-own-36b3108/"

# Go 欄：多數共識（portfolio / speaking / news / contact）＋補齊 privacy、insights
GO_LINKS = [
    ("portfolio.html", "Work &amp; Ventures"),
    ("insights.html", "Insights"),
    ("speaking.html", "Speaking"),
    ("news.html", "News &amp; Writing"),
    ("privacy.html", "Privacy"),
    ("contact.html", "Contact"),
]

COPYRIGHT_TXT = "© 2026 Sean Own · Built Static · All Rights Reserved"

# ── 安全範圍 ────────────────────────────────────────────────
KEEP_THIRD_COLUMN = {'index.html'}   # 保留訂閱表單
CUSTOM_FOOTER = {'gba-leadership.html'}  # 淺色簡易版，只補 Privacy
NO_FOOTER = {'404.html', 'eci.html', 'article.html'}  # 本來就沒 footer


def replace_about(html: str) -> tuple:
    """把 About 欄的 <p> 換成統一文案。"""
    pat = re.compile(
        r'(<h4[^>]*>About</h4>\s*)<p[^>]*>.*?</p>',
        re.DOTALL,
    )
    m = pat.search(html)
    if not m:
        return html, False
    new = m.group(1) + f'<p>{ABOUT_TXT}</p>'
    return html[:m.start()] + new + html[m.end():], True


def replace_social(html: str) -> tuple:
    """統一 Social 欄為單一 LinkedIn。"""
    pat = re.compile(
        r'(<h4[^>]*>Social</h4>\s*<ul[^>]*>).*?(</ul>)',
        re.DOTALL,
    )
    m = pat.search(html)
    if not m:
        return html, False
    inner = f'\n          <li><a href="{LINKEDIN}">LinkedIn</a></li>\n        '
    return html[:m.start()] + m.group(1) + inner + m.group(2) + html[m.end():], True


def build_go_column(indent: str) -> str:
    lines = [f'{indent}<h4>Go</h4>', f'{indent}<ul>']
    for href, label in GO_LINKS:
        lines.append(f'{indent}  <li><a href="{href}">{label}</a></li>')
    lines.append(f'{indent}</ul>')
    return '\n'.join(lines)


def replace_nav_column(html: str, indent: str) -> tuple:
    """把 Go 或 Index 欄換成統一 Go 欄。"""
    pat = re.compile(
        r'[ \t]*<h4[^>]*>(?:Go|Index)</h4>\s*<ul[^>]*>.*?</ul>',
        re.DOTALL,
    )
    m = pat.search(html)
    if not m:
        return html, False
    return html[:m.start()] + build_go_column(indent) + html[m.end():], True


def replace_copyright(html: str) -> tuple:
    """統一版權行文字，Privacy 連結保持。"""
    pat = re.compile(
        r'(<(?:div|p)\s+class="copyright"[^>]*>).*?(</(?:div|p)>)',
        re.DOTALL,
    )
    m = pat.search(html)
    if not m:
        return html, False
    new_inner = f'{COPYRIGHT_TXT} · <a href="privacy.html">Privacy</a>'
    return html[:m.start()] + m.group(1) + new_inner + m.group(2) + html[m.end():], True


def main():
    args = sys.argv[1:]
    apply = '--apply' in args

    pages = sorted(ROOT.glob('*.html'))
    report, skipped = [], []

    for p in pages:
        if p.name in NO_FOOTER:
            skipped.append(f'{p.name}（無標準 footer，維持原樣）')
            continue

        if p.name in CUSTOM_FOOTER:
            # 只補 Privacy 連結，不改結構
            html = p.read_text(encoding='utf-8')
            if 'privacy.html' in html:
                skipped.append(f'{p.name}（淺色簡易版，已有 Privacy）')
                continue
            pat = re.compile(r'(<div>© 2026 Sean Own[^<]*?Association)(</div>)')
            m = pat.search(html)
            if not m:
                skipped.append(f'{p.name}（未找到版權行，需手動）')
                continue
            new = html[:m.start()] + m.group(1) + \
                ' · <a href="privacy.html">Privacy</a>' + m.group(2) + html[m.end():]
            if apply:
                p.write_text(new, encoding='utf-8')
            report.append((p.name, '淺色版：補 Privacy 連結'))
            continue

        html = p.read_text(encoding='utf-8')
        orig = html
        notes = []

        html, ok = replace_about(html)
        notes.append('About' if ok else '')

        html, ok = replace_social(html)
        notes.append('Social' if ok else '')

        if p.name not in KEEP_THIRD_COLUMN:
            html, ok = replace_nav_column(html, ' ' * 8)
            notes.append('Go' if ok else '')
        else:
            notes.append('Go(保留訂閱表單)')

        html, ok = replace_copyright(html)
        notes.append('版權行' if ok else '')

        if html == orig:
            skipped.append(f'{p.name}（已一致，無需改動）')
            continue

        if apply:
            p.write_text(html, encoding='utf-8')

        report.append((p.name, '＋'.join(n for n in notes if n)))

    mode = 'APPLY' if apply else 'DRY-RUN（未寫入）'
    print(f'\n───── {mode} ─────')
    print(f'會變更頁數  : {len(report)}')
    for name, note in report:
        print(f'   · {name:<38} {note}')
    if skipped:
        print(f'\n維持原樣    : {len(skipped)}')
        for s in skipped:
            print(f'   · {s}')

    if not apply:
        print('\n確認無誤後加 --apply 執行。')
    else:
        print('\n完成。')


if __name__ == '__main__':
    main()