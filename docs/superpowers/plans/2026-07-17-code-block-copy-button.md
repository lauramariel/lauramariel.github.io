# Code Block Copy Button Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a hover-revealed copy button to every syntax-highlighted code block on the site, with icon+"Copied" feedback on click.

**Architecture:** Pure client-side enhancement. A vanilla-JS function (added to the existing IIFE in `javascripts/main.js`) finds every Rouge-generated code block at page load and injects a button; matching SCSS rules in `_sass/base.scss` position and theme it. No Jekyll plugin, no build-pipeline changes.

**Tech Stack:** Vanilla JS (`navigator.clipboard` API), hand-written SCSS using the site's existing CSS custom properties. No new dependencies.

## Global Constraints

- Jekyll + GitHub Pages only — no custom plugins, no build-pipeline changes.
- No jQuery, no new icon libraries/fonts — icons are inline SVG.
- Button and all colors must be theme-aware via the site's existing CSS custom properties (`--color-border`, `--color-muted`, `--color-accent`, `--color-bg`) — no new hardcoded colors.
- Copies the code block's raw text only (`<code>` element's `textContent`) — no line numbers, prompts, or markup.
- If `navigator.clipboard` is unavailable, no button is injected for that block (no dead/broken UI).
- This is a static site with **no automated test suite** (consistent with the rest of the project) — verification is manual, via `bundle exec jekyll build`/`serve` plus curl/grep-based structural checks and, where noted, an actual browser check.
- The ambient shell's `$PATH` doesn't include `~/.rbenv/shims` by default — prefix `bundle exec` commands with `export PATH="$HOME/.rbenv/shims:$PATH"` (confirm with `ruby -v` → `3.3.6`).

---

### Task 1: Copy button — JS injection + SCSS styling

**Files:**
- Modify: `javascripts/main.js`
- Modify: `_sass/base.scss`

**Interfaces:**
- Consumes: Rouge's existing static output structure — each code block is wrapped as `<div class="language-xxx highlighter-rouge"><div class="highlight"><pre class="highlight"><code>...</code></pre></div></div>` (confirmed against this site's built output).
- Produces: `.copy-code-btn` (button element, injected as the first child of each `.highlighter-rouge` div) and `.copy-code-btn-label` (span for the "Copied" text) — self-contained, nothing later depends on these class names elsewhere in the codebase.

- [ ] **Step 1: Add the copy-button JS to `javascripts/main.js`**

Current file content (for reference — you are extending this, not replacing it):

```js
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
})();
```

Replace the entire file with this (adds the copy-button logic inside the same IIFE, after the mobile-nav block, before the closing `})();`):

```js
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
```

- [ ] **Step 2: Add copy-button styles to `_sass/base.scss`**

Current end of file (for reference — `.site-main` is the last rule):

```scss
.site-main {
  max-width: var(--content-width);
  margin: 0 auto;
  padding: 2.5rem 1.25rem 4rem;
}
```

Append these rules after it (do not modify anything above):

```scss

.highlighter-rouge {
  position: relative;
}

.copy-code-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  display: flex;
  align-items: center;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-bg);
  color: var(--color-muted);
  padding: 0.3rem 0.5rem;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.15s ease, color 0.15s ease, border-color 0.15s ease;
}

.highlighter-rouge:hover .copy-code-btn,
.copy-code-btn:focus-visible {
  opacity: 1;
}

.copy-code-btn:hover,
.copy-code-btn:focus-visible,
.copy-code-btn.is-copied {
  color: var(--color-accent);
  border-color: var(--color-accent);
}

.copy-code-btn svg {
  display: block;
}

.copy-code-btn-label {
  margin-left: 0.3em;
  font-size: 0.75rem;
}
```

- [ ] **Step 3: Build and verify structurally**

```bash
export PATH="$HOME/.rbenv/shims:$PATH"
bundle exec jekyll build
```

Expected: exits 0, no new warnings (the 2 pre-existing unrelated Liquid warnings about `{{.Architecture}}`/`{{.Os}}` in `_posts/2026-01-30-running-mcp-server.md` are expected and fine).

Then verify the SCSS compiled (the button itself is injected client-side by JS, so it will NOT appear in this static HTML — that's expected and is verified live in Step 4, not here):

```bash
grep -n "\.copy-code-btn" _site/stylesheets/main.css | head -5
```

Expected: shows the compiled `.copy-code-btn` rules referencing `var(--color-border)`, `var(--color-accent)`, etc.

- [ ] **Step 4: Verify live in a browser**

```bash
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000/calm-dsl` (or any post with a code block):
- Hover over a code block — a small button should fade in at the top-right corner.
- Tab to the button with keyboard focus (no mouse) — it should become visible via `:focus-visible` even without hovering.
- Click it — button should briefly show a checkmark + "Copied", then revert to the copy icon after ~1.5s.
- Paste the clipboard contents somewhere — confirm it's exactly the code text, no line numbers or extra whitespace.
- Toggle dark mode — confirm the button's border/icon color remains legible and theme-appropriate in both modes.
- Check a code block with long lines that horizontally scroll — confirm the button stays fixed in the top-right corner regardless of scroll position.
- Confirm no regression to existing code block styling — background color (light gray in light mode, dark in dark mode, per the earlier fix to `_sass/pygments-tomorrow.scss`) and syntax highlighting colors should look exactly as they did before this change.

Stop the server once verified.

- [ ] **Step 5: Commit**

```bash
git add javascripts/main.js _sass/base.scss
git commit -m "Add copy button to code blocks"
```

---
