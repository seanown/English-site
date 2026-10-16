#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ownsean.com — footer Privacy 連結注入器（冪等）

用法：
    python tools/add_privacy_link.py            # dry-run
    python tools/add_privacy_link.py --apply    # 寫入

做法：在每頁 <div class="copyright">…</div> 內，於版權文字後追加
      「· <a href="privacy.html">Privacy</a>」。

選 copyright 而非 footer 的「Go」欄，原因：全站 21 頁都有 copyright，
但只有 17 頁有標準「Go」欄且縮排/連結集各頁不一，逐一硬改風險高。

privacy.html 自身跳過（已手動放好）。
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# 抓 <div|p class="copyright"> ... </div|p> 的整段
COPYRIGHT_RE = re.compile(
    r'(<(?:div|p)\s+class="copyright"[^>]*>)(.*?)(</(?:div|p)>)',
    re.DOTALL,
)

# 抓已存在的 privacy 連結（冪等判據用）
PRIVACY_LINK_RE = re.compile(r'href="privacy\.html"')

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

        m = COPYRIGHT_RE.search(html)
        if not m:
            skipped.append(p.name + '（找不到 copyright 區塊）')
            continue

        block = m.group(0)
        if PRIVACY_LINK_RE.search(block):
            done.append(p.name)
            continue

        inner = m.group(2)
        # 保留原縮排：抓 inner 開頭的空白
        lead = re.match(r'^[ \t]*', inner).group(0)
        new_inner = inner.rstrip() + \
            f' · <a href="privacy.html">Privacy</a>'

        new_block = m.group(1) + new_inner + m.group(3)
        new_html = html[:m.start()] + new_block + html[m.end():]

        changed.append(p.name)

        if apply:
            p.write_text(new_html, encoding='utf-8')

    mode = 'APPLY' if apply else 'DRY-RUN（未寫入）'
    print(f'\n───── {mode} ─────')
    print(f'頁面總數    : {len(pages)}')
    print(f'需加連結    : {len(changed)}')
    for n in changed:
        print(f'   + {n}')
    if done:
        print(f'已有連結    : {", ".join(done)}')
    if skipped:
        print(f'跳過        : {", ".join(skipped)}')

    if not apply and changed:
        print('\n確認無誤後加 --apply 執行。')
    elif apply:
        print('\n完成。')


if __name__ == '__main__':
    main()
