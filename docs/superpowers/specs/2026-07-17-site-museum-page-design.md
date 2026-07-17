# Site Museum Page — Design Spec

## Motivation

The user wants to be able to look back at what this blog looked like at earlier points in its life. The repo already has an exact precedent for this: `nutanix-bible-history.md`, a standalone page (not linked from nav) documenting past visual versions of the Nutanix Bible site with a heading, bullet list of what changed, and screenshots per version.

## Scope

A single new standalone page, `museum.html`, following the same pattern. No new layout, no new CSS, no JS — reuses the existing `page` layout and default page styling.

## Page content

- Front matter: `title: The Museum`, `permalink: "museum.html"`, `layout: page`.
- Not linked from the nav or any other page — reachable only by direct URL, same as `nutanix-bible-history.md`.
- Intro line: "A look back at what this blog used to look like."
- One version section for now, matching the `nutanix-bible-history.md` heading style (`## <name> (<date/range>)`, bullet list, then images):

  ```
  ## Shiori theme (until July 2026)
  * Bootstrap 3 + jQuery theme (Shiori)
  * Sidebar navigation with category ribbon
  * Homepage was a hardcoded list of videos, talks, and blog links

  ![](images/laurajordana/laurajordana_v1_home.png)
  ![](images/laurajordana/laurajordana_v1_blog.png)
  ![](images/laurajordana/laurajordana_v1_post.png)
  ```

- Images already exist at `images/laurajordana/` (`laurajordana_v1_home.png`, `laurajordana_v1_blog.png`, `laurajordana_v1_post.png`) — no image processing needed, just reference them the same way `nutanix-bible-history.md` references `images/bible/*.png` (relative path, no leading slash — both pages live at the site root so this resolves correctly).
- Future versions (e.g. the current Clean Minimal redesign, once screenshotted) get added the same way: a new `## heading` + bullets + images, appended below the existing section. Not part of this pass — deferred until screenshots of the current design exist.

## Verification

No automated test suite on this project (consistent with the rest of the site). Verify manually via `bundle exec jekyll build`/`serve`:
- Page builds with no errors.
- `/museum.html` renders the intro line, the heading, the three bullets, and all three images loading correctly.
- Confirm the page is NOT linked from `_includes/nav.html` or `about.html`.
