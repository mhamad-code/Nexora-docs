/**
 * Nexora Docs — UI behaviour
 * Theme toggle, mobile sidebar, tabs and client-side search.
 *
 * Developed by محمد حمرة (Mohamed Hamra) — https://github.com/mhamad-code
 */
(function () {
  'use strict';

  var doc = document;
  var root = doc.documentElement;

  /* ------------------------------------------------------------------
   * Theme toggle
   * ------------------------------------------------------------------ */
  doc.getElementById('themeBtn').onclick = function () {
    var prefersDark = matchMedia('(prefers-color-scheme: dark)').matches;
    var current = root.dataset.theme || (prefersDark ? 'dark' : 'light');
    var next = current === 'dark' ? 'light' : 'dark';

    root.dataset.theme = next;
    try {
      localStorage.setItem('theme', next);
    } catch (e) {
      /* storage unavailable — theme simply won't persist */
    }
  };

  /* ------------------------------------------------------------------
   * Mobile sidebar
   * ------------------------------------------------------------------ */
  var side = doc.getElementById('side');

  doc.getElementById('menuBtn').onclick = function () {
    side.classList.toggle('open');
  };

  // Close when tapping outside the sidebar.
  doc.addEventListener('click', function (e) {
    var isOpen = side.classList.contains('open');
    var insideSide = side.contains(e.target);
    var onMenuBtn = e.target.closest('#menuBtn');

    if (isOpen && !insideSide && !onMenuBtn) {
      side.classList.remove('open');
    }
  });

  /* ------------------------------------------------------------------
   * Tabs
   * ------------------------------------------------------------------ */
  doc.querySelectorAll('.tabs').forEach(function (tabs) {
    var buttons = tabs.querySelectorAll(':scope > .tab-bar > .tab-btn');
    var panels = tabs.querySelectorAll(':scope > .tab-panel');

    buttons.forEach(function (button, index) {
      button.onclick = function () {
        buttons.forEach(function (b, j) {
          b.classList.toggle('on', index === j);
          panels[j].classList.toggle('on', index === j);
        });
      };
    });
  });

  /* ------------------------------------------------------------------
   * Search
   *   window.SEARCH_INDEX — array of { t: title, g: group, u: url, d: description, x: text }
   *   window.BASE         — URL prefix for result links
   *   window.NO_RES       — localised "no results" label
   * ------------------------------------------------------------------ */
  var input = doc.getElementById('q');
  var results = doc.getElementById('results');
  var index = window.SEARCH_INDEX || [];

  function escapeHtml(str) {
    var map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' };
    return str.replace(/[&<>"]/g, function (c) {
      return map[c];
    });
  }

  // Returns a relevance score, or -1 when any word is missing from the page.
  function score(page, words) {
    var haystack = (page.t + ' ' + page.d + ' ' + page.x).toLowerCase();
    var title = page.t.toLowerCase();
    var description = page.d.toLowerCase();
    var total = 0;

    for (var i = 0; i < words.length; i++) {
      if (haystack.indexOf(words[i]) < 0) {
        return -1;
      }
      total += title.indexOf(words[i]) >= 0 ? 10 : 0;
      total += description.indexOf(words[i]) >= 0 ? 3 : 1;
    }
    return total;
  }

  function renderResult(page) {
    return (
      '<a href="' + window.BASE + page.u + '">' +
        '<b>' + escapeHtml(page.t) + '</b>' +
        '<small>' + escapeHtml(page.g) + ' · ' + escapeHtml(page.d.slice(0, 90)) + '</small>' +
      '</a>'
    );
  }

  input.addEventListener('input', function () {
    var value = input.value.trim().toLowerCase();

    if (!value) {
      results.classList.remove('on');
      return;
    }

    var words = value.split(/\s+/);
    var matches = [];

    index.forEach(function (page) {
      var s = score(page, words);
      if (s > 0) {
        matches.push([s, page]);
      }
    });

    matches.sort(function (a, b) {
      return b[0] - a[0];
    });

    results.innerHTML = matches.length
      ? matches.slice(0, 8).map(function (m) { return renderResult(m[1]); }).join('')
      : '<a><b>' + (window.NO_RES || 'No results') + '</b></a>';

    results.classList.add('on');
  });

  // Close results when clicking elsewhere.
  doc.addEventListener('click', function (e) {
    if (!e.target.closest('.search')) {
      results.classList.remove('on');
    }
  });

  // Press "/" to focus the search box.
  doc.addEventListener('keydown', function (e) {
    if (e.key === '/' && doc.activeElement !== input) {
      e.preventDefault();
      input.focus();
    }
  });
})();
