(function () {
  'use strict';

  // Privacy-friendly YouTube facade: the iframe is only created on click.
  document.querySelectorAll('.video-frame[data-video-id]').forEach(function (frame) {
    var button = frame.querySelector('.video-play');
    if (!button) return;
    button.addEventListener('click', function () {
      var id = frame.getAttribute('data-video-id');
      var title = frame.getAttribute('data-video-title') || 'YouTube video';
      var iframe = document.createElement('iframe');
      iframe.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0';
      iframe.title = title;
      iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      iframe.allowFullscreen = true;
      iframe.loading = 'lazy';
      frame.textContent = '';
      frame.appendChild(iframe);
    });
  });

  // Build an "On this page" table of contents from h2/h3 headings.
  var content = document.querySelector('.lesson-content, .doc-content, .page-content');
  var tocNavs = document.querySelectorAll('[data-toc]');
  if (content && tocNavs.length) {
    var headings = Array.prototype.slice.call(content.querySelectorAll('h2, h3'));
    headings.forEach(function (heading, index) {
      if (!heading.id) {
        var slug = heading.textContent.toLowerCase().replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-');
        heading.id = slug || 'section-' + index;
      }
    });
    tocNavs.forEach(function (nav) {
      nav.textContent = '';
      headings.forEach(function (heading) {
        var link = document.createElement('a');
        link.href = '#' + heading.id;
        link.textContent = heading.textContent;
        link.className = heading.tagName === 'H3' ? 'toc-h3' : 'toc-h2';
        nav.appendChild(link);
      });
      if (!headings.length) {
        var card = nav.closest('.toc-card');
        if (card) card.hidden = true;
      }
    });

    if ('IntersectionObserver' in window && headings.length) {
      var links = document.querySelectorAll('[data-toc] a');
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          links.forEach(function (link) {
            link.classList.toggle('is-active', link.getAttribute('href') === '#' + entry.target.id);
          });
        });
      }, { rootMargin: '-90px 0px -70% 0px', threshold: 0 });
      headings.forEach(function (heading) { observer.observe(heading); });
    }
  }

  // Copy buttons for fenced code blocks.
  if (navigator.clipboard) {
    document.querySelectorAll('.prose pre').forEach(function (pre) {
      var button = document.createElement('button');
      button.type = 'button';
      button.className = 'copy-code';
      button.textContent = 'Copy';
      button.addEventListener('click', function () {
        var code = pre.querySelector('code');
        var text = code ? code.innerText : pre.innerText;
        navigator.clipboard.writeText(text).then(function () {
          button.textContent = 'Copied';
          window.setTimeout(function () { button.textContent = 'Copy'; }, 1600);
        }).catch(function () {
          button.textContent = 'Copy failed';
          window.setTimeout(function () { button.textContent = 'Copy'; }, 1600);
        });
      });
      pre.appendChild(button);
    });
  }

  // Reading progress for lesson pages.
  var article = document.getElementById('lesson-content');
  var bar = document.querySelector('[data-reading-progress]');
  if (article && bar) {
    var update = function () {
      var rect = article.getBoundingClientRect();
      var viewport = window.innerHeight;
      var total = rect.height - viewport;
      var progress = total > 0 ? ((0 - rect.top) / total) * 100 : 0;
      bar.style.width = Math.min(100, Math.max(0, progress)) + '%';
    };
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  }
})();
