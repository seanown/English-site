/* ==========================================================
   SEAN OWN — Consent banner (ownsean.com)
   Pairs with js/analytics.js (GA4 Consent Mode v2 Basic).

   Contract:
     - js/analytics.js sets localStorage['seanown_consent'] = 'granted' | 'denied'
       through window.updateConsent(choice). This file only READS that key and
       renders UI when it is absent.
     - Once a choice exists the banner never mounts again, so a returning
       visitor sees no banner and no layout shift.
     - Every button call routes through window.updateConsent(), keeping the
       consent signal and the stored value in one place.

   Conventions (match js/site.js):
     - IIFE, no global pollution, self-defending, no deps.
   ========================================================== */

(function () {
  'use strict';

  var STORAGE_KEY = 'seanown_consent';
  var PRIVACY_URL = 'https://ownsean.com/privacy.html';

  /* ---------- 1. read existing choice ---------- */
  function readConsent() {
    try { return localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  }

  // 'granted' and 'denied' are both final answers — do not re-ask.
  if (readConsent()) return;

  /* ---------- 2. build the banner ---------- */
  var banner = document.createElement('div');
  banner.className = 'consent-banner';
  banner.setAttribute('role', 'dialog');
  banner.setAttribute('aria-live', 'polite');
  banner.setAttribute('aria-label', 'Cookie consent');
  banner.hidden = false;

  var title = document.createElement('strong');
  title.className = 'consent-title';
  title.textContent = 'This site uses cookies';

  var text = document.createElement('p');
  text.textContent = 'I use Google Analytics to understand which pages are read, so I can write more of what is useful. No advertising, no selling your data. You can decline and keep browsing. See the ';
  var link = document.createElement('a');
  link.href = PRIVACY_URL;
  link.textContent = 'privacy policy';
  text.appendChild(link);
  text.appendChild(document.createTextNode('.'));

  var copy = document.createElement('div');
  copy.className = 'consent-copy';
  copy.appendChild(title);
  copy.appendChild(text);

  function makeButton(label, className, value) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'consent-btn ' + className;
    btn.textContent = label;
    btn.addEventListener('click', function () {
      // analytics.js owns the storage write + consent signal.
      if (typeof window.updateConsent === 'function') {
        window.updateConsent(value);
      } else {
        try { localStorage.setItem(STORAGE_KEY, value === 'accept' ? 'granted' : 'denied'); } catch (e) {}
      }
      banner.hidden = true;
    });
    return btn;
  }

  var accept = makeButton('Accept', 'consent-btn-accept', 'accept');
  var reject = makeButton('Decline', 'consent-btn-reject', 'reject');

  var actions = document.createElement('div');
  actions.className = 'consent-actions';
  actions.appendChild(accept);
  actions.appendChild(reject);

  var inner = document.createElement('div');
  inner.className = 'consent-inner';
  inner.appendChild(copy);
  inner.appendChild(actions);

  banner.appendChild(inner);
  document.body.appendChild(banner);

  /* ---------- 3. footer "cookie settings" re-open link ----------
     Gives a way back into the choice after it has been made. Safe to add on
     every page: it is inert until a visitor clicks it.                      */
  function mountSettingsLink() {
    var footer = document.querySelector('footer');
    if (!footer || footer.querySelector('.consent-reset')) return;

    var p = document.createElement('div');
    p.className = 'copyright consent-reset';

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'consent-btn consent-btn-reject';
    btn.textContent = 'Cookie settings';
    btn.addEventListener('click', function () {
      try { localStorage.removeItem(STORAGE_KEY); } catch (e) {}
      banner.hidden = false;
    });

    p.appendChild(btn);
    footer.appendChild(p);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mountSettingsLink);
  } else {
    mountSettingsLink();
  }
})();
