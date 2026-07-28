# About Page Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Relocate the Speaking/Videos/Blogs & Code Samples content to a new standalone `speaking.html` page, and rewrite `about.html` in the reference site's intro → topics → why → contact format.

**Architecture:** Two sequential tasks. Task 1 creates `speaking.html` (new file, `page` layout, same pattern as `museum.html`) containing the relocated link sections verbatim. Task 2 fully rewrites `about.html` with the new structure and removes the old sections from it (they now live only in `speaking.html`), plus adds small CSS for the new Contact icon links.

**Tech Stack:** Plain Jekyll pages (Markdown/HTML + front matter), inline SVG icons (no new dependency), Sass in `_sass/base.scss`.

## Global Constraints

- Jekyll + GitHub Pages only — no build-pipeline changes.
- No new dependencies (no icon fonts/libraries) — inline SVG only, same approach as the existing copy-code-button icons in `javascripts/main.js`.
- `speaking.html` must NOT be linked from `_includes/nav.html`, `about.html`, or anywhere else — reachable only by direct URL, matching `museum.html`.
- This is a static site with **no automated test suite** — verification is manual, via `bundle exec jekyll build`/`serve`.
- The ambient shell's `$PATH` doesn't include `~/.rbenv/shims` by default — prefix `bundle exec` commands with `export PATH="$HOME/.rbenv/shims:$PATH"` (confirm with `ruby -v` → `3.3.6`).

---

### Task 1: Create `speaking.html`

**Files:**
- Create: `speaking.html`

**Interfaces:**
- Consumes: the existing `page` layout (`_layouts/page.html`), unchanged.

- [ ] **Step 1: Create `speaking.html`**

```markdown
---
title: Speaking & Videos
permalink: "speaking.html"
layout: page
---
<h2>Speaking</h2>
<ul>
  <li><a href="https://www.youtube.com/watch?v=LUsBgfiCyOA&t=5550" target="_blank">Nutanix .NEXT 2019 Anaheim Keynote</a></li>
  <li><a href="https://youtu.be/v1dz98ZwJB0?t=132" target="_blank">Nutanix .NEXT 2019 Copenhagen Keynote</a></li>
  <li><a href="https://youtu.be/w23_m6T0dd4?t=2897" target="_blank">Nutanix .NEXT 2020 Virtual Keynote</a></li>
  <li><a href="https://www.youtube.com/watch?v=ytU8p8Jd0zU&t=12s" target="_blank">Nutanix .NEXT 2021 Virtual Keynote</a></li>
  <li><a href="https://www.youtube.com/watch?v=owlLY13PEmg" target="_blank">Microsoft Ignite - What&rsquo;s new in the world of Hybrid Cloud? Find out with Nutanix and Azure</a></li>
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

- [ ] **Step 2: Build and verify**

```bash
export PATH="$HOME/.rbenv/shims:$PATH"
bundle exec jekyll build
```

Expected: exits 0, no new warnings (the 2 pre-existing unrelated Liquid warnings in `_posts/2026-01-30-running-mcp-server.md` are expected and fine).

```bash
grep -c "<h2>" _site/speaking.html
```

Expected: `3` (Speaking, Videos, Blogs & Code Samples headings).

```bash
grep -c "youtube.com\|youtu.be\|nutanix.dev\|next.nutanix.com" _site/speaking.html
```

Expected: `23` (5 Speaking links + 8 Videos links + 10 Blogs links).

- [ ] **Step 3: Verify unlinked**

```bash
grep -c "speaking" _site/index.html _site/about/index.html _site/archive/index.html _site/tags/index.html
```

Expected: `0` for each (page is not linked from anywhere on the site yet — `about.html` still has its own copy of this content until Task 2 removes it).

- [ ] **Step 4: Commit**

```bash
git add speaking.html
git commit -m "Add standalone Speaking & Videos page"
```

---

### Task 2: Rewrite `about.html`

**Files:**
- Modify: `about.html` (full rewrite, replacing lines 6-41)
- Modify: `_sass/base.scss` (append Contact icon-link styles at end of file)

**Interfaces:**
- Consumes: nothing from Task 1 (this task doesn't link to `speaking.html` — it stands alone per direct URL, per spec).
- Produces: `.contact-links` CSS class (used only within this task).

- [ ] **Step 1: Replace `about.html` body**

Replace the file's content after the front matter (lines 6-41 in the current file) so the full file reads:

```markdown
---
title: About
permalink: "about/index.html"
layout: page
---
<p>I'm Laura. I write about infrastructure, automation, and the fixes I don't want to re-Google later.</p>

<h2>What you'll find here</h2>
<ul>
  <li>Nutanix automation</li>
  <li>Generative AI</li>
  <li>Infrastructure how-tos</li>
</ul>

<h2>Why this blog</h2>
<p>This blog started as a place to save the fixes I didn't want to re-Google &mdash; Nutanix automation scripts, GenAI experiments, infrastructure gotchas. It's grown into a running log of what I've learned building and breaking things, mostly so future-me (and maybe you) doesn't have to start from scratch.</p>

<h2>Contact</h2>
<p class="contact-links">
  <a href="https://github.com/lauramariel" target="_blank" aria-label="GitHub"><svg viewBox="0 0 16 16" width="20" height="20" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg></a>
  <a href="https://linkedin.com/in/laurajordana" target="_blank" aria-label="LinkedIn"><svg viewBox="0 0 16 16" width="20" height="20" fill="currentColor"><path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/></svg></a>
</p>
```

- [ ] **Step 2: Append Contact icon-link CSS to `_sass/base.scss`**

Append at the end of the file:

```scss
.contact-links {
  display: flex;
  gap: 0.75rem;
}

.contact-links a {
  display: inline-flex;
  color: var(--color-muted);
}

.contact-links a:hover,
.contact-links a:focus-visible {
  color: var(--color-accent);
  text-decoration: none;
}
```

- [ ] **Step 3: Build and verify**

```bash
export PATH="$HOME/.rbenv/shims:$PATH"
bundle exec jekyll build
```

Expected: exits 0, no new warnings.

```bash
grep -c "<h2>" _site/about/index.html
```

Expected: `3` ("What you'll find here", "Why this blog", "Contact").

```bash
grep -c "youtube.com\|nutanix.dev" _site/about/index.html
```

Expected: `0` (old Speaking/Videos/Blogs links fully removed from `about.html`).

```bash
grep -c "github.com/lauramariel\|linkedin.com/in/laurajordana" _site/about/index.html
```

Expected: `2`.

- [ ] **Step 4: Manually verify in the browser**

```bash
bundle exec jekyll serve
```

Open `http://127.0.0.1:4000/about/`. Confirm order: intro paragraph, "What you'll find here" (3 bullets: Nutanix automation, Generative AI, Infrastructure how-tos), "Why this blog" (paragraph), "Contact" (GitHub + LinkedIn icons). Hover each icon — confirm it changes to the accent color, no underline. Click each — confirm it opens the correct profile in a new tab. Toggle dark mode — confirm icons stay legible and themed correctly (icons use `currentColor`, following `--color-muted`/`--color-accent`). Then open `http://127.0.0.1:4000/speaking.html` directly — confirm it still renders correctly (unaffected by this task).

Stop the server once verified.

- [ ] **Step 5: Commit**

```bash
git add about.html _sass/base.scss
git commit -m "Redesign About page with topics/why/contact sections"
```

---
