# Post Content Enhancements — Design Spec

## Motivation

Two independent improvements to the reading experience on post pages:

1. Deep-linkable headings — readers can't currently share a link to a specific section of a post.
2. Enlargeable images — screenshots and diagrams embedded in posts are shown at their inline width only, with no way to view them larger.

Both are small, self-contained DOM enhancements that fit the site's existing "vanilla JS, no dependencies" approach (see the copy-code-button feature in `javascripts/main.js`).

## Scope

Two features, implemented together since both are small and touch the same files:

- Heading anchor links, scoped to `h2`/`h3` inside `.post-content` (post body only — not the post title, not other pages like `about.html`/`archive.html`).
- Image lightbox, scoped to all `img` elements inside `.post-content`.

No new dependencies, no new files. Extends the existing `javascripts/main.js` IIFE and `_sass/base.scss`, same pattern as the existing copy-code-button feature.

## Feature 1: Heading anchors

- Jekyll's default markdown processor (kramdown) already auto-generates an `id` attribute on every heading (confirmed via build output, e.g. `<h2 id="versions-used">Versions used</h2>`) — no Liquid/layout changes needed to get IDs.
- On page load, JS selects every `h2`, `h3` inside `.post-content` and prepends an anchor element: `<a class="heading-anchor" href="#{id}">#</a>`.
- Styling: absolutely positioned to the left of the heading (via a wrapping `position: relative` on the heading), `opacity: 0` by default, fading to `opacity: 1` on heading `:hover` or anchor `:focus-visible` — same fade pattern as `.copy-code-btn`.
- Behavior is native anchor-tag behavior: left-click scrolls and updates `location.hash`; middle-click/cmd-click opens in a new tab; right-click offers "copy link" — no custom click handler required.

## Feature 2: Image lightbox

- On page load, JS selects every `img` inside `.post-content` and attaches a click handler.
- Click handler builds a fixed, full-viewport overlay element (dark scrim, appended to `document.body`) containing a cloned/enlarged `<img>` sized via `max-width: 90vw; max-height: 90vh` (preserves aspect ratio, never exceeds viewport).
- Overlay closes on: click anywhere within the overlay, or `Escape` keydown. Overlay is removed from the DOM on close (not just hidden), so repeated opens don't accumulate stale elements.
- `.post-content img` gets `cursor: zoom-in` via CSS as a hover affordance.
- The scrim uses a fixed semi-transparent dark background (not theme-variable-driven) so the enlarged image stays legible in both light and dark mode.

## Non-goals

- No caption support, no next/prev navigation between multiple images in a post — single-image lightbox only.
- No lazy-loading or thumbnail generation — images already load at their existing markdown-defined size.
- No anchors on `h1`/`h4+` or on non-post pages.

## Verification

No automated test suite on this project (consistent with the rest of the site). Verify manually via `bundle exec jekyll serve`:

- Open a post with multiple `h2`/`h3` headings. Hover each — confirm a `#` fades in to the left. Click it — confirm the URL gains `#heading-id` and the page scrolls/stays at that heading. Reload with that hash in the URL — confirm the browser lands at the right heading.
- Open a post with images. Hover an image — confirm the cursor changes to zoom-in. Click it — confirm a fullscreen overlay shows the image enlarged and centered, in both light and dark mode. Click the overlay — confirm it closes. Reopen and press `Esc` — confirm it closes.
- Confirm non-post pages (`about.html`, `archive.html`, `tags.html`) are unaffected (no anchors, no lightbox — since selectors are scoped to `.post-content`).
