# blog

Michel Albert's personal blog, live at <https://michel.albert.lu>.
Static site built with [Pelican](https://getpelican.com) from
reStructuredText. Read `README.md` for setup; this file covers what an
agent needs on top of it.

## Commands

All tooling goes through [Task](https://taskfile.dev). Do not add a
Makefile, fabfile or shell scripts next to it.

| Purpose   | Command           | Notes                                    |
|-----------|-------------------|------------------------------------------|
| Bootstrap | `task install`    | Creates `.venv`, installs requirements.  |
| Run       | `task dev`        | Autoreload + server on :8000.            |
| Build     | `task build`      | Dev config, output in `output/`.         |
| Prod build| `task build:prod` | Uses `publishconf.py`. Safe, no deploy.  |
| Publish   | `task publish`    | Legacy rsync to the old server. Unused.  |

Dependencies are pinned in `requirements.txt`, compiled from
`requirements.in` with `pip-compile`. Edit the `.in` file, then
recompile.

## Branches and publishing

- `master` is what is live. Work on a feature branch and open a pull
  request. Never push to `master` directly.
- Every push to `master` deploys: `.github/workflows/pages.yml` builds
  with `publishconf.py` and publishes to GitHub Pages. Merging a pull
  request is publishing. Branches are never deployed.
- Do not change the workflow, the Pages settings (custom domain
  included) or secrets unless Michel asks.

## Writing posts

- One file per post in `content/`, named `YYYY-MM-DD-slug.rst`.
- Metadata block under the title:

  ```rst
  Post title in sentence case
  ###########################

  :date: 2026-10-13 10:00:00
  :tags: python, tooling
  :category: programming
  :summary: One sentence for the index page.
  ```

- Reuse existing categories (`automation`, `desktop`, `programming`,
  `sysadmin`, `web`) unless a new one is clearly needed.
- Images go in `content/images/`. Link them with `{static}/images/...`
  (older posts use `{filename}`, which Pelican warns about).
- Unfinished posts get `:status: draft`, or stay in `staging/`, which
  Pelican does not build.
- Voice: short sentences, sentence case, no emoji, no exclamation marks.
  Name things by what they are.

### Where posts come from

The blog is being revived to write about Michel's current work: Claude
Code workflows (the `umbrella` meta-repo, Quartermaster kits) and
Hermes. Michel provides the material for a post, usually with links to
issues and pull requests. Draft from those, but leave the post on a
branch for Michel to review. Never publish on his behalf.

## Theme

The theme in `theme/` applies the Michel Albert design system. Source
of truth: <https://claude.ai/artifact/USZfWqBJGsJhfdoiH7HXH2>.
`theme/readme.md` lists the rules. In short:

- Only use the CSS custom properties defined in
  `theme/static/css/main.css`. No raw colour values.
- Dark is the default; light must keep working. Check both.
- No icon sets, no illustrations, no CSS frameworks.
- Before calling a theme change done, run `task build` and look at the
  index, an article with code and a callout (for example
  `getting-flask-social-working`), and the archives, at desktop and
  phone width.
