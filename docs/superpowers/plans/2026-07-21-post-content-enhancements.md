# Post Content Enhancements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add hover-reveal heading anchor links and a click-to-enlarge image lightbox to post content.

**Architecture:** Both features are vanilla JS DOM enhancements appended to the existing IIFE in `javascripts/main.js` (same pattern as the existing `initCopyButtons`), with supporting CSS added to `_sass/base.scss`. No new files, no Liquid/layout changes, no dependencies.

**Tech Stack:** Plain JS (ES5-style, matching existing `main.js`), Sass (existing `_sass/base.scss`, uses CSS custom properties from `_sass/variables.scss`).

## Global Constraints

- Jekyll + GitHub Pages only — no build-pipeline changes.
- No new dependencies (no lightbox libraries, no icon fonts) — matches the site's existing vanilla-JS approach.
- This is a static site with **no automated test suite** — verification is manual, via `bundle exec jekyll build`/`serve`.
- The ambient shell's `$PATH` doesn't include `~/.rbenv/shims` by default — prefix `bundle exec` commands with `export PATH="$HOME/.rbenv/shims:$PATH"` (confirm with `ruby -v` → `3.3.6`).
- Selectors must be scoped to `.post-content` — anchors on `h2`/`h3` only, lightbox on all `img`, neither should affect `about.html`, `archive.html`, `tags.html`, or the post title (`h1`).

---

### Task 1: Heading anchor links

**Files:**
- Modify: `javascripts/main.js:65-66` (insert new function + call before the closing `})();`)
- Modify: `_sass/base.scss` (append new rules at end of file, after the existing `.copy-code-btn-label` block ending at line 130)

**Interfaces:**
- Produces: `.heading-anchor` CSS class (consumed only within this task — no dependency from Task 2).

- [ ] **Step 1: Add `initHeadingAnchors` to `javascripts/main.js`**

Insert immediately before the final `initCopyButtons();` call's closing `})();` — i.e. after line 65 (`initCopyButtons();`) and before line 66 (`})();`):

```js
  function initHeadingAnchors() {
    var headings = document.querySelectorAll('.post-content h2, .post-content h3');

    headings.forEach(function (heading) {
      if (!heading.id) return;

      var anchor = document.createElement('a');
      anchor.className = 'heading-anchor';
      anchor.href = '#' + heading.id;
      anchor.setAttribute('aria-label', 'Link to this section');
      anchor.textContent = '#';

      heading.insertBefore(anchor, heading.firstChild);
    });
  }

  initHeadingAnchors();
```

The full end of the file should read:

```js
  initCopyButtons();

  function initHeadingAnchors() {
    var headings = document.querySelectorAll('.post-content h2, .post-content h3');

    headings.forEach(function (heading) {
      if (!heading.id) return;

      var anchor = document.createElement('a');
      anchor.className = 'heading-anchor';
      anchor.href = '#' + heading.id;
      anchor.setAttribute('aria-label', 'Link to this section');
      anchor.textContent = '#';

      heading.insertBefore(anchor, heading.firstChild);
    });
  }

  initHeadingAnchors();
})();
```

- [ ] **Step 2: Append heading-anchor CSS to `_sass/base.scss`**

Append at the end of the file (after the existing `.copy-code-btn-label` rule):

```scss
.post-content h2,
.post-content h3 {
  position: relative;
}

.heading-anchor {
  position: absolute;
  left: -1.1em;
  color: var(--color-muted);
  text-decoration: none;
  opacity: 0;
  transition: opacity 0.15s ease, color 0.15s ease;
}

.post-content h2:hover .heading-anchor,
.post-content h3:hover .heading-anchor,
.heading-anchor:focus-visible {
  opacity: 1;
}

.heading-anchor:hover,
.heading-anchor:focus-visible {
  color: var(--color-accent);
}
```

- [ ] **Step 3: Build and verify heading IDs + anchor markup**

```bash
export PATH="$HOME/.rbenv/shims:$PATH"
bundle exec jekyll build
```

Expected: exits 0, no new warnings (the 2 pre-existing unrelated Liquid warnings in `_posts/2026-01-30-running-mcp-server.md` are expected and fine).

```bash
grep -o 'id="[a-z0-9-]*"' _site/connect-remote-mcp-to-nai.html | head -3
```

Expected: at least one `id="..."` match (confirms kramdown still emits heading IDs — the JS depends on this at runtime, this step just confirms the precondition still holds, since the anchor insertion itself happens client-side and won't appear in the static HTML).

- [ ] **Step 4: Manually verify anchor behavior in the browser**

```bash
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000/connect-remote-mcp-to-nai.html`. Hover over an `h2`/`h3` heading — confirm a `#` fades in to the left. Click it — confirm the URL gains `#<heading-id>` and the page stays scrolled at that heading. Reload the page with that `#heading-id` still in the URL — confirm the browser lands at the right heading on load. Confirm `about.html` has no anchors — its `h2`/`h3` headings are raw HTML with no kramdown-generated `id` — the anchors JS skips headings without an `id`, so nothing renders even though the `.post-content h2, h3` selector technically matches them.

Stop the server once verified.

- [ ] **Step 5: Commit**

```bash
git add javascripts/main.js _sass/base.scss
git commit -m "Add hover-reveal anchor links to post headings"
```

---

### Task 2: Image lightbox

**Files:**
- Modify: `javascripts/main.js` (insert new function + call before the closing `})();`, after Task 1's additions)
- Modify: `_sass/base.scss` (append new rules at end of file, after Task 1's additions)

**Interfaces:**
- Consumes: nothing from Task 1 (independent DOM scan/feature, just lives in the same shared file).
- Produces: `.image-lightbox` CSS class and DOM element, created/destroyed at runtime only (not present in static build output).

- [ ] **Step 1: Add `initImageLightbox` to `javascripts/main.js`**

Insert after Task 1's `initHeadingAnchors();` call and before the final `})();`:

```js
  function initImageLightbox() {
    var images = document.querySelectorAll('.post-content img');
    if (!images.length) return;

    var overlay = null;

    function onKeydown(event) {
      if (event.key === 'Escape') closeOverlay();
    }

    function closeOverlay() {
      if (!overlay) return;
      overlay.remove();
      overlay = null;
      document.removeEventListener('keydown', onKeydown);
    }

    function openOverlay(src, alt) {
      overlay = document.createElement('div');
      overlay.className = 'image-lightbox';

      var img = document.createElement('img');
      img.src = src;
      img.alt = alt;

      overlay.appendChild(img);
      overlay.addEventListener('click', closeOverlay);
      document.body.appendChild(overlay);
      document.addEventListener('keydown', onKeydown);
    }

    images.forEach(function (image) {
      image.addEventListener('click', function () {
        openOverlay(image.src, image.alt);
      });
    });
  }

  initImageLightbox();
```

The full end of the file should read:

```js
  initHeadingAnchors();

  function initImageLightbox() {
    var images = document.querySelectorAll('.post-content img');
    if (!images.length) return;

    var overlay = null;

    function onKeydown(event) {
      if (event.key === 'Escape') closeOverlay();
    }

    function closeOverlay() {
      if (!overlay) return;
      overlay.remove();
      overlay = null;
      document.removeEventListener('keydown', onKeydown);
    }

    function openOverlay(src, alt) {
      overlay = document.createElement('div');
      overlay.className = 'image-lightbox';

      var img = document.createElement('img');
      img.src = src;
      img.alt = alt;

      overlay.appendChild(img);
      overlay.addEventListener('click', closeOverlay);
      document.body.appendChild(overlay);
      document.addEventListener('keydown', onKeydown);
    }

    images.forEach(function (image) {
      image.addEventListener('click', function () {
        openOverlay(image.src, image.alt);
      });
    });
  }

  initImageLightbox();
})();
```

- [ ] **Step 2: Append lightbox CSS to `_sass/base.scss`**

Append at the end of the file (after Task 1's `.heading-anchor` rules):

```scss
.post-content img {
  cursor: zoom-in;
}

.image-lightbox {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.85);
  z-index: 100;
  cursor: zoom-out;
}

.image-lightbox img {
  max-width: 90vw;
  max-height: 90vh;
}
```

- [ ] **Step 3: Build and verify**

```bash
export PATH="$HOME/.rbenv/shims:$PATH"
bundle exec jekyll build
```

Expected: exits 0, no new warnings (same 2 pre-existing unrelated warnings as before).

Use a post that has an image in its body for browser verification — check which posts have images:

```bash
grep -rl '!\[' _posts/*.md
```

- [ ] **Step 4: Manually verify lightbox behavior in the browser**

```bash
bundle exec jekyll serve
```

Open one of the posts found in Step 3 that contains an image. Hover over the image — confirm the cursor changes to zoom-in. Click it — confirm a fullscreen dark overlay appears with the image enlarged and centered, not exceeding the viewport. Click anywhere on the overlay (including on the enlarged image itself) — confirm it closes. Reopen it, then press `Esc` — confirm it closes. Toggle dark mode (theme button in nav) and repeat — confirm the image stays legible against the scrim in both themes. Confirm `about.html` (no images in `.post-content` there) is unaffected.

Stop the server once verified.

- [ ] **Step 5: Commit**

```bash
git add javascripts/main.js _sass/base.scss
git commit -m "Add click-to-enlarge lightbox for post images"
```

---
