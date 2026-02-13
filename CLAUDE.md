# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**doge** is a Python CLI tool that prints doge meme-style MOTD messages in the terminal. It displays a Unicode Shibe with randomly placed, colored, grammatically incorrect phrases based on system information or piped stdin. Requires a UTF-8 capable terminal with 256-color support.

## Development Commands

```bash
uv sync                    # Install/sync dependencies
uv run doge                # Run the application
just check                 # Auto-fix lint/format, type check (mypy + ty), and test
just ci                    # Same but strict (no auto-fix, for CI)
just test [args]           # Run tests (e.g. just test tests/test_doge.py::test_name)
```

## Architecture

The codebase lives in `src/doge/` with three modules:

- **core.py** — Main application logic. Key classes:
  - `DogeConfig` — Frozen dataclass for typed CLI configuration (replaces raw `argparse.Namespace`)
  - `TTYHandler` — Terminal detection (dimensions, color support, platform)
  - `Doge` — Orchestrator: loads Shibe art, collects words (system data or stdin), places colored text on random lines
  - `DogeMessage` — Formats individual messages with random prefix/suffix, ANSI 256-color, and spacing
  - `main()` — Entry point (`doge = "doge.core:main"` in pyproject.toml) with UTF-8/locale error handling

- **wow.py** — Data and word collections:
  - `DogeDeque[T]` / `FrequencyBasedDogeDeque[T]` — Generic deques that shuffle and rotate for non-repetitive random word selection
  - `MonthDay` (NamedTuple), `DateRange`, `Season` (TypedDict) — Typed date/season structures
  - Static data: `PREFIXES`, `SUFFIXES`, `WORD_LIST`, `COLORS` (256-color codes), `STOPWORDS`
  - `SEASONS` dict — 8 holidays (valentine, halloween, xmas, easter, moon, etc.) with date ranges, custom Shibe art paths, and themed word lists. Easter and moon dates are calculated dynamically via `python-dateutil` and `fullmoon`.

- **static/** — Unicode Shibe art files (doge.txt, seasonal variants) loaded via `importlib.resources`

## Code Style

- **pre-commit** hooks: ruff check+format, trailing whitespace, YAML/TOML checks, merge conflict detection
- **Ruff** with `select = ["ALL"]` — very strict linting. Key ignores: `COM812` (trailing commas), `T20` (print statements OK), `D203`/`D213` (docstring style), `S311` (random OK)
- **mypy** strict mode + **ty** for type checking. Stubs for `fullmoon` in `typings/`.
- Python 3.10+ compatibility required (no PEP 695 type syntax — use `TypeVar` instead)
- Build system: Hatchling
- Commit messages use doge-speak ("Wow bamp version", "Much real data wow")
