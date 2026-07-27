# About Page Redesign — Design Spec

## Motivation

The current `about.html` opens with a one-line bio, then dumps three long link-list sections (Speaking, Videos, Blogs & Code Samples) — mostly older Nutanix conference/community content. The user wants a more personal, narrative About page in the style of https://joseluisgomez.com/about/ (short intro → "what you'll find here" topic list → "why this blog" → contact links), with the old link-heavy sections moved out to their own page rather than deleted.

## Scope

Two pieces:

1. A new standalone page, `speaking.html`, holding the relocated Speaking/Videos/Blogs & Code Samples content verbatim.
2. A rewritten `about.html` following the reference page's structure.

No new layouts, no new CSS beyond small inline-icon links, no JS.

## Part 1: `speaking.html`

- Front matter: `title: Speaking & Videos`, `permalink: "speaking.html"`, `layout: page` — same pattern as the existing `museum.html`.
- Not linked from `_includes/nav.html`, `about.html`, or anywhere else — reachable only by direct URL, same as `museum.html` and `nutanix-bible-history.md`.
- Content: the current `about.html` `<h2>Speaking</h2>`, `<h2>Videos</h2>`, and `<h2>Blogs &amp; Code Samples</h2>` sections (headings + list markup + all links), moved verbatim — no link or text changes.

## Part 2: `about.html` rewrite

Structure, matching the reference page:

1. **Intro** — unchanged from today: "I'm Laura. I write about infrastructure, automation, and the fixes I don't want to re-Google later."
2. **"What you'll find here"** (`<h2>`) — bulleted list (`<ul>`) with exactly three items: Nutanix automation, Generative AI, Infrastructure how-tos.
3. **"Why this blog"** (`<h2>`) — one paragraph:
   > "This blog started as a place to save the fixes I didn't want to re-Google — Nutanix automation scripts, GenAI experiments, infrastructure gotchas. It's grown into a running log of what I've learned building and breaking things, mostly so future-me (and maybe you) doesn't have to start from scratch."
4. **"Contact"** (`<h2>`) — two inline-SVG icon links, no new dependency (same approach as the existing copy-code-button icons in `javascripts/main.js`):
   - GitHub icon → `https://github.com/lauramariel`
   - LinkedIn icon → `https://linkedin.com/in/laurajordana`
   - Both open in a new tab (`target="_blank"`), matching the existing external-link convention already used in `about.html`'s Speaking/Videos links.

All old Speaking/Videos/Blogs & Code Samples markup is removed from `about.html` (relocated to `speaking.html`, not duplicated).

## Non-goals

- No photo/avatar (the reference page doesn't have one either).
- No changes to `_layouts/page.html` or any shared layout/CSS structure.
- No changes to nav — neither `about.html`'s new content nor `speaking.html` add any nav links.

## Known side effect (not addressed by this spec)

`_layouts/page.html` wraps all page content — including `about.html` and the new `speaking.html` — in the same `.post-content` div used by blog posts. The still-unexecuted heading-anchors feature (`docs/superpowers/plans/2026-07-21-post-content-enhancements.md`) scopes its anchor links to `.post-content h2, h3`, meaning once that plan is executed, the new `<h2>` headings on `about.html` (and `speaking.html`) will also get hover-reveal anchor links. This is a pre-existing structural fact about `page.html`, not something this change introduces. Left as-is for now; worth revisiting when the heading-anchors plan is executed, since that plan's verification steps assume `about.html` has no headings in `.post-content` (no longer true after this change).

## Verification

No automated test suite on this project. Verify manually via `bundle exec jekyll build`/`serve`:

- `speaking.html` builds and renders all three original sections with all links intact and working (spot-check a few).
- `speaking.html` is not linked from `_includes/nav.html`, `about.html`, `archive.html`, `tags.html`, or `index.html`.
- `about.html` renders in order: intro, "What you'll find here" (3 bullets), "Why this blog" (paragraph), "Contact" (2 icon links).
- Both Contact icons link to the correct URLs and open in a new tab.
- Visual check in both light and dark mode — icons and links are legible/themed correctly (using existing `--color-fg`/`--color-accent` patterns, no new hardcoded colors).
