# michel.albert.lu — blog

Personal blog built with [Pelican](https://getpelican.com). Live at **https://michel.albert.lu**.

## Requirements

- Python 3.8+
- [Task](https://taskfile.dev) (`brew install go-task` / `apt install task`)

## Setup

```sh
task install
```

## Common tasks

| Command | Description |
|---------|-------------|
| `task dev` | Watch + serve locally at http://localhost:8000 |
| `task build` | One-off build (dev config) |
| `task build:prod` | Build with production settings |
| `task rebuild` | Clean then build from scratch |

## Writing a post

Add a `.rst` file to `content/`:

```rst
My Post Title
#############

:date: 2026-01-01 10:00:00
:tags: python, whatever
:category: programming

Post body here.
```

## Deployment

Every push to `master` deploys the site to GitHub Pages:
`.github/workflows/pages.yml` builds with `publishconf.py` and
publishes `output/`. Branches are never deployed.

Pages link to each other with relative URLs, so the same build works at
<https://michel.albert.lu> and under <https://exhuma.github.io/blog>.
Only the feeds use absolute URLs, taken from `SITEURL`. To point them
elsewhere, set `PELICAN_SITEURL`, or pass the `siteurl` input to a
manual run of the workflow:

```sh
gh workflow run pages.yml -f siteurl=https://exhuma.github.io/blog
```
