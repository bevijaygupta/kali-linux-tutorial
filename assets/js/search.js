(function () {
  'use strict';

  var body = document.body;
  var baseurl = (body.dataset.baseurl || '').replace(/\/$/, '');
  var indexUrl = body.dataset.searchIndex;
  var widgets = Array.prototype.slice.call(document.querySelectorAll('[data-lesson-search]'));
  var overlay = document.querySelector('[data-search-overlay]');
  var openButton = document.querySelector('[data-search-open]');
  var closeButton = document.querySelector('[data-search-close]');
  var lastFocus = null;
  var index = null;
  var loadPromise = null;
  var state = new WeakMap();

  if (!widgets.length || !indexUrl) return;

  function loadIndex() {
    if (index) return Promise.resolve(index);
    if (loadPromise) return loadPromise;
    loadPromise = fetch(indexUrl, { credentials: 'same-origin' })
      .then(function (response) {
        if (!response.ok) throw new Error('HTTP ' + response.status);
        return response.json();
      })
      .then(function (data) {
        index = data;
        return index;
      })
      .catch(function (error) {
        loadPromise = null;
        throw error;
      });
    return loadPromise;
  }

  function normalize(value) {
    return String(value || '')
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '');
  }

  function score(entry, terms) {
    var title = normalize(entry.title);
    var module = normalize(entry.module);
    var tags = normalize((entry.tags || []).join(' '));
    var text = normalize(entry.text);
    var total = 0;
    for (var i = 0; i < terms.length; i += 1) {
      var term = terms[i];
      if (!term) continue;
      if (String(entry.chapter) === term || String(entry.number) === term) total += 50;
      if (title.indexOf(term) !== -1) total += 12;
      if (title.indexOf(term) === 0) total += 10;
      if (tags.indexOf(term) !== -1) total += 6;
      if (module.indexOf(term) !== -1) total += 3;
      if (text.indexOf(term) !== -1) total += 2;
    }
    return total;
  }

  function makeResult(entry) {
    var link = document.createElement('a');
    link.className = 'search-result';
    link.href = baseurl + entry.url;
    link.setAttribute('role', 'option');

    var title = document.createElement('span');
    title.className = 'search-result-title';
    title.textContent = entry.title;
    link.appendChild(title);

    var meta = document.createElement('span');
    meta.className = 'search-result-meta';
    var bits = ['Chapter ' + entry.chapter, entry.status === 'published' ? 'Published' : 'Scheduled'];
    if (entry.duration) bits.push(entry.duration);
    if (entry.module) bits.push(entry.module);
    meta.textContent = bits.join(' · ');
    link.appendChild(meta);

    if (entry.description) {
      var desc = document.createElement('span');
      desc.className = 'search-result-desc';
      desc.textContent = entry.description;
      link.appendChild(desc);
    }
    return link;
  }

  function render(widget, results, term) {
    var container = widget.querySelector('[data-search-results]');
    var hint = widget.querySelector('[data-search-hint]');
    if (!container) return;
    container.textContent = '';
    var widgetState = state.get(widget) || { active: -1 };
    widgetState.active = -1;
    state.set(widget, widgetState);

    if (!term) {
      if (hint) hint.textContent = 'Try “nmap”, “permissions” or “wireshark”.';
      return;
    }
    if (!results.length) {
      if (hint) hint.textContent = 'No lesson matched “' + term + '”. Try a tool name, chapter number or topic.';
      return;
    }
    if (hint) hint.textContent = results.length + (results.length === 1 ? ' lesson found.' : ' lessons found.') + ' Use arrow keys and Enter.';
    results.forEach(function (entry) {
      container.appendChild(makeResult(entry));
    });
  }

  function search(widget, raw) {
    var term = raw.trim();
    var terms = normalize(term).split(/\s+/).filter(Boolean);
    if (!term) {
      render(widget, [], '');
      return;
    }
    loadIndex()
      .then(function (data) {
        var results = data
          .map(function (entry) { return { entry: entry, points: score(entry, terms) }; })
          .filter(function (item) { return item.points > 0; })
          .sort(function (a, b) { return b.points - a.points || a.entry.chapter - b.entry.chapter; })
          .slice(0, 8)
          .map(function (item) { return item.entry; });
        render(widget, results, term);
      })
      .catch(function () {
        var hint = widget.querySelector('[data-search-hint]');
        if (hint) {
          hint.textContent = 'Search index could not load. Open the lessons page to browse all chapters.';
        }
      });
  }

  widgets.forEach(function (widget) {
    var input = widget.querySelector('[data-search-input]');
    if (!input) return;
    state.set(widget, { active: -1 });
    var timer = null;
    input.addEventListener('input', function () {
      window.clearTimeout(timer);
      var value = input.value;
      timer = window.setTimeout(function () { search(widget, value); }, 90);
    });
    input.addEventListener('focus', function () { loadIndex().catch(function () {}); });
    input.addEventListener('keydown', function (event) {
      var container = widget.querySelector('[data-search-results]');
      if (!container) return;
      var links = Array.prototype.slice.call(container.querySelectorAll('.search-result'));
      if (!links.length) return;
      var widgetState = state.get(widget) || { active: -1 };
      if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
        event.preventDefault();
        var delta = event.key === 'ArrowDown' ? 1 : -1;
        widgetState.active = (widgetState.active + delta + links.length) % links.length;
        links.forEach(function (link, index) { link.classList.toggle('is-active', index === widgetState.active); });
        links[widgetState.active].scrollIntoView({ block: 'nearest' });
        state.set(widget, widgetState);
      } else if (event.key === 'Enter' && widgetState.active >= 0) {
        event.preventDefault();
        links[widgetState.active].click();
      }
    });
  });

  function openOverlay() {
    if (!overlay) return;
    lastFocus = document.activeElement;
    overlay.hidden = false;
    document.body.style.overflow = 'hidden';
    var input = overlay.querySelector('[data-search-input]');
    if (input) {
      input.value = '';
      window.setTimeout(function () { input.focus(); }, 30);
      var widget = overlay.querySelector('[data-lesson-search]');
      if (widget) render(widget, [], '');
    }
  }

  function closeOverlay() {
    if (!overlay || overlay.hidden) return;
    overlay.hidden = true;
    document.body.style.overflow = '';
    if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();
  }

  if (openButton) openButton.addEventListener('click', openOverlay);
  if (closeButton) closeButton.addEventListener('click', closeOverlay);
  if (overlay) {
    overlay.addEventListener('click', function (event) {
      if (event.target === overlay) closeOverlay();
    });
  }
  document.addEventListener('keydown', function (event) {
    var target = event.target;
    var typing = target && (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable);
    if (event.key === 'Escape') closeOverlay();
    if ((event.key === '/' && !typing) || ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k')) {
      event.preventDefault();
      openOverlay();
    }
  });
})();
