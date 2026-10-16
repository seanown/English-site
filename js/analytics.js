/* ownsean.com — Google Analytics 4
 * 獨立於中文站 seanown.org 的 GA4 資料流，兩站數據互不干擾。
 *
 * Consent Mode v2（Basic）：預設 denied，量測 ID 一律先載入，
 * 同意後由 updateConsent() 補發 consent signals，不阻塞首屏。
 */
(function () {
  'use strict';

  var GA_ID = 'G-J92ZJ07QRW';
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
