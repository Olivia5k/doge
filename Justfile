# Run all checks: fix, type check, and test
check: fix typecheck test

# Auto-fix lint and format issues
fix:
    uv run ruff check --fix .
    uv run ruff format .

# Type check with mypy and ty
typecheck:
    uv run mypy src/doge/
    uv run ty check

# Run tests (pass args like: just test tests/test_doge.py::test_name)
test *args:
    uv run pytest {{ args }}

# Strict lint and format check (no auto-fix, for CI)
ci: lint typecheck test

# Lint and format check (no auto-fix)
lint:
    uv run ruff check .
    uv run ruff format --check .
