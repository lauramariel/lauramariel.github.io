# Code Block Copy Button — Design Spec

## Motivation

Code blocks on this blog already have syntax highlighting (Rouge, with light/dark themes matching the site's overall theme). There's no way to copy a block's contents except manual text selection, which is fiddly for multi-line commands. Add a copy button to every code block.

## Scope

Client-side only, vanilla JS + hand-written SCSS — consistent with the rest of this redesigned site (no jQuery, no new icon libraries, no build-pipeline changes, Jekyll + GitHub Pages compatible).

## Behavior

- Every Rouge-generated code block (`div.highlighter-rouge`) gets a copy button injected at page load.
- The button sits in the block's top-right corner, absolutely positioned. It's invisible by default and fades in on hover of the code block (`opacity` transition, no layout shift).
- Clicking the button copies the block's raw code text (via `navigator.clipboard.writeText()`) — the `<code>` element's `textContent`, so no line numbers, prompts, or injected markup leak into the copied text.
- On successful copy, the button's icon swaps from a copy glyph to a checkmark and shows the text "Copied" for ~1.5 seconds, then reverts to its default state.
- If `navigator.clipboard` isn't available (very old browser), the button is not injected for that block at all — no dead/broken button in the UI.

## Visual design

- Icons are inline SVG (copy icon, checkmark icon) — no new icon library or font dependency.
- Button styling matches the site's existing small-control look (e.g. the tag pills in `_sass/posts.scss`): `border: 1px solid var(--color-border)`, `color: var(--color-muted)` by default, hover/active state uses `var(--color-accent)` for both border and icon color.
- Fully theme-aware via the site's existing CSS custom properties — no new hardcoded colors, works automatically in both light and dark mode.

## Implementation approach

- **JS** (`javascripts/main.js`, extending the existing IIFE alongside the dark-mode toggle and mobile-nav logic): on `DOMContentLoaded`, `querySelectorAll('.highlighter-rouge')`, for each block find its `code` element, inject a `<button class="copy-code-btn">` as the first child of the wrapper, wire a `click` listener.
- **CSS** (new rules in `_sass/base.scss`, alongside the existing `pre`/`code` rules): `.highlighter-rouge` gets `position: relative`; `.copy-code-btn` is absolutely positioned, opacity 0 by default, opacity 1 on `.highlighter-rouge:hover .copy-code-btn` and on the button's own `:focus-visible` (so keyboard users can reach it without hovering).
- No Jekyll plugin, no build-pipeline changes — this is pure client-side enhancement on top of Rouge's existing static HTML output.

## Alternatives considered (not chosen)

- **Font Awesome icons** (already loaded via the site's FA kit script): rejected to avoid depending on an external icon kit for two simple glyphs, and to avoid a possible icon-flash if the kit script hasn't loaded yet.
- **Build-time injection via a custom Jekyll plugin**: rejected — GitHub Pages' safe-mode build doesn't run arbitrary custom plugins, and this would violate the "no build-pipeline changes" constraint established in the original redesign.

## Verification

No automated test suite on this project (static site, manual verification only, consistent with the rest of the redesign). Verify manually via `bundle exec jekyll serve`:
- Every code block on a real post gets a button on hover; keyboard-focusing the button also reveals it.
- Clicking copies the exact code text (paste and compare) with no line numbers/extra whitespace.
- Button shows checkmark + "Copied" for ~1.5s, then reverts.
- Correct appearance in both light and dark mode.
- No regression to existing code block styling (background, syntax colors) from Task 4/the earlier code-block-background fix.
