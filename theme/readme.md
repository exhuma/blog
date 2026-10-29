# Blog theme

Pelican theme for michel.albert.lu. It applies the Michel Albert design
system: <https://claude.ai/artifact/USZfWqBJGsJhfdoiH7HXH2>.

Originally based on "Built Texts" (see `LICENSE.txt`); rewritten in 2026
without Bootstrap, jQuery or Font Awesome.

## Layout

- `templates/` — Jinja2 templates. `base.html` holds the header, footer,
  fonts and the light/dark toggle.
- `static/css/main.css` — design tokens, components (`ma-*`) and prose
  styles for rendered reStructuredText.
- `static/css/pygments.css` — syntax highlighting built from the tokens.

## Rules

- Use the CSS custom properties from `main.css`. Do not add raw colour
  values to templates or new CSS.
- Dark is the default theme. Light follows `prefers-color-scheme`, or the
  toggle, which sets `data-theme` on `<html>`.
- No icon sets and no illustrations. Images get a 1px hairline and the
  4px radius.
- Fonts: Source Sans 3 for text, Source Code Pro for code. Headings use
  weight 600.
