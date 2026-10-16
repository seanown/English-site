#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ownsean.com — GA4 埋點注入器（冪等）

用法：
    python tools/add_ga.py                 # dry-run，只報告會改哪裡
    python tools/add_ga.py --apply         # 實際寫入
    python tools/add_ga.py --apply --id G-XXXXXXXXXX   # 指定 ID

設計原則：
- 冪等：已埋過的頁面跳過，可重複執行
- 統一用 js/analytics.js 外部檔案（可集中改 Consent 邏輯）
- noscript 版 G-XXXXXXXXXX 自動同步
- 有給體的 html 才處理；404.html 也埋（GA 認得 404 是行為不是頁面）
"""
import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# ── GA4 Measurement ID ──────────────────────────────────
# 預設留空：軒哥確認 ID 後改這裡，或跑指令時帶 --id
GA_ID = ""  # 例："G-9Z5XZML16S"

TARGET = "js/analytics.js"

ANALYTICS_JS = """/* ownsean.com — Google Analytics 4
 * 獨立於中文站 seanown.org 的 GA4 資料流，兩站數據互不干擾。
 *
 * Consent Mode v2（Basic）：預設 denied，量測 ID 一律先載入，
 * 同意後由 updateConsent() 補發 consent signals，不阻塞首屏。
 */
(function () {
  'use strict';

  var GA_ID = '{GA_ID}';
  var STORAGE_KEY = 'seanown_consent';

  // ── 1. 預設全部拒絕（Basic consent），先於 gtag.js 執行 ──
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  function setConsent(analytics) {
    gtag('consent', 'default', {
      analytics_storage: analytics,
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied',
      wait_for_update: 500
    });
  }
  setConsent('denied');

  // ── 2. 讀取既有同意狀態 ──
  function readConsent() {
    try { return localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  }
  var saved = readConsent();
  if (saved === 'granted') setConsent('granted');
  if (saved === 'denied') setConsent('denied');

  // ── 3. 載入 gtag.js ──
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(s);

  gtag('js', new Date());
  gtag('config', GA_ID, { anonymize_ip: true });

  // ── 4. 同意更新機制 ──
  window.updateConsent = function (choice) {
    var v = choice === 'accept' ? 'granted' : 'denied';
    try { localStorage.setItem(STORAGE_KEY, v); } catch (e) {}
    gtag('consent', 'update', {
      analytics_storage: v,
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });
    gtag('event', 'consent_update', { consent_state: v });
    document.dispatchEvent(new CustomEvent('consentchange', { detail: v }));
  };
})();
"""


def build_snippet(ga_id: str, indent: str) -> str:
    """產生要插在 </head> 前的那段。"""
    return (
        f'{indent}<!-- Google Analytics 4 — ownsean.com (Consent Mode v2 Basic) -->\n'
        f'{indent}<script src="js/analytics.js"></script>\n'
        f'{indent}<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={ga_id}" '
        f'style="display:none;visibility:hidden" title="ga"></iframe></noscript>'
    )


def main():
    args = sys.argv[1:]
    apply = '--apply' in args
    ga_id = GA_ID

    if '--id' in args:
        i = args.index('--id')
        ga_id = args[i + 1].strip()
    elif not ga_id:
        sys.exit('[停] 未提供 GA4 ID。\n'
                 '用法：python tools/add_ga.py --apply --id G-XXXXXXXXXX')

    if not re.fullmatch(r'G-[A-Z0-9]{6,12}', ga_id):
        sys.exit(f'[停] GA4 ID 格式不正確：{ga_id}（應為 G-XXXXXXXXXX）')

    # ── 寫 analytics.js ──
    content = ANALYTICS_JS.replace('{GA_ID}', ga_id)
    tgt = ROOT / TARGET
    exists = tgt.exists() and tgt.read_text(encoding='utf-8') == content

    if not exists:
        if apply:
            tgt.write_text(content, encoding='utf-8')
            print(f'[寫入] {TARGET}')
        else:
            print(f'[將寫入] {TARGET}  ({len(content)} bytes)')
    else:
        print(f'[略過] {TARGET} 內容未變')

    # ── 找出所有有 </head> 的 html ──
    pages = sorted(ROOT.glob('*.html'))
    # 跳過純重導向 stub
    skip = {'article.html'}
    changed, skipped, done = [], [], []

    snippet_cache = {}

    for p in pages:
        if p.name in skip:
            skipped.append(p.name + '（重導向 stub）')
            continue
        html = p.read_text(encoding='utf-8')

        # 已埋過 → 跳過（冪等）
        if 'js/analytics.js' in html or ga_id in html:
            done.append(p.name)
            continue

        if '</head>' not in html:
            skipped.append(p.name + '（無 </head>）')
            continue

        if p.name not in snippet_cache:
            snippet_cache[p.name] = build_snippet(ga_id, '  ')

        new = html.replace('</head>', snippet_cache[p.name] + '\n</head>', 1)
        changed.append(p.name)

        if apply:
            p.write_text(new, encoding='utf-8')

    mode = 'APPLY' if apply else 'DRY-RUN（未寫入）'
    print(f'\n───── {mode} ─────')
    print(f'GA4 ID      : {ga_id}')
    print(f'頁面總數    : {len(pages)}')
    print(f'需埋點      : {len(changed)}')
    for n in changed:
        print(f'   + {n}')
    if done:
        print(f'已埋略過    : {len(done)}')
    if skipped:
        print(f'跳過        : {", ".join(skipped)}')

    if not apply and changed:
        print('\n確認無誤後加 --apply 執行。')
    elif apply:
        print('\n完成。接著：commit → push（Netlify 自動部署）')


if __name__ == '__main__':
    main()