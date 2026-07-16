# Blog Redesign — Design Spec

Date: 2026-07-15

## Motivation

The site currently runs the [Shiori](https://github.com/ellekasai/shiori) Jekyll theme, an unmaintained (as of the theme's own README) Bootstrap 3 / jQuery theme from ~2014. This redesign addresses three things at once:

1. **Visual style** is dated (Bootstrap defaults, Montserrat/Merriweather Google Fonts, flat-color presets).
2. **Content organization** — the homepage (`index.html`) is a hand-maintained list of Nutanix videos/talks/blog links, entirely disconnected from the Jekyll posts collection. It doesn't read as a blog.
3. **Technical debt** — Bootstrap 3, jQuery, and a theme-authoring helper script (`purplecoat.js`) are all unnecessary for a single-column personal blog.

## Scope

Stay on **Jekyll + GitHub Pages** — no build pipeline changes, same deploy-on-push workflow via the existing `CNAME`/Pages setup. This is a full theme replacement (CSS, layouts, includes, homepage content) but not a platform migration.

## Visual Identity

- **Layout direction:** Clean Minimal — neutral, high-contrast, single-column, content-first. No sidebar (today's `hide_sidebar: true` already hides it; the redesign removes the sidebar code path entirely rather than just hiding it).
- **Typeface:** IBM Plex Sans throughout (headings, body copy, nav, UI chrome). Self-hosted webfont files (woff2) preferred over a Google Fonts CDN link, for reliability and to drop an external network dependency — implementation detail, not a design constraint.
- **Accent color:** Coral / burnt-orange (`~#d6552f`) for links, hover states, tag pills, and small UI details. Everything else stays black/white/gray.
- **Dark mode:** Manual toggle in the nav (not just system-preference `prefers-color-scheme`), state persisted in `localStorage` so it's sticky across visits. Default falls back to system preference on first visit.
- **Code blocks:** Syntax highlighting theme adapts to light/dark mode (light Rouge/Pygments theme in light mode, dark theme in dark mode) so code blocks read as part of the page rather than isolated high-contrast boxes. This matters because a large share of the existing posts are command-line cheat sheets with heavy code content.

## Site Structure & Navigation

Nav bar: **Home · Notes · Tags · About**, plus GitHub/LinkedIn icon links and the dark-mode toggle, right-aligned. Responsive: collapses to a simple mobile menu at narrow widths (no separate mobile-nav partial/JS framework needed — plain CSS).

- **Home (`/`)** — one-line tagline (name + what the site is about) above a list of recent posts (title, date, estimated read time). Replaces the current hardcoded videos/talks/blog-links dump.
- **Notes (`/archive`, URL unchanged, nav label renamed from "Archive" to "Notes")** — full chronological post list grouped by month/year, same grouping logic as today's `archive.html`, restyled.
- **Tags (`/tags`, new page)** — posts grouped by tag, built from post front matter.
- **About (`/about`)** — bio, plus the Videos / Blogs-and-Code-Samples / Speaking link lists relocated from the current homepage.

### Content cleanup (prerequisite, not visual)

- All 12 real posts currently use malformed front matter: `categories: ai, mcp, genai` is a single YAML scalar string, not a list, so `site.categories` doesn't group them usefully today. Add a proper `tags: [ai, mcp, genai]` list field to each post (new field, not repurposing `categories`) so the Tags page can group correctly.
- Delete the two leftover 2014 Shiori theme demo posts: `_posts/2014-06-28-example-bootstrap.md` and `_posts/2014-07-27-example-css.md`. They're theme boilerplate, not real content.

## Technical Approach

- Remove the Shiori theme and its dependencies entirely:
  - Delete `stylesheets/shiori.scss`, `stylesheets/shiori-original.scss`, `_sass/bootstrap-sass/**`, `_sass/custom-bootstrap-variables.scss`, `_sass/custom-scss.scss`.
  - Replace with a single hand-written SCSS file — no CSS framework. A single-column blog layout doesn't need a grid system or component library.
  - Drop jQuery, Bootstrap JS (`javascripts/jquery.min.js`, `javascripts/bootstrap.min.js`), and `purplecoat.js` (a Shiori theme-documentation helper, not used for real site functionality) along with the `data-purplecoat-*` attributes sprinkled through `_includes/*.html`.
  - The only JS needed going forward: a small vanilla-JS dark-mode toggle (~15 lines, `localStorage`-backed).
- Simplify `_layouts/` and `_includes/`:
  - Remove `_layouts/default_without_sidebar.html`, `_includes/sidebar.html`, `_includes/ribbon.html`, `_includes/nav-mobile.html` (mobile nav folds into the single responsive nav markup).
  - `_data/theme.yml` simplified/removed — its Bootstrap color-scheme presets (`color: default/dark/turquoise/...`) and `hide_sidebar` toggle become moot once there's one clean layout with a real dark-mode toggle instead of preset flat-UI color schemes.
- Keep `_layouts/post.html`'s existing prev/next post navigation logic (`page.previous`/`page.next`) — it already works correctly, just needs restyling to match the new visual identity.

## Post Page & Footer

- **Post page:** title, date, tags (rendered as small pills linking back to `/tags`), then post content, in the Clean Minimal type treatment. Prev/next post nav retained at the bottom.
- **Footer:** GitHub + LinkedIn icons (Twitter already removed in a prior commit), RSS link (existing `feed.xml`), copyright line. Drop the "Built with Jekyll and Shiori Theme" attribution since Shiori is being removed.

## Verification

This is a visual/CSS redesign with no test suite to run — verification is running `bundle exec jekyll serve` locally and manually checking:
- Homepage (tagline + recent posts render, links work)
- A post page (typography, code block rendering, prev/next nav, tag pills)
- Notes page (month/year grouping intact)
- Tags page (posts group correctly under their tags)
- About page (bio + relocated video/blog/speaking lists)
- Dark-mode toggle (persists across reload, code blocks re-theme correctly)
- Mobile width (nav collapses, layout doesn't break)
