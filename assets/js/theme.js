(function () {
  'use strict';

  var root = document.documentElement;
  var toggle = document.querySelector('[data-theme-toggle]');
  var media = window.matchMedia('(prefers-color-scheme: dark)');

  function storedTheme() {
    try { return localStorage.getItem('theme'); } catch (error) { return null; }
  }

  function applyTheme(theme) {
    root.dataset.theme = theme;
    if (toggle) {
      var dark = theme === 'dark';
      toggle.setAttribute('aria-pressed', String(dark));
      toggle.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
    }
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', theme === 'dark' ? '#0b0b0c' : '#ffffff');
  }

  // The inline script in <head> already set the initial theme. Sync the button.
  applyTheme(root.dataset.theme || (media.matches ? 'dark' : 'light'));

  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = root.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem('theme', next); } catch (error) { /* storage blocked */ }
      applyTheme(next);
    });
  }

  media.addEventListener('change', function (event) {
    if (!storedTheme()) applyTheme(event.matches ? 'dark' : 'light');
  });

  // Mobile navigation
  var navToggle = document.querySelector('[data-nav-toggle]');
  var nav = document.getElementById('site-nav');
  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', function (event) {
      if (event.target.closest('a')) {
        nav.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') {
        nav.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 900) {
        nav.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // Current year in the footer
  var year = document.querySelector('[data-current-year]');
  if (year) year.textContent = String(new Date().getFullYear());
})();
