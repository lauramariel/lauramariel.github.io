# Site Museum Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a standalone `museum.html` page documenting past visual versions of this blog, starting with the old Shiori theme.

**Architecture:** A single new Jekyll page using the existing `page` layout — no new layout, CSS, or JS. Follows the exact pattern already established by `nutanix-bible-history.md` (heading + bullets + images per version).

**Tech Stack:** Plain Jekyll page (Markdown + front matter), no new dependencies.

## Global Constraints

- Jekyll + GitHub Pages only — no build-pipeline changes.
- Page must NOT be linked from `_includes/nav.html`, `about.html`, or anywhere else — reachable only by direct URL, matching `nutanix-bible-history.md`.
- Images already exist at `images/laurajordana/` — do not move, rename, or reprocess them.
- This is a static site with **no automated test suite** — verification is manual, via `bundle exec jekyll build`/`serve`.
- The ambient shell's `$PATH` doesn't include `~/.rbenv/shims` by default — prefix `bundle exec` commands with `export PATH="$HOME/.rbenv/shims:$PATH"` (confirm with `ruby -v` → `3.3.6`).

---

### Task 1: Create the museum page

**Files:**
- Create: `museum.html`

**Interfaces:**
- Consumes: the existing `page` layout (`_layouts/page.html`), unchanged.
- Consumes: existing image files at `images/laurajordana/laurajordana_v1_home.png`, `images/laurajordana/laurajordana_v1_blog.png`, `images/laurajordana/laurajordana_v1_post.png` — already present in the repo, not created by this task.

- [ ] **Step 1: Create `museum.html`**

```markdown
---
title: The Museum
permalink: "museum.html"
layout: page
---

A look back at what this blog used to look like.

## Shiori theme (until July 2026)
* Bootstrap 3 + jQuery theme (Shiori)
* Sidebar navigation with category ribbon
* Homepage was a hardcoded list of videos, talks, and blog links

![](images/laurajordana/laurajordana_v1_home.png)
![](images/laurajordana/laurajordana_v1_blog.png)
![](images/laurajordana/laurajordana_v1_post.png)
```

- [ ] **Step 2: Build and verify**

```bash
export PATH="$HOME/.rbenv/shims:$PATH"
bundle exec jekyll build
```

Expected: exits 0, no new warnings (the 2 pre-existing unrelated Liquid warnings in `_posts/2026-01-30-running-mcp-server.md` are expected and fine).

```bash
grep -c "laurajordana_v1" _site/museum.html
```

Expected: `3` (all three images referenced in the built page).

- [ ] **Step 3: Verify live and confirm it's unlinked**

```bash
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000/museum.html` directly — confirm the intro line, heading, three bullets, and all three images render and load correctly (no broken image icons).

```bash
grep -c "museum" _site/index.html _site/about/index.html _site/archive/index.html _site/tags/index.html
```

Expected: `0` for each (page is not linked from anywhere on the site).

Stop the server once verified.

- [ ] **Step 4: Commit**

```bash
git add museum.html
git commit -m "Add site museum page with Shiori-era screenshots"
```

---
