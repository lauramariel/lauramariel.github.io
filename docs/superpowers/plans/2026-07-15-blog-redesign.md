# Blog Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the unmaintained Shiori/Bootstrap Jekyll theme with a clean-minimal, IBM Plex Sans, coral-accented design with dark mode, restructure navigation (Home/Notes/Tags/About), and clean up post front matter — while staying on Jekyll + GitHub Pages with no build pipeline changes.

**Architecture:** Static Jekyll site. Replace `_sass`/`stylesheets` (drop Bootstrap, add hand-written SCSS partials wired through CSS custom properties for light/dark theming), replace `_layouts`/`_includes` (single unified `default.html`, no sidebar), rewrite `index.html`/`archive.html`/add `tags.html`/rewrite `about.html`, and add front matter (`tags:`) to existing posts. One new shared Liquid include (`post-list-item.html`) renders a post row and is reused by home, Notes, and Tags pages.

**Tech Stack:** Jekyll (via `github-pages` gem), Sass/SCSS, vanilla JS (no jQuery/Bootstrap), Liquid templating, Rouge syntax highlighting.

## Global Constraints

- Stay on Jekyll + GitHub Pages — no CI/build pipeline changes, same deploy-on-push workflow.
- No jQuery, Bootstrap CSS/JS, or `purplecoat.js` in the final site.
- Typeface: IBM Plex Sans. Accent color: coral (`#d6552f` light / `#ff8b66` dark). Manual dark-mode toggle, `localStorage`-backed, defaulting to system preference on first visit.
- Code blocks use adaptive (light/dark) syntax highlighting, not a fixed theme.
- Nav: Home, Notes, Tags, About (in that order), plus GitHub/LinkedIn/RSS icons and the theme toggle.
- No placeholder content — About page must contain the real, existing bio/links content relocated from the current homepage.

---

### Task 1: Local Ruby toolchain — install and verify baseline build

The system Ruby (2.6.10) is too old for the locked `github-pages` gem (needs Ruby ≥ 3.1). Set up `rbenv` with a modern Ruby scoped to this project, confirm `bundle install` and `bundle exec jekyll serve` work against the **current, unmodified** site before touching any code — this is the safety net for every later task.

**Files:**
- Create: `.ruby-version` (repo root)

**Interfaces:**
- Produces: a working local `bundle exec jekyll serve` command every later task's verification step relies on.

- [ ] **Step 1: Install rbenv and ruby-build via Homebrew**

```bash
brew install rbenv ruby-build
```

- [ ] **Step 2: Hook rbenv into the shell**

```bash
rbenv init
```

This prints the exact line to add to your shell profile (e.g. `~/.bash_profile` for bash). Add that line, then reload:

```bash
source ~/.bash_profile
```

- [ ] **Step 3: Install Ruby 3.3.6 and pin it to this project**

```bash
rbenv install 3.3.6
rbenv local 3.3.6
```

This creates `.ruby-version` in the repo root containing `3.3.6`.

- [ ] **Step 4: Verify the pinned Ruby is active**

Run: `ruby -v`
Expected: output contains `3.3.6`

- [ ] **Step 5: Install bundler and project gems**

```bash
gem install bundler
bundle install
```

Expected: completes without the "Ruby >= 3.1.0" resolution error seen previously. If `Gemfile.lock` changes as a result, that's expected (it was locked against an unresolvable dependency graph).

- [ ] **Step 6: Verify the current (unmodified) site builds and serves**

```bash
bundle exec jekyll serve
```

Expected: starts without errors, prints `Server address: http://127.0.0.1:4000`. Open it in a browser and confirm the existing (old Shiori-themed) homepage loads. Stop the server (Ctrl-C) once confirmed.

- [ ] **Step 7: Commit the Ruby version pin**

```bash
git add .ruby-version Gemfile.lock
git commit -m "Pin project Ruby version to 3.3.6 via rbenv"
```

(If `Gemfile.lock` had no changes, only add `.ruby-version`.)

---

### Task 2: Remove Shiori/Bootstrap theme, add base layout foundation

Delete the old theme, framework JS, and dead includes/layouts. Replace them with a single unified `_layouts/default.html`, a new nav/footer structure, and a fresh SCSS foundation (CSS custom properties for the light/dark palette, reset, typography, IBM Plex Sans). This task leaves the site building and navigable, in the new Clean Minimal style, even though page-specific content (home/notes/tags/about) isn't rewritten yet — that's later tasks.

**Files:**
- Delete: `_sass/bootstrap-sass/` (entire directory), `_sass/custom-bootstrap-variables.scss`, `_sass/custom-scss.scss`, `stylesheets/shiori.scss`, `stylesheets/shiori-original.scss`, `javascripts/jquery.min.js`, `javascripts/bootstrap.min.js`, `javascripts/purplecoat-min.js`, `_includes/ribbon.html`, `_includes/nav-mobile.html`, `_includes/sidebar.html`, `_includes/post-header.html`, `_includes/post-header-home.html`, `_includes/post-footer.html`, `_layouts/default_without_sidebar.html`, `_layouts/index.html`, `blog.html`
- Create: `stylesheets/main.scss`, `_sass/variables.scss`, `_sass/base.scss`, `_sass/nav.scss`, `_sass/footer.scss`
- Rename: `_sass/pygments-tomorrow.scss` → keep as-is (imported by `main.scss`, no content change in this task)
- Modify: `_layouts/default.html` (full rewrite), `_includes/nav.html` (full rewrite), `_includes/nav-right.html` (full rewrite), `_includes/footer.html` (full rewrite), `_data/theme.yml` (simplify), `_config.yml` (no change needed — `defaults` already points pages at `layout: default`)
- Modify: `index.html` (only its front matter — remove `layout: index`, content stays as-is for now, rewritten in Task 6)

**Interfaces:**
- Produces: CSS custom properties `--color-bg`, `--color-fg`, `--color-muted`, `--color-border`, `--color-accent`, `--color-code-bg`, `--font-sans`, `--content-width`, overridden under `[data-theme="dark"]`. Later tasks (dark mode, syntax highlighting, page content) style against these variables.
- Produces: `.site-main` wrapper class (max-width content column) that all page content renders inside via `{{ content }}` in `default.html`.
- Produces: nav markup with `id="nav-links"` and `.nav-toggle` button, consumed by Task 3's mobile-menu JS.
- Produces: `#theme-toggle` button in `_includes/nav-right.html`, consumed by Task 3's dark-mode JS.

- [ ] **Step 1: Delete the old theme files**

```bash
git rm -r _sass/bootstrap-sass
git rm _sass/custom-bootstrap-variables.scss _sass/custom-scss.scss
git rm stylesheets/shiori.scss stylesheets/shiori-original.scss
git rm javascripts/jquery.min.js javascripts/bootstrap.min.js javascripts/purplecoat-min.js
git rm _includes/ribbon.html _includes/nav-mobile.html _includes/sidebar.html
git rm _includes/post-header.html _includes/post-header-home.html _includes/post-footer.html
git rm _layouts/default_without_sidebar.html _layouts/index.html
git rm blog.html
```

- [ ] **Step 2: Create `_sass/variables.scss`**

```scss
:root {
  --color-bg: #ffffff;
  --color-fg: #1a1a1a;
  --color-muted: #6b6b6b;
  --color-border: #e6e6e6;
  --color-accent: #d6552f;
  --color-code-bg: #f6f6f6;
  --font-sans: "IBM Plex Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --content-width: 42rem;
}

[data-theme="dark"] {
  --color-bg: #16181d;
  --color-fg: #e8e8e6;
  --color-muted: #9a9a95;
  --color-border: #2c2f36;
  --color-accent: #ff8b66;
  --color-code-bg: #1d1f21;
}
```

- [ ] **Step 3: Create `_sass/base.scss`**

```scss
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: var(--font-sans);
  font-size: 17px;
  line-height: 1.6;
  color: var(--color-fg);
  background: var(--color-bg);
  transition: background-color 0.15s ease, color 0.15s ease;
}

h1, h2, h3, h4 {
  font-weight: 600;
  line-height: 1.3;
  margin: 1.6em 0 0.5em;
}

h1 { font-size: 1.9rem; }
h2 { font-size: 1.4rem; }
h3 { font-size: 1.15rem; }

p, ul, ol, blockquote, table {
  margin: 0 0 1em;
}

a {
  color: var(--color-accent);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

blockquote {
  border-left: 3px solid var(--color-border);
  margin-left: 0;
  padding-left: 1em;
  color: var(--color-muted);
}

code {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  font-size: 0.9em;
  background: var(--color-code-bg);
  padding: 0.15em 0.35em;
  border-radius: 3px;
}

pre {
  background: var(--color-code-bg);
  padding: 1em;
  border-radius: 6px;
  overflow-x: auto;
}

pre code {
  background: none;
  padding: 0;
}

img {
  max-width: 100%;
  height: auto;
}

table {
  border-collapse: collapse;
  width: 100%;
}

th, td {
  border: 1px solid var(--color-border);
  padding: 0.5em 0.75em;
  text-align: left;
}

th {
  background: var(--color-code-bg);
}

.site-main {
  max-width: var(--content-width);
  margin: 0 auto;
  padding: 2.5rem 1.25rem 4rem;
}
```

- [ ] **Step 4: Create `_sass/nav.scss`**

```scss
.site-nav {
  border-bottom: 1px solid var(--color-border);
}

.site-nav-inner {
  max-width: var(--content-width);
  margin: 0 auto;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

.site-brand {
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--color-fg);
}

.site-brand:hover {
  text-decoration: none;
}

.nav-toggle {
  display: none;
  flex-direction: column;
  gap: 4px;
  background: none;
  border: 0;
  cursor: pointer;
  padding: 0.5rem;
}

.nav-toggle span {
  width: 20px;
  height: 2px;
  background: var(--color-fg);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.nav-list {
  list-style: none;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  margin: 0;
  padding: 0;
}

.nav-list a {
  color: var(--color-fg);
  font-size: 0.95rem;
}

.nav-list a:hover {
  color: var(--color-accent);
  text-decoration: none;
}

.icon-link {
  font-size: 1.1rem;
  line-height: 1;
}

.theme-toggle {
  background: none;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
  color: var(--color-fg);
  font-size: 0.95rem;
  line-height: 1;
}

@media (max-width: 640px) {
  .nav-toggle {
    display: flex;
  }

  .nav-links {
    display: none;
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
    margin-top: 1rem;
  }

  .nav-links.is-open {
    display: flex;
  }

  .nav-list {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
}
```

- [ ] **Step 5: Create `_sass/footer.scss`**

```scss
.site-footer {
  max-width: var(--content-width);
  margin: 3rem auto 0;
  padding: 1.5rem 1.25rem 2.5rem;
  border-top: 1px solid var(--color-border);
  color: var(--color-muted);
  font-size: 0.85rem;
  text-align: center;
}

.site-footer a {
  color: var(--color-muted);
}

.site-footer a:hover {
  color: var(--color-accent);
}
```

- [ ] **Step 6: Create `stylesheets/main.scss`**

```scss
---
---

@import "variables";
@import "base";
@import "nav";
@import "footer";
@import "pygments-tomorrow";
```

- [ ] **Step 7: Rewrite `_layouts/default.html`**

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="{{ "/stylesheets/main.css" | prepend: site.baseurl }}">
    <link href="//fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="canonical" href="{{ page.url | replace: 'index.html','' | prepend: site.baseurl | prepend: site.url }}">
    <link rel="shortcut icon" href="{{ "/favicon.ico" | prepend: site.baseurl }}">
    <link rel="alternate" type="application/rss+xml" title="{{ site.title }}" href="{{ "/feed.xml" | prepend: site.baseurl | prepend: site.url }}">
    <title>{% if page.title %}{{ page.title }} | {% endif %}{{ site.title }}</title>
    <script>
      (function () {
        var stored = localStorage.getItem('theme');
        var theme = stored || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        document.documentElement.setAttribute('data-theme', theme);
      })();
    </script>
    {% include head.html %}
  </head>
  <body>
    <header class="site-nav">
      <div class="site-nav-inner">
        <a href="{{ "/" | prepend: site.baseurl }}" class="site-brand">{{ site.title }}</a>
        <button type="button" class="nav-toggle" aria-controls="nav-links" aria-expanded="false" aria-label="Toggle navigation">
          <span></span><span></span><span></span>
        </button>
        <nav id="nav-links" class="nav-links">
          <ul class="nav-list">
            {% include nav.html %}
          </ul>
          <ul class="nav-list nav-list-right">
            {% include nav-right.html %}
          </ul>
        </nav>
      </div>
    </header>
    <main class="site-main">
      {{ content }}
    </main>
    <footer class="site-footer">
      {% include footer.html %}
    </footer>
    <script src="https://kit.fontawesome.com/7c5e474110.js" crossorigin="anonymous"></script>
    <script src="{{ "/javascripts/main.js" | prepend: site.baseurl }}"></script>
    {% include scripts.html %}
  </body>
</html>
```

- [ ] **Step 8: Rewrite `_includes/nav.html`**

```html
<li><a href="{{ "/" | prepend: site.baseurl }}">Home</a></li>
<li><a href="{{ "/archive" | prepend: site.baseurl }}">Notes</a></li>
<li><a href="{{ "/tags" | prepend: site.baseurl }}">Tags</a></li>
<li><a href="{{ "/about" | prepend: site.baseurl }}">About</a></li>
```

- [ ] **Step 9: Rewrite `_includes/nav-right.html`**

```html
<li><a class="icon-link" href="https://github.com/lauramariel" target="_blank" rel="noopener" aria-label="GitHub"><i class="fab fa-github"></i></a></li>
<li><a class="icon-link" href="https://linkedin.com/in/laurajordana" target="_blank" rel="noopener" aria-label="LinkedIn"><i class="fab fa-linkedin"></i></a></li>
<li><a class="icon-link" href="{{ "/feed.xml" | prepend: site.baseurl }}" aria-label="RSS feed"><i class="fas fa-rss"></i></a></li>
<li>
  <button id="theme-toggle" class="theme-toggle" type="button" aria-pressed="false" aria-label="Toggle dark mode">
    <span class="theme-toggle-icon" aria-hidden="true">&#9788;</span>
  </button>
</li>
```

- [ ] **Step 10: Rewrite `_includes/footer.html`**

```html
<p>&copy; {{ site.time | date: "%Y" }} {{ site.title }}. Built with <a href="https://jekyllrb.com/">Jekyll</a>.</p>
```

- [ ] **Step 11: Simplify `_data/theme.yml`**

```yaml
# Theme customization is done on this file instead of _config.yml so that
# you don't have to restart Jekyll to see changes.

# Number of posts displayed on the home page.
num_home_posts: 3

# Show navigation (older/newer) below each post?
show_post_navs: true
```

- [ ] **Step 12: Update `index.html` front matter only**

Change the top of `index.html` from:

```
---
layout: index
---
```

to:

```
---
layout: default
---
```

(Leave the rest of `index.html`'s content untouched — it's fully rewritten in Task 6.)

- [ ] **Step 13: Create placeholder `javascripts/main.js` (filled in Task 3)**

```js
// Mobile nav toggle and dark-mode toggle are wired up in Task 3.
```

- [ ] **Step 14: Build and verify**

```bash
bundle exec jekyll build
```

Expected: builds without errors (Liquid include errors would appear here if any deleted include is still referenced — there should be none left).

```bash
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000` and confirm: page loads with new nav (Home/Notes/Tags/About + icons + toggle button, unstyled toggle behavior is fine — JS comes in Task 3), IBM Plex Sans font renders, no Bootstrap styling remains, no browser console errors about missing JS/CSS files. Stop the server.

- [ ] **Step 15: Commit**

```bash
git add -A
git commit -m "Replace Shiori/Bootstrap theme with base Clean Minimal layout"
```

---

### Task 3: Dark mode toggle and mobile nav JS

Wire up the `#theme-toggle` button and `.nav-toggle` hamburger button created in Task 2. The inline script in `default.html`'s `<head>` already sets the initial `data-theme` attribute before paint (avoiding a flash of the wrong theme); this task adds the click handlers.

**Files:**
- Modify: `javascripts/main.js` (replace placeholder from Task 2)

**Interfaces:**
- Consumes: `#theme-toggle` button and `#nav-links`/`.nav-toggle` elements from `_layouts/default.html` (Task 2).
- Consumes: CSS variables under `[data-theme="dark"]` from `_sass/variables.scss` (Task 2).

- [ ] **Step 1: Write `javascripts/main.js`**

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

- [ ] **Step 2: Manually verify in the browser**

```bash
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000`. Click the theme toggle button — confirm the background/text/border colors flip (via the CSS variables from Task 2) and the change persists after a page reload (check `localStorage.getItem('theme')` in devtools console, or just reload and confirm it stayed). Narrow the browser window below 640px width and confirm the hamburger button appears and toggles the nav list open/closed. Stop the server.

- [ ] **Step 3: Commit**

```bash
git add javascripts/main.js
git commit -m "Wire up dark-mode toggle and mobile nav JS"
```

---

### Task 4: Adaptive (light/dark) syntax highlighting

Many posts are command-line cheat sheets with heavy code content. Add a dark variant of the existing Tomorrow-theme Rouge/Pygments CSS, scoped under `[data-theme="dark"]`, so code blocks re-theme along with the rest of the page instead of staying a fixed light box.

**Files:**
- Create: `_sass/syntax-dark.scss`
- Modify: `stylesheets/main.scss` (add the new import)

**Interfaces:**
- Consumes: the `[data-theme="dark"]` attribute set by Task 3's JS / Task 2's inline head script.
- Consumes: the same Rouge CSS class names (`.highlight .c`, `.highlight .k`, etc.) already used by `_sass/pygments-tomorrow.scss`.

- [ ] **Step 1: Create `_sass/syntax-dark.scss`** (Tomorrow Night palette, mirroring every selector in `_sass/pygments-tomorrow.scss`)

```scss
[data-theme="dark"] .highlight .hll { background-color: #373b41 }
[data-theme="dark"] .highlight { background: #1d1f21; color: #c5c8c6 }
[data-theme="dark"] .highlight .c { color: #969896 }
[data-theme="dark"] .highlight .err { color: #cc6666 }
[data-theme="dark"] .highlight .k { color: #b294bb }
[data-theme="dark"] .highlight .l { color: #de935f }
[data-theme="dark"] .highlight .n { color: #c5c8c6 }
[data-theme="dark"] .highlight .o { color: #8abeb7 }
[data-theme="dark"] .highlight .p { color: #c5c8c6 }
[data-theme="dark"] .highlight .cm { color: #969896 }
[data-theme="dark"] .highlight .cp { color: #969896 }
[data-theme="dark"] .highlight .c1 { color: #969896 }
[data-theme="dark"] .highlight .cs { color: #969896 }
[data-theme="dark"] .highlight .gd { color: #cc6666 }
[data-theme="dark"] .highlight .ge { font-style: italic }
[data-theme="dark"] .highlight .gh { color: #c5c8c6; font-weight: bold }
[data-theme="dark"] .highlight .gi { color: #b5bd68 }
[data-theme="dark"] .highlight .gp { color: #969896; font-weight: bold }
[data-theme="dark"] .highlight .gs { font-weight: bold }
[data-theme="dark"] .highlight .gu { color: #8abeb7; font-weight: bold }
[data-theme="dark"] .highlight .kc { color: #b294bb }
[data-theme="dark"] .highlight .kd { color: #b294bb }
[data-theme="dark"] .highlight .kn { color: #8abeb7 }
[data-theme="dark"] .highlight .kp { color: #b294bb }
[data-theme="dark"] .highlight .kr { color: #b294bb }
[data-theme="dark"] .highlight .kt { color: #f0c674 }
[data-theme="dark"] .highlight .ld { color: #b5bd68 }
[data-theme="dark"] .highlight .m { color: #de935f }
[data-theme="dark"] .highlight .s { color: #b5bd68 }
[data-theme="dark"] .highlight .na { color: #81a2be }
[data-theme="dark"] .highlight .nb { color: #c5c8c6 }
[data-theme="dark"] .highlight .nc { color: #f0c674 }
[data-theme="dark"] .highlight .no { color: #cc6666 }
[data-theme="dark"] .highlight .nd { color: #8abeb7 }
[data-theme="dark"] .highlight .ni { color: #c5c8c6 }
[data-theme="dark"] .highlight .ne { color: #cc6666 }
[data-theme="dark"] .highlight .nf { color: #81a2be }
[data-theme="dark"] .highlight .nl { color: #c5c8c6 }
[data-theme="dark"] .highlight .nn { color: #f0c674 }
[data-theme="dark"] .highlight .nx { color: #81a2be }
[data-theme="dark"] .highlight .py { color: #c5c8c6 }
[data-theme="dark"] .highlight .nt { color: #8abeb7 }
[data-theme="dark"] .highlight .nv { color: #cc6666 }
[data-theme="dark"] .highlight .ow { color: #8abeb7 }
[data-theme="dark"] .highlight .w { color: #c5c8c6 }
[data-theme="dark"] .highlight .mf { color: #de935f }
[data-theme="dark"] .highlight .mh { color: #de935f }
[data-theme="dark"] .highlight .mi { color: #de935f }
[data-theme="dark"] .highlight .mo { color: #de935f }
[data-theme="dark"] .highlight .sb { color: #b5bd68 }
[data-theme="dark"] .highlight .sc { color: #c5c8c6 }
[data-theme="dark"] .highlight .sd { color: #969896 }
[data-theme="dark"] .highlight .s2 { color: #b5bd68 }
[data-theme="dark"] .highlight .se { color: #de935f }
[data-theme="dark"] .highlight .sh { color: #b5bd68 }
[data-theme="dark"] .highlight .si { color: #de935f }
[data-theme="dark"] .highlight .sx { color: #b5bd68 }
[data-theme="dark"] .highlight .sr { color: #b5bd68 }
[data-theme="dark"] .highlight .s1 { color: #b5bd68 }
[data-theme="dark"] .highlight .ss { color: #b5bd68 }
[data-theme="dark"] .highlight .bp { color: #c5c8c6 }
[data-theme="dark"] .highlight .vc { color: #cc6666 }
[data-theme="dark"] .highlight .vg { color: #cc6666 }
[data-theme="dark"] .highlight .vi { color: #cc6666 }
[data-theme="dark"] .highlight .il { color: #de935f }
```

- [ ] **Step 2: Add the import to `stylesheets/main.scss`**

```scss
---
---

@import "variables";
@import "base";
@import "nav";
@import "footer";
@import "pygments-tomorrow";
@import "syntax-dark";
```

- [ ] **Step 3: Verify against a real post**

```bash
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000/setting-up-github-repo-access-with-custom-ssh-configs/` (or any post with a fenced code block, e.g. `calm-dsl-v4-2-0-cheat-sheet`). Confirm the code block has a light background matching the page in light mode. Click the dark-mode toggle and confirm the code block switches to the dark Tomorrow Night palette. Stop the server.

- [ ] **Step 4: Commit**

```bash
git add _sass/syntax-dark.scss stylesheets/main.scss
git commit -m "Add adaptive light/dark syntax highlighting for code blocks"
```

---

### Task 5: Shared post-list partial + front matter tags cleanup

Add the `post-list-item.html` include that Home, Notes, and Tags pages will all reuse (title + date + estimated read time), and fix post front matter so tags actually work: convert the malformed `categories: a, b, c` string on each post to a proper `tags: [a, b, c]` list.

**Files:**
- Create: `_includes/post-list-item.html`
- Modify: `_sass/posts.scss` (new file, styles for `.post-list-item` and friends — used by Tasks 6/7/8 too)
- Modify: `stylesheets/main.scss` (add the `posts` import)
- Modify: all 10 real posts under `_posts/` (front matter only)

**Interfaces:**
- Produces: `{% include post-list-item.html post=post %}` — renders one post row given a Liquid post object in `include.post`. Consumed by Task 6 (Home), Task 7 (Notes), Task 8 (Tags).
- Produces: `tags:` front matter array on every real post, consumed by Task 8 (Tags page) and the post page tag pills (Task 9).

- [ ] **Step 1: Create `_includes/post-list-item.html`**

```html
<div class="post-list-item">
  <h2 class="post-list-title"><a href="{{ include.post.url | prepend: site.baseurl }}">{{ include.post.title }}</a></h2>
  <p class="post-list-meta">
    {{ include.post.date | date: "%b %-d, %Y" }}
    {% assign words = include.post.content | strip_html | number_of_words %}
    {% assign read_time = words | divided_by: 200 | plus: 1 %}
    &middot; {{ read_time }} min read
  </p>
</div>
```

- [ ] **Step 2: Create `_sass/posts.scss`**

```scss
.home-intro {
  color: var(--color-muted);
  margin-bottom: 2rem;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.post-list-item {
  padding-bottom: 1.75rem;
  border-bottom: 1px solid var(--color-border);
}

.post-list-item:last-child {
  border-bottom: none;
}

.post-list-title {
  margin: 0 0 0.25rem;
  font-size: 1.15rem;
}

.post-list-title a {
  color: var(--color-fg);
}

.post-list-title a:hover {
  color: var(--color-accent);
}

.post-list-meta {
  margin: 0;
  font-size: 0.85rem;
  color: var(--color-muted);
}

.home-more {
  margin-top: 1rem;
}

.archive-heading {
  margin-top: 2.5rem;
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-muted);
}

.tag-heading {
  margin-top: 2.5rem;
  font-size: 1.1rem;
}
```

- [ ] **Step 3: Add the import to `stylesheets/main.scss`**

```scss
---
---

@import "variables";
@import "base";
@import "nav";
@import "posts";
@import "footer";
@import "pygments-tomorrow";
@import "syntax-dark";
```

- [ ] **Step 4: Fix front matter on all 10 real posts**

For each file below, replace the `categories:` line with a `tags:` line as shown.

`_posts/2021-08-04-pc-2021-7-new-xplay-actions.md`:
```
categories: aiops, automation, prism ops, nutanix
```
→
```
tags: [aiops, automation, "prism ops", nutanix]
```

`_posts/2021-11-03-test-drive-prism-ops.md`:
```
categories: aiops, automation, prism ops, nutanix
```
→
```
tags: [aiops, automation, "prism ops", nutanix]
```

`_posts/2023-12-08-mac-sonoma-finder-icons.md`:
```
categories: mac, workstation
```
→
```
tags: [mac, workstation]
```

`_posts/2025-04-10-importing-custom-model.md`:
```
categories: nutanix, genai
```
→
```
tags: [nutanix, genai]
```

`_posts/2025-08-28-calm-dsl.md`:
```
categories: calm, dsl, ncm
```
→
```
tags: [calm, dsl, ncm]
```

`_posts/2025-08-28-git-custom-ssh.md`:
```
categories: github, git, ssh
```
→
```
tags: [github, git, ssh]
```

`_posts/2025-09-25-acme.md`:
```
categories: web, certs, security
```
→
```
tags: [web, certs, security]
```

`_posts/2025-11-13-add-disk-to-rocky.md`:
```
categories: linux, storage
```
→
```
tags: [linux, storage]
```

`_posts/2026-01-05-export-pdfs-from-vuepress-site.md`:
```
categories: vuepress, javascript
```
→
```
tags: [vuepress, javascript]
```

`_posts/2026-01-30-running-mcp-server.md`:
```
categories: ai, mcp, genai
```
→
```
tags: [ai, mcp, genai]
```

- [ ] **Step 5: Build and verify front matter parses cleanly**

```bash
bundle exec jekyll build
```

Expected: exits 0, no YAML parse errors or "Invalid Date" errors (a stray unquoted `:` or bad list syntax in the `tags:` edits would fail the build here). Full verification that tags group posts correctly happens visually in Task 8, once the Tags page exists to render `site.tags`.

- [ ] **Step 6: Commit**

```bash
git add _includes/post-list-item.html _sass/posts.scss stylesheets/main.scss _posts/
git commit -m "Add shared post-list partial and fix post tags front matter"
```

---

### Task 6: Homepage rewrite

Replace the hardcoded videos/talks/blog-links homepage with a tagline + recent posts list, using the `post-list-item.html` partial from Task 5.

**Files:**
- Modify: `index.html` (full content rewrite, front matter already set to `layout: default` in Task 2)

**Interfaces:**
- Consumes: `{% include post-list-item.html post=post %}` from Task 5.
- Consumes: `site.data.theme.num_home_posts` from `_data/theme.yml` (Task 2).

- [ ] **Step 1: Rewrite `index.html`**

```html
---
layout: default
---
<p class="home-intro">Notes on infrastructure, automation, and whatever else I run into.</p>
<div class="post-list">
{% for post in site.posts limit: site.data.theme.num_home_posts %}
  {% if post.render != false %}
    {% include post-list-item.html post=post %}
  {% endif %}
{% endfor %}
</div>
<p class="home-more"><a href="{{ "/archive" | prepend: site.baseurl }}">View all notes &rarr;</a></p>
```

- [ ] **Step 2: Verify in the browser**

```bash
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000`. Confirm: tagline shows above the post list, 3 most recent posts render (title, date, read time), "View all notes →" links to `/archive`, no leftover video/talk/blog links remain on the homepage. Stop the server.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "Rewrite homepage as tagline + recent posts list"
```

---

### Task 7: Notes page (renamed Archive) restyle

Restyle `archive.html` to use the shared post-list partial while keeping its existing month/year grouping logic. URL stays `/archive` — only the nav label changed to "Notes" (already done in Task 2).

**Files:**
- Modify: `archive.html`

**Interfaces:**
- Consumes: `{% include post-list-item.html post=post %}` from Task 5.

- [ ] **Step 1: Rewrite `archive.html`**

```html
---
title: Notes
permalink: "archive/index.html"
layout: page
---
<div class="page-archive">
{% for post in site.posts %}
  {% if post.render != false %}
    {% assign post_month_year = post.date | date: "%B %Y" %}
    {% assign newer_post_month_year = post.next.date | date: "%B %Y" %}
    {% if post_month_year != newer_post_month_year %}
      <h2 class="archive-heading">{{ post_month_year }}</h2>
    {% endif %}
    {% include post-list-item.html post=post %}
  {% endif %}
{% endfor %}
</div>
```

- [ ] **Step 2: Verify in the browser**

```bash
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000/archive`. Confirm: page title reads "Notes", posts are grouped under month/year headings in chronological order (newest first, matching current behavior), each row shows title/date/read-time via the shared partial. Stop the server.

- [ ] **Step 3: Commit**

```bash
git add archive.html
git commit -m "Restyle Notes (archive) page with shared post-list partial"
```

---

### Task 8: Tags page

New page grouping posts by tag, using the `tags:` front matter added in Task 5.

**Files:**
- Create: `tags.html`

**Interfaces:**
- Consumes: `site.tags` (built-in Jekyll data from each post's `tags:` front matter) and `{% include post-list-item.html post=post %}` from Task 5.
- Produces: anchor targets `#<slugified-tag-name>` that post pages' tag pills (Task 9) link to.

- [ ] **Step 1: Create `tags.html`**

```html
---
title: Tags
permalink: "tags/index.html"
layout: page
---
{% assign tags = site.tags | sort %}
<div class="tags-page">
{% for tag in tags %}
  {% assign tag_name = tag[0] %}
  {% assign tag_posts = tag[1] %}
  <h2 id="{{ tag_name | slugify }}" class="tag-heading">{{ tag_name }}</h2>
  <div class="post-list">
    {% for post in tag_posts %}
      {% if post.render != false %}
        {% include post-list-item.html post=post %}
      {% endif %}
    {% endfor %}
  </div>
{% endfor %}
</div>
```

- [ ] **Step 2: Verify in the browser**

```bash
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000/tags`. Confirm: every tag from the front matter cleanup in Task 5 appears as a heading (alphabetically sorted), with the correct posts listed under each (e.g. "genai" should list both the MCP server post and the custom-model-import post), and `render: false` posts (the 2021 X-Play/Test-Drive posts) do not appear. Stop the server.

- [ ] **Step 3: Commit**

```bash
git add tags.html
git commit -m "Add Tags page grouping posts by tag"
```

---

### Task 9: About page — relocate bio and links

Move the videos/talks/blog-links content that used to live on the homepage into `about.html`, with a short bio line above it.

**Files:**
- Modify: `about.html`

- [ ] **Step 1: Rewrite `about.html`**

```html
---
title: About
permalink: "about/index.html"
layout: page
---
<p>I'm Laura. I write about infrastructure, automation, and the fixes I don't want to re-Google later &mdash; mostly Nutanix, Linux, and whatever's currently broken on my Mac.</p>

<h2>Speaking</h2>
<ul>
  <li><a href="https://www.youtube.com/watch?v=LUsBgfiCyOA&t=5550" target="_blank">Nutanix .NEXT 2019 Anaheim Keynote</a></li>
  <li><a href="https://youtu.be/v1dz98ZwJB0?t=132" target="_blank">Nutanix .NEXT 2019 Copenhagen Keynote</a></li>
  <li><a href="https://youtu.be/w23_m6T0dd4?t=2897" target="_blank">Nutanix .NEXT 2020 Virtual Keynote</a></li>
  <li><a href="https://www.youtube.com/watch?v=ytU8p8Jd0zU&t=12s" target="_blank">Nutanix .NEXT 2021 Virtual Keynote</a></li>
  <li><a href="https://www.youtube.com/watch?v=owlLY13PEmg" target="_blank">Microsoft Ignite &mdash; What's new in the world of Hybrid Cloud? Find out with Nutanix and Azure</a></li>
</ul>

<h2>Videos</h2>
<ul>
  <li><a href="https://www.youtube.com/watch?v=q4HFcGMO11Q" target="_blank">New Playbook Actions in Nutanix X-Play PC.2021.7 | Tech Bytes | Nutanix University</a></li>
  <li><a href="https://www.youtube.com/watch?v=jtsAx4etUII" target="_blank">Get The Data You're Looking For | Tech Bytes | Nutanix University</a></li>
  <li><a href="https://www.youtube.com/watch?v=YfrFszGN6Q0" target="_blank">Easy automation with 4 new actions in Nutanix X-Play PC.2022.1 | Tech Bytes | Nutanix University</a></li>
  <li><a href="https://www.youtube.com/watch?v=ihAfqkN4lkg" target="_blank">Prism for IT Operations Features | Tech Bytes | Nutanix University</a></li>
  <li><a href="https://www.youtube.com/watch?v=MJfETH-bU-A" target="_blank">Setting up Cluster RBAC | Tech Bytes | Nutanix University</a></li>
  <li><a href="https://www.youtube.com/watch?v=WtM3hBJQVNY" target="_blank">Capacity Planning | Tech Bytes | Nutanix University</a></li>
  <li><a href="https://www.youtube.com/watch?v=SbFbIuFv5xc" target="_blank">Nutanix X-Play and ServiceNow Integration | Tech Bytes | Nutanix University</a></li>
  <li><a href="https://www.youtube.com/watch?v=xMLrALGPHZ4" target="_blank">Automated Remediation with X-Play | Tech Bytes | Nutanix University</a></li>
</ul>

<h2>Blogs &amp; Code Samples</h2>
<ul>
  <li><a href="https://www.nutanix.dev/2022/01/19/getting-started-with-nutanix-x-play/" target="_blank">Getting Started With Nutanix X-Play</a></li>
  <li><a href="https://www.nutanix.dev/2021/12/22/code-sample-collecting-cluster-wide-vm-performance-data-with-python/" target="_blank">Collecting Cluster Wide VM Performance Data With Python</a></li>
  <li><a href="https://www.nutanix.dev/2019/12/02/calm-cookbook-recipe-1-blueprint-import/" target="_blank">Calm Cookbook - Blueprint Import</a></li>
  <li><a href="https://next.nutanix.com/community-blog-154/set-up-an-approval-workflow-in-test-drive-40380" target="_blank">Set Up An Approval Workflow in Test Drive</a></li>
  <li><a href="https://next.nutanix.com/community-blog-154/test-drive-application-automation-and-lifecycle-management-today-37853" target="_blank">Test Drive Application Automation and Lifecycle Management Today</a></li>
  <li><a href="https://next.nutanix.com/community-blog-154/deep-dive-into-disaster-recovery-as-a-service-draas-with-test-drive-37693" target="_blank">Deep-dive into Disaster Recovery as a Service (DRaaS) with Test Drive</a></li>
  <li><a href="https://next.nutanix.com/community-blog-154/get-hands-on-with-nutanix-test-drive-2-0-34015" target="_blank">Get Hands-On with Nutanix Test Drive 2.0</a></li>
  <li><a href="https://next.nutanix.com/community-blog-154/maintaining-compliance-with-worm-for-nutanix-objects-33239" target="_blank">Maintaining Compliance with WORM for Nutanix Objects</a></li>
  <li><a href="https://next.nutanix.com/community-blog-154/using-nutanix-objects-as-an-s3-compatible-backup-target-32959" target="_blank">Using Nutanix Objects as an S3-Compatible Backup Target</a></li>
  <li><a href="https://next.nutanix.com/community-blog-154/nutanix-objects-and-containerized-architecture-32020" target="_blank">Nutanix Objects and Containerized Architecture</a></li>
</ul>
```

- [ ] **Step 2: Verify in the browser**

```bash
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000/about`. Confirm: bio line at top, then Speaking/Videos/Blogs & Code Samples sections with all links intact and working (spot-check 2-3). Stop the server.

- [ ] **Step 3: Commit**

```bash
git add about.html
git commit -m "Relocate videos/talks/blog links to About page"
```

---

### Task 10: Post page restyle — tags, meta, prev/next nav

Restyle `_layouts/post.html` to match the new visual identity: title, date, tag pills (linking to the Tags page), content, then prev/next post navigation. This replaces the now-deleted `post-header.html`/`post-footer.html` includes with inline markup.

**Files:**
- Modify: `_layouts/post.html`
- Modify: `_sass/posts.scss` (add post-page and prev/next-nav styles)

**Interfaces:**
- Consumes: `page.tags` (Task 5's front matter cleanup) and the `#<slug>` anchors on the Tags page (Task 8).

- [ ] **Step 1: Rewrite `_layouts/post.html`**

```html
---
layout: default
---

<article>
  <header class="post-header">
    <h1 class="post-title-main">{{ page.title }}</h1>
    <p class="post-meta">{{ page.date | date_to_string }}</p>
    {% if page.tags and page.tags.size > 0 %}
    <ul class="post-tags">
      {% for tag in page.tags %}
      <li><a href="{{ "/tags" | prepend: site.baseurl }}#{{ tag | slugify }}">{{ tag }}</a></li>
      {% endfor %}
    </ul>
    {% endif %}
  </header>
  <div class="post-content">
    {{ content }}
  </div>
</article>

{% if site.data.theme.show_post_navs %}
  {% if page.previous or page.next %}
    <nav class="post-navs">
      {% if page.previous and page.previous.render != false %}
        <div class="post-nav">
          <h3>Older</h3>
          <h2 class="post-title-link"><a href="{{ page.previous.url | prepend: site.baseurl }}">{{ page.previous.title }}</a></h2>
        </div>
      {% endif %}
      {% if page.next and page.next.render != false %}
        <div class="post-nav">
          <h3>Newer</h3>
          <h2 class="post-title-link"><a href="{{ page.next.url | prepend: site.baseurl }}">{{ page.next.title }}</a></h2>
        </div>
      {% endif %}
    </nav>
  {% endif %}
{% endif %}
```

- [ ] **Step 2: Add post-page and prev/next-nav styles to `_sass/posts.scss`** (append to the end of the existing file from Task 5)

```scss
.post-header {
  margin-bottom: 2rem;
}

.post-title-main {
  margin-bottom: 0.25rem;
}

.post-meta {
  color: var(--color-muted);
  font-size: 0.9rem;
  margin: 0 0 0.75rem;
}

.post-tags {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 0;
  padding: 0;
}

.post-tags li a {
  display: inline-block;
  border: 1px solid var(--color-border);
  border-radius: 999px;
  padding: 0.15rem 0.7rem;
  font-size: 0.8rem;
  color: var(--color-muted);
}

.post-tags li a:hover {
  color: var(--color-accent);
  border-color: var(--color-accent);
  text-decoration: none;
}

.post-navs {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-border);
}

.post-nav {
  flex: 1 1 240px;
}

.post-nav h3 {
  margin-top: 0;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-muted);
}

.post-title-link {
  margin-top: 0.25rem;
  font-size: 1rem;
}
```

- [ ] **Step 3: Verify in the browser**

```bash
bundle exec jekyll serve
```

Open a post, e.g. `http://127.0.0.1:4000/calm-dsl-v4-2-0-cheat-sheet`. Confirm: title, date, and tag pills render at the top; clicking a tag pill navigates to `/tags#<tag>` and lands near the right heading; prev/next post navigation renders at the bottom with working links. Stop the server.

- [ ] **Step 4: Commit**

```bash
git add _layouts/post.html _sass/posts.scss
git commit -m "Restyle post page with tag pills and prev/next navigation"
```

---

### Task 11: Delete demo posts and full-site verification pass

Remove the leftover 2014 Shiori demo posts and do a final end-to-end check across every page and both color themes.

**Files:**
- Delete: `_posts/2014-06-28-example-bootstrap.md`, `_posts/2014-07-27-example-css.md`

- [ ] **Step 1: Delete the demo posts**

```bash
git rm _posts/2014-06-28-example-bootstrap.md _posts/2014-07-27-example-css.md
```

- [ ] **Step 2: Full build check**

```bash
bundle exec jekyll build
```

Expected: exits 0, no warnings about missing layouts/includes.

- [ ] **Step 3: Full manual verification pass**

```bash
bundle exec jekyll serve
```

Walk through and confirm, in **both** light and dark mode (toggle partway through):

- `/` — tagline + 3 recent posts, all links work
- `/archive` — all real posts grouped by month/year, "Notes" label in nav is active/highlighted
- `/tags` — every tag from Task 5's cleanup shows the right posts, no `render: false` posts appear
- `/about` — bio + Speaking/Videos/Blogs sections, links work
- A post page — tags pills, code blocks (light and dark), prev/next nav
- Narrow the window to mobile width — nav collapses to hamburger, no horizontal scroll/broken layout anywhere
- Reload the page after toggling dark mode — theme persists (no flash of light theme before dark applies)
- `/feed.xml` — still renders valid RSS (spot check in browser)

Stop the server once everything checks out.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "Remove leftover Shiori demo posts"
```
