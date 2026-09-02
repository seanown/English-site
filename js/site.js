/* ==========================================================
   SEAN OWN — English-site client runtime
   Vanilla JS · No deps · Defer-loaded on every page
   ==========================================================
   Conventions:
     - IIFE wrapping, no global pollution
     - Each module self-defends (returns early if no element found)
     - DOM hooks via data-* attrs (never class triggers)
     - Hidden state via element.hidden (semantic, a11y-friendly)
     - Animations are CSS; JS toggles class / hidden only
   ========================================================== */

(function () {
  'use strict';

  /* ============================================================
     SECTION 1 — News Category Filter
     ============================================================
     Markup contract:
       - One .news-grid container on news.html
       - Filter buttons carry data-cat="<category|all>"
       - Each <article class="news-card"> carries data-category="<category>"
       - Optional: Tech placeholder card (data-category="tech", hidden by default)
     Behavior:
       - Click button -> mark .active, set aria-pressed, filter cards
       - "all" shows every data-category (including the Tech placeholder)
       - No animation (instant show/hide per design rule)
     ============================================================ */
  function initNewsFilter() {
    var grid = document.querySelector('.news-grid');
    if (!grid) return;

    var buttons = document.querySelectorAll('[data-cat]');
    var cards = grid.querySelectorAll('.news-card');
    if (!buttons.length || !cards.length) return;

    function apply(category) {
      // 1) button active state + a11y
      for (var i = 0; i < buttons.length; i++) {
        var btn = buttons[i];
        var isActive = btn.dataset.cat === category;
        if (isActive) {
          btn.classList.add('active');
          btn.setAttribute('aria-pressed', 'true');
        } else {
          btn.classList.remove('active');
          btn.setAttribute('aria-pressed', 'false');
        }
      }

      // 2) card visibility
      for (var j = 0; j < cards.length; j++) {
        var card = cards[j];
        var cardCat = card.dataset.category || '';
        var match = (category === 'all' || cardCat === category);
        card.hidden = !match;
      }
    }

    for (var k = 0; k < buttons.length; k++) {
      buttons[k].addEventListener('click', function (e) {
        var cat = e.currentTarget.dataset.cat;
        if (cat) apply(cat);
      });
    }
  }

  /* ============================================================
     SECTION 2 — [Placeholder] Mobile Nav Toggle (future)
     SECTION 3 — [Placeholder] Smooth Scroll (future)
     SECTION 4 — [Placeholder] Form Validation (future)
     ============================================================
     When a new interactive feature is needed, add an initXxx()
     function below and dispatch it in bootstrap().
     ============================================================ */

  /* ============================================================
     Bootstrap
     ============================================================ */
  function bootstrap() {
    initNewsFilter();
    // initMobileNav();     // future
    // initSmoothScroll();  // future
    // initFormValidation(); // future
  }

  // defer ensures DOM is parsed when this runs, but be defensive anyway
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootstrap);
  } else {
    bootstrap();
  }
})();
