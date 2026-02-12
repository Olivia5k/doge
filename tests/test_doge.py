"""Smoke tests for doge CLI."""

import subprocess
import sys

import pytest

SEASONS = [
    "valentine",
    "halloween",
    "thanksgiving",
    "xmas",
    "easter",
    "earth",
    "kabosu",
    "moon",
]


def run_doge(*args, stdin_data=None):
    """Run doge as a subprocess and return the result."""
    cmd = [sys.executable, "-m", "doge", "--max-height", "20", "--max-width", "80"]
    cmd.extend(args)
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        input=stdin_data,
        timeout=10,
    )


def test_basic_run():
    """Doge runs and produces output."""
    result = run_doge("--no-shibe")
    assert result.returncode == 0
    assert len(result.stdout) > 0


def test_frequency_mode():
    """Frequency-based word selection works."""
    result = run_doge("--no-shibe", "-f")
    assert result.returncode == 0
    assert len(result.stdout) > 0


@pytest.mark.parametrize("season", [*SEASONS, "none"])
def test_season(season):
    """Each season flag works without error."""
    result = run_doge("--no-shibe", "--season", season)
    assert result.returncode == 0


def test_custom_density():
    """Custom density produces output."""
    result = run_doge("--no-shibe", "--density", "50")
    assert result.returncode == 0
    assert len(result.stdout) > 0


def test_zero_density():
    """Zero density produces only blank lines."""
    result = run_doge("--no-shibe", "--density", "0")
    assert result.returncode == 0
    # All lines should be blank (whitespace only)
    for line in result.stdout.splitlines():
        assert line.strip() == ""


def test_stdin_piping():
    """Piped stdin words are picked up."""
    result = run_doge("--no-shibe", stdin_data="hello world\n")
    assert result.returncode == 0
    assert len(result.stdout) > 0


def test_empty_stdin():
    """Empty piped stdin still produces wow lines."""
    result = run_doge("--no-shibe", stdin_data="")
    assert result.returncode == 0
    assert "wow" in result.stdout.lower()


def test_stdin_all_stopwords():
    """Stdin where all words are filtered out still produces wow lines."""
    result = run_doge("--no-shibe", "-s", stdin_data="the a an\n")
    assert result.returncode == 0
    assert "wow" in result.stdout.lower()


def test_invalid_density():
    """Density over 100 exits with error."""
    result = run_doge("--density", "200")
    assert result.returncode == 1
    assert "density" in result.stderr.lower()
