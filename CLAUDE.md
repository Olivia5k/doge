# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**doge** is a Python CLI tool that prints doge meme-style MOTD messages in the terminal. It displays a Unicode Shibe with randomly placed, colored, grammatically incorrect phrases based on system information or piped stdin. Requires a UTF-8 capable terminal with 256-color support.

## Development Commands

```bash
uv sync                  # Install/sync dependencies
uv run doge              # Run the application
uv run ruff check .      # Lint (uses ALL rules with specific ignores)
uv run ruff format .     # Format code
uv run ruff check --fix .  # Auto-fix lint issues
```

```bash
uv run pytest              # Run all tests
uv run pytest tests/test_doge.py::test_name  # Run a single test
```

## Architecture

The codebase lives in `src/doge/` with three modules:

- **core.py** — Main application logic. Key classes:
  - `TTYHandler` — Terminal detection (dimensions, color support, platform)
  - `Doge` — Orchestrator: parses args, loads Shibe art, collects words (system data or stdin), places colored text on random lines
  - `DogeMessage` — Formats individual messages with random prefix/suffix, ANSI 256-color, and spacing
  - `main()` — Entry point (`doge = "doge.core:main"` in pyproject.toml) with UTF-8/locale error handling

- **wow.py** — Data and word collections:
  - `DogeDeque` / `FrequencyBasedDogeDeque` — Custom deques that shuffle and rotate for non-repetitive random word selection
  - Static data: `PREFIXES`, `SUFFIXES`, `WORD_LIST`, `COLORS` (256-color codes), `STOPWORDS`
  - `SEASONS` dict — 8 holidays (valentine, halloween, xmas, easter, moon, etc.) with date ranges, custom Shibe art paths, and themed word lists. Easter and moon dates are calculated dynamically via `python-dateutil` and `fullmoon`.

- **static/** — Unicode Shibe art files (doge.txt, seasonal variants) loaded via `importlib.resources`

## Code Style

- **Ruff** with `select = ["ALL"]` — very strict linting. Key ignores: `COM812` (trailing commas), `T20` (print statements OK), `D203`/`D213` (docstring style), `S311` (random OK)
- Python 3.9+ compatibility required
- Build system: Hatchling
- Commit messages use doge-speak ("Wow bamp version", "Much real data wow")
