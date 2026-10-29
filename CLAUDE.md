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
| Prod build| `task build:prod` | Uses `publishconf.py`. Never deploys.    |

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
  Post Title in Title Case
  ########################

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
- Write in Michel's voice. See "Voice" below.

### Where posts come from

The blog is being revived to write about Michel's current work: Claude
Code workflows (the `umbrella` meta-repo, Quartermaster kits) and
Hermes. Michel provides the material for a post, usually with links to
issues and pull requests. Draft from those, but leave the post on a
branch for Michel to review. Never publish on his behalf.

## Voice

Posts are written as Michel. The reference is his own posts from 2009
to 2017, for example `2014-10-06-automove-files-on-wifi-connect.rst`,
`2015-02-23-maximising-in-x11.rst` and `2016-03-04-flask-social.rst`.
`2026-03-09-nine-years-retrospective.rst` was co-written by an AI and
shows what to avoid. Do not use it as a model.

### Tone

- First person, conversational, like explaining something to a
  colleague over coffee. Not a press release, not a pitch.
- Start from a concrete situation: what annoyed him, what he needed,
  what he tried. "For ages, I was annoyed that ...", "A couple of weeks
  ago I decided to ...", "I've been using X for quite some time. But
  recently ...".
- Be honest about effort and dead ends. Say what did not work and what
  is only a guess: "However, this did not work for me.", "I assume that
  ...", "I should have known better."
- Dry, self-deprecating humour in small doses: "because I'm lazy",
  "So yay...", "that's where the fun started".
- Enthusiasm is fine when it is plain: "nifty", "really handy",
  "impressed so far". At most one exclamation mark per post.
- Credit people and tools by name, with a link.

### Structure

- Get to the point in the first paragraph. Short posts are fine; 150
  words can be a whole post.
- Practical posts follow the problem: what happened, why, and what
  fixed it. Headings like "The Problem", "Solution" and "End-Result"
  are fine. Long posts may open with an `Abstract` topic.
- Show the real thing: commands, config, code, numbers, and links to
  the commits or pull requests.
- Caveats go into a `.. note::`, including what he would still improve.
- Stop when the content is done. No conclusion, no recap, no moral.
  "And that's it!" is as much ending as a post needs.
- Collect links as reStructuredText reference targets at the bottom.

### Vocabulary and mechanics

- Plain technical English. Prefer the simple word. British spellings
  where they come naturally (colour, maximise, visualise).
- Titles and section headings in Title Case, like his existing posts.
- `*emphasis*` for the one word that matters, ``literals`` for names,
  commands and files. Bold rarely.
- Contractions are fine: "I've", "it's", "don't".

### Never

These read as machine-written. Michel noticed them in a draft.

- Aphorism openers and slogans: "The blog went quiet in 2017. The
  keyboard didn't.", headings like "Finished means correct".
- Em dashes as a rhythm device. Use a full stop or a comma.
- Parallel headings or sentences repeated for effect, and lists of
  three for rhythm.
- "Not X, but Y" contrasts, "The point is", "Here's what happened",
  "quietly", "journey", "landscape", "robust", "seamless", "leverage".
- Summary or call-to-action endings.
- Claims nobody measured. Say what was done and measured; mark
  opinions with "I think".
- Invented motives. If the reason for something is unknown, leave a
  `.. TODO` comment for Michel instead of guessing.

## Theme

The theme in `theme/` applies the Michel Albert design system. Source
of truth: <https://claude.ai/artifact/USZfWqBJGsJhfdoiH7HXH2>.
`theme/readme.md` lists the rules. In short:

- Only use the CSS custom properties defined in
  `theme/static/css/main.css`. No raw colour values.
- Dark is the default; light must keep working. Check both.
- No icon sets, no illustrations, no CSS frameworks. The contour-line
  backdrop is the one exception; never hand-edit
  `theme/static/css/backdrop.css`.
- Before calling a theme change done, run `task build` and look at the
  index, an article with code and a callout (for example
  `getting-flask-social-working`), and the archives, at desktop and
  phone width.
