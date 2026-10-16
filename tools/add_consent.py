#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ownsean.com — Consent 横幅注入器（冪等）

用法：
    python tools/add_consent.py                      # dry-run
    python tools/add_consent.py --apply              # 寫入

設計原則：
- 冪等：已注入的頁面跳過，可重複執行
- 插在 js/site.js 那行之後（同一 defer 區塊，跟在主 runtime 後面）
- 跳過 privacy.html 與 article.html（前者手動放好，後者是重導向 stub）
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

MARKER = 'js/consent-banner.js'
ANCHOR = 'js/site.js'

# 匹配 <script src="js/site.js" defer></script>，容忍任意缩进与属性顺序差异
ANCHOR_RE = re.compile(
    r'^([ \t]*)<script\s+src="js/site\.js"\s+defer\s*></script>[ \t]*$',
    re.MULTILINE,
)

# privacy.html 手動維護（新建時已含正確位置）
SKIP = {'privacy.html', 'article.html'}


def main():
    args = sys.argv[1:]
    apply = '--apply' in args

    pages = sorted(ROOT.glob('*.html'))
    changed, skipped, done = [], [], []

    for p in pages:
        if p.name in SKIP:
            skipped.append(p.name + '（手動維護／重導向 stub）')
            continue

        html = p.read_text(encoding='utf-8')

        # 已注入 → 跳過（冪等）
        if MARKER in html:
            done.append(p.name)
            continue

        m = ANCHOR_RE.search(html)
        if not m:
            skipped.append(p.name + f'（找不到 {ANCHOR}）')
            continue

        # 在 site.js 那行之後插入，沿用同樣的縮排
        indent = m.group(1)
        insertion = f'{indent}<script src="{ANCHOR}" defer></script>\n' \
                    f'{indent}<script src="{MARKER}" defer></script>'
        new = html[:m.start()] + insertion + html[m.end():]

        changed.append(p.name)

        if apply:
            p.write_text(new, encoding='utf-8')

    mode = 'APPLY' if apply else 'DRY-RUN（未寫入）'
    print(f'\n───── {mode} ─────')
    print(f'頁面總數    : {len(pages)}')
    print(f'需注入      : {len(changed)}')
    for n in changed:
        print(f'   + {n}')
    if done:
        print(f'已注入略過  : {len(done)}')
    if skipped:
        print(f'跳過        : {", ".join(skipped)}')

    if not apply and changed:
        print('\n確認無誤後加 --apply 執行。')
    elif apply:
        print(f'\n完成。下一件事：把 privacy.html 加進 sitemap.xml（未自動改）。')


if __name__ == '__main__':
    main()
