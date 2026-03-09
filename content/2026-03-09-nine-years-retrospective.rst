Nine Years of Quiet Building
#############################

:date: 2026-03-09 12:00:00
:tags: python, javascript, hardware, retrospective, open-source
:category: programming

The blog went quiet in 2017. The keyboard didn't.

Here's what happened in the intervening nine years — a quick tour through the
projects that got built, shipped, and occasionally finished.

----

The SNMP Ecosystem
==================

The most sustained body of work, and the one I'm most proud of.

`puresnmp <https://github.com/exhuma/puresnmp>`_ is a pure Python SNMPv2
library — no C extensions, no compiled dependencies, just Python. The goal was
simple: make SNMP accessible without fighting a build system first. It quietly
grew from a weekend experiment into something with actual users, reaching
**v2.0.1 in July 2024**.

Along the way it spawned two companion libraries:

- `x690 <https://github.com/exhuma/x690>`_ — X.690 / BER encoding, extracted
  into its own package (v1.0.0 in 2022) so other tools could use it
  independently.
- `puresnmp-crypto <https://github.com/exhuma/puresnmp-crypto>`_ — DES and AES
  encryption support as an optional add-on, keeping the core dependency-free.

The biggest design lesson: carving out a focused, composable library from a
monolith is worth the effort. ``x690`` being separate means it can evolve
independently. More things should work like this.

----

Infrastructure & Ops Tooling
==============================

A few small tools that scratched real itches.

`pgflux <https://github.com/exhuma/pgflux>`_ ships PostgreSQL monitoring
metrics to InfluxDB. It's one of those tools that does one thing and stays out
of the way — v1.0.0 shipped in 2021 and it hasn't needed much attention since.

`weathermonitor <https://github.com/exhuma/weathermonitor>`_ captures sensor
data from Zigbee/Phoscon devices and stores it for later. Dockerised in 2023,
which made it actually usable on a home server without ceremony.

Three smaller utilities that get regular use:

- `gouge <https://github.com/exhuma/gouge>`_ — a small collection of Python
  logging configurations, because the stdlib defaults are ugly.
- `clproc <https://github.com/exhuma/clproc>`_ — a changelog processor.
- `strec <https://github.com/exhuma/strec>`_ — a stream coloriser for
  stdout/stderr output.

None of these are glamorous. They're the kind of thing you build because the
alternative is doing it by hand every time.

----

Web & Frontend Work
====================

`schmackhaft <https://github.com/exhuma/schmackhaft>`_ is a self-hosted
bookmark manager inspired by the old del.icio.us. Six releases from v0.5 to
v1.2.3 shipped across 2022. The short answer to "why build your own bookmark
manager in 2022" is: the hosted options are either dead, privacy-hostile, or
both.

On the component side:

- `editable-text <https://github.com/exhuma/editable-text>`_ — a web component
  that makes any text element inline-editable.
- `copy-able <https://github.com/exhuma/copy-able>`_ — a web component for
  one-click clipboard copy on any element with a ``.value``.
- `vue-components <https://github.com/exhuma/vue-components>`_ — reusable
  VueJS components, started in 2025.

Small, focused, no framework dependencies. The kind of thing that should exist
as a package but rarely does.

----

Hardware & IoT
===============

In 2025 the work moved off the screen entirely.

`noise-goblin <https://github.com/exhuma/noise-goblin>`_ is a physical button —
ESP32-based, WiFi-connected — that fetches a random sound from an API and plays
it. Originally on a basic ESP32-DevC, it grew an OLED memory display and
eventually moved to the XIAO ESP32S3 module. The commit history from September
2025 tells the story: memory footprint battles, event loop trade-offs, buffer
tuning. Hardware is humbling in ways software rarely is.

`spriglet <https://github.com/exhuma/spriglet>`_ is a more ambitious project:
a collaborative tabletop device ecosystem for games and activities that need
shared counting or tracking. Still early — the design document landed in
September 2025 — but it's the most interesting hardware direction to date.

The honest reflection on moving into hardware: everything you know about
debugging becomes unreliable. You can't ``print()`` your way out of a stack
overflow when there's no stack trace. It's frustrating and completely
absorbing.

----

Developer Workflow
==================

Two recent additions to the toolbox:

`taskfiles <https://github.com/exhuma/taskfiles>`_ — a collection of reusable
`Taskfile <https://taskfile.dev>`_ tasks for common project operations. Started
in January 2026 as a way to stop copying the same boilerplate across repos.

`timerz <https://github.com/exhuma/timerz>`_ — a chess clock implementation,
first commit February 2026. Simple scope, well-contained problem, useful result.

----

What's Next
============

A few things on the horizon:

- **JS modernisation** — ``closure-easing``, ``galeshapley-js``, and others
  were written for Google Closure Library circa 2012. Time to bring them to
  ES6 modules and npm. `Issue filed <https://github.com/exhuma/closure-easing/issues/2>`_.
- **npm publishing** — several of the web components are useful enough to
  publish properly.
- **Profile cleanup** — archiving old forks and playgrounds that have been
  cluttering the profile.

Nine years is a long time to go without a post. Hopefully the next one won't
take as long.
