# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Carryover is a football-intelligence research project asking whether a striker's
performance and role transfer into a specific team, coach and tactical
environment. It is a research preview: the code currently makes **no predictive
claims**, only descriptive comparisons. First public case: Loïs Openda to
Juventus, reconstructed from information available at transfer time.

## Commands

```sh
make setup     # create .venv and install the package plus the dev extra
make test      # pytest (pythonpath=src, testpaths=tests, addopts=-ra)
make quality   # ruff check . && ruff format --check .
make demo      # run the CLI against examples/data/*.json
```

Every target runs through `.venv/bin/python` and depends on it as a build
target, so `make test` on a clean clone bootstraps the environment first;
`make setup` exists because PRD section 11.2 documents it, not because the
other targets need it run beforehand. The venv is rebuilt whenever
`pyproject.toml` changes, which is how new dependencies get picked up.

Requires Python >= 3.12, and the recipe refuses to build the venv with
anything older. On macOS the Command Line Tools `python3` is often 3.9, so
pass an explicit interpreter when the guard fires:
`make setup PYTHON=python3.12`.

Single test:
`.venv/bin/python -m pytest tests/test_roles.py::test_compare_roles_calculates_deltas_gaps_and_mean_distance`

Run the CLI directly: `.venv/bin/python -m carryover_football <origin.json>
<destination.json>`, or `PYTHONPATH=src python3 -m carryover_football ...`
without a venv (also installed as the `carryover-football` console script).
Dev deps are in the `dev` extra (`pytest`, `ruff`); the runtime package has zero
dependencies and that is deliberate.

## Architecture

`src/` layout, single package `carryover_football`:

- `roles.py` - the domain core. Everything hangs off `DIMENSIONS`, a fixed
  six-tuple of striker behavior dimensions (`depth_running`, `box_presence`,
  `link_play`, `aerial_play`, `pressing`, `chance_creation`). `RoleProfile` is a
  frozen dataclass with exactly those six float fields, all constrained to
  0.0-1.0. `RoleProfile.from_mapping` is a strict validator: missing keys, extra
  keys, non-numeric values and booleans are all `RoleProfileError`.
- `cli.py` - argparse front end; `format_report` does all the rendering and is
  what the CLI tests exercise. `main` converts `OSError`/`RoleProfileError` into
  `parser.error` (exit code 2).
- `__main__.py` - `python -m carryover_football` entry point.

The comparison model, in one line: a *transition* is
`destination_demand - origin_behavior` per dimension. `DimensionComparison`
carries the pair plus `delta` and `absolute_gap`; `RoleTransition` aggregates the
six into `role_transition_distance` (the mean absolute gap) and ranks dimensions
into `largest_new_demands` / `most_deemphasized`. Argument order is
`compare_roles(origin, destination)` and the CLI takes `origin` then
`destination` - getting this backwards flips every sign silently.

Adding or renaming a dimension means editing `DIMENSIONS`, the `RoleProfile`
fields, both example JSON files, and the expected deltas asserted in
`tests/test_cli.py` - they are coupled by design so the schema stays explicit.

## Project constraints

These come from the README's principles and are load-bearing for how code should
be written here, not just documentation:

- **Point-in-time correctness.** No future information may enter a case
  reconstruction.
- **Explainability before complexity.** Prefer a transparent arithmetic index
  over a model whose output cannot be traced by hand.
- `role_transition_distance` is a descriptive index, not a probability, risk
  percentage, or prediction. `cli.DISCLAIMER` says so and the CLI test asserts
  its presence - do not soften or drop it, and do not introduce output that
  reads as a forecast.
- No mentality or personality scoring.
- Player quality and player-context fit are distinct concepts; keep them
  separate in naming and in any future scoring.

## Conventions

Ruff with `select = ["E", "F", "I", "UP", "B", "SIM"]`, line length 88, target
py312. All modules use `from __future__ import annotations` and modern typing
(`str | Path`, `tuple[...]`). Domain types are frozen dataclasses with derived
values exposed as `@property`, not stored fields. Every public function and
class has a one-line docstring.

Use only the regular hyphen (-) in code, comments, output strings, docs, and
commit messages - no em-dash or en-dash. Note `cli.py`'s report header currently
contains an em-dash and does not follow this.
