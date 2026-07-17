# laurajordana.com

Source for my personal blog, built with Jekyll and hosted on GitHub Pages.

## Running locally

Requires Ruby 3.3.6 (pinned in `.ruby-version`; use [rbenv](https://github.com/rbenv/rbenv) or similar).

```
bundle install
bundle exec jekyll serve
```

Then open http://127.0.0.1:4000. Add `--livereload` to auto-refresh on file changes.

## Structure

* `_posts/`: blog posts
* `_layouts/`, `_includes/`: page templates
* `_sass/`, `stylesheets/main.scss`: styles (CSS custom properties drive light/dark theming, see `_sass/variables.scss`)
* `javascripts/main.js`: dark-mode toggle and mobile nav
* `index.html`, `archive.html`, `tags.html`, `about.html`: top-level pages
