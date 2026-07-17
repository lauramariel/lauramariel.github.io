(function () {
  var root = document.documentElement;
  var themeToggle = document.getElementById('theme-toggle');

  function syncThemeButton() {
    if (!themeToggle) return;
    var isDark = root.getAttribute('data-theme') === 'dark';
    themeToggle.setAttribute('aria-pressed', isDark);
  }

  syncThemeButton();

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      localStorage.setItem('theme', next);
      root.setAttribute('data-theme', next);
      syncThemeButton();
    });
  }

  var navToggle = document.querySelector('.nav-toggle');
  var navLinks = document.getElementById('nav-links');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function () {
      var isOpen = navLinks.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', isOpen);
    });
  }

  var COPY_ICON = '<svg viewBox="0 0 20 20" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="6.5" y="6.5" width="10" height="10" rx="1.5"/><path d="M4.5 13.5H3.5A1.5 1.5 0 0 1 2 12V3.5A1.5 1.5 0 0 1 3.5 2H12a1.5 1.5 0 0 1 1.5 1.5v1"/></svg>';
  var CHECK_ICON = '<svg viewBox="0 0 20 20" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 10.5l3.5 3.5L16 6"/></svg>';

  function initCopyButtons() {
    if (!navigator.clipboard || !navigator.clipboard.writeText) return;

    var blocks = document.querySelectorAll('.highlighter-rouge');

    blocks.forEach(function (block) {
      var codeEl = block.querySelector('pre.highlight code') || block.querySelector('code');
      if (!codeEl) return;

      var button = document.createElement('button');
      button.type = 'button';
      button.className = 'copy-code-btn';
      button.setAttribute('aria-label', 'Copy code');
      button.innerHTML = COPY_ICON;

      button.addEventListener('click', function () {
        navigator.clipboard.writeText(codeEl.textContent).then(function () {
          button.innerHTML = CHECK_ICON + '<span class="copy-code-btn-label">Copied</span>';
          button.classList.add('is-copied');
          setTimeout(function () {
            button.innerHTML = COPY_ICON;
            button.classList.remove('is-copied');
          }, 1500);
        });
      });

      block.insertBefore(button, block.firstChild);
    });
  }

  initCopyButtons();
})();
