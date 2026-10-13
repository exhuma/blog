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
| `task publish` | Build prod + rsync to server |

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

`task publish` builds with `publishconf.py` and rsyncs `output/` over SSH
to an AWS EC2 instance (Apache, eu-central-1).

A GitHub Actions workflow that runs this on every push to `master` is
prepared in `docs/workflows-deploy.yml` but **not active yet**. To enable
it, move it to `.github/workflows/deploy.yml` and set the `DEPLOY_SSH_KEY`
repository secret. Until then, nothing is deployed automatically, and
even once it is, only `master` is published.
