# Getting Started

Practical setup and day-to-day commands for working on Oneiros. For
the concept and roadmap, see [README.md](README.md); for full
conventions (naming, git, workflow), see [CLAUDE.md](CLAUDE.md).

## Prerequisites

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) - the project's package/env
  manager. Everything below assumes it's installed.
- An NVIDIA GPU with CUDA if you plan to actually run image
  generation (`uv run poe verify-noise` and anything downstream of
  it). Lint/format/tests don't need one.

## Setup

```
uv sync
```

Creates `.venv/` and installs `oneiros/` (editable) plus its runtime
dependencies (torch, diffusers, etc.) and dev tools, all pinned by
`uv.lock`. This pulls a fair amount of ML tooling - if you only need
to lint or format, skip the heavy deps:

```
uv sync --only-dev
```

Either way, run project commands through `uv run <cmd>` rather than
activating the venv or calling `.venv/bin/python` directly - that's
what keeps everyone on the exact versions in `uv.lock`.

## Running things

Task running goes through [`poe`](https://poethepoet.natn.io/)
(poethepoet) - tasks live in `pyproject.toml` under `[tool.poe.tasks]`
and run as `uv run poe <task>`. Run `uv run poe` with no task name to
list what's available along with a description of each - that listing
is always the source of truth; the table below is a snapshot of it.

| Command                     | What it does                                                                          |
| ---------------------------- | -------------------------------------------------------------------------------------- |
| `uv run poe tell-tale-lint`  | Check formatting (`black`), import order (`isort`), and style (`flake8`) - no changes. |
| `uv run poe raven-format`    | Auto-fix formatting and import order (`black` + `isort`, writes changes).              |
| `uv run poe verify-noise`    | Manual smoke test for the noise generator - loads a real Stable Diffusion pipeline (downloads several GB to the Hugging Face cache on first run) and confirms noise reaches it. |

CI (`.github/workflows/lint.yml`) runs `tell-tale-lint` on every push
and PR to `main` - run it locally before pushing so CI isn't the first
place a formatting issue shows up.

There's no automated test suite yet (Phase 1 is still early); the
`poe` tasks above are the extent of the current toolchain.

## Project layout

```
oneiros/            the package - pipeline stages live here (e.g. noise.py)
scripts/             manual/one-off scripts, not part of the package (e.g. verify_noise.py)
docs/todos/          Phase 1 work tracked at build-item granularity
docs/todos/active/    not built yet, one file per item
docs/todos/completed/ shipped, written up as a build record
```

`docs/todos/README.md` lists the current build order and links each
item. Check `completed/` before assuming something hasn't been
considered yet.

## Contributing

- Read [CLAUDE.md](CLAUDE.md) first - it covers naming conventions
  (puns are welcome, within two guardrails), commit expectations, and
  a hard rule about not leaking conversation content into anything
  committed to the repo.
- Keep `uv run poe tell-tale-lint` clean before committing.
- One `docs/todos/` file per unit of work; move it from `active/` to
  `completed/` as a build record when it ships, rather than just
  flipping a status line.
