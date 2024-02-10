#!/usr/bin/env python

# Copyright (C) 2013-2024 Olivia Thiderman

"""Wow print Shibe to terminal, such random words."""

import argparse
import datetime
import os
import random
import re
import shutil
import subprocess as sp
import sys
import traceback
import unicodedata
from importlib.resources import files

import dateutil.tz

from doge import wow

ROOT = files("doge").joinpath("static")
DEFAULT_DOGE = "doge.txt"


class Doge:
    """Make Shibe and pretty random words."""

    MAX_PERCENT = 100
    MIN_PS_LEN = 2

    def __init__(self, tty, ns):
        self.tty = tty
        self.ns = ns
        self.lines = []
        self.doge_path = ROOT.joinpath(ns.doge_path or DEFAULT_DOGE)
        if ns.frequency:
            # such frequency based
            self.words = wow.FrequencyBasedDogeDeque(*wow.WORD_LIST, step=ns.step)
        else:
            self.words = wow.DogeDeque(*wow.WORD_LIST)

    def setup(self):
        """Check args and seasons, load data, and decorate shibe."""
        # Setup seasonal data
        self.setup_seasonal()

        if self.tty.pretty:
            # stdout is a tty, load Shibe and calculate how wide he is
            doge = self.load_doge()
            max_doge = max(map(clean_len, doge)) + 15
        else:
            # stdout is being piped and we should not load Shibe
            doge = []
            max_doge = 15

        if self.ns.density > self.MAX_PERCENT:
            sys.stderr.write("wow, density such over 100%, too high\n")
            sys.exit(1)

        if self.ns.density < 0:
            sys.stderr.write("wow, density such negative, too low\n")
            sys.exit(1)

        if self.tty.width < max_doge:
            # Shibe won't fit, so abort.
            sys.stderr.write("wow, such small terminal\n")
            sys.stderr.write(f"no doge under {max_doge} column\n")
            return False

        # Check for prompt height so that we can fill the screen minus how high
        # the prompt will be when done.
        prompt = os.environ.get("PS1", "").split("\n")
        line_count = len(prompt) + 1

        # Create a list filled with empty lines and Shibe at the bottom.
        fill = range(self.tty.height - len(doge) - line_count)
        self.lines = ["\n" for x in fill]
        self.lines += doge

        # Try to fetch data fed thru stdin
        had_stdin = self.get_stdin_data()

        # Get some system data, but only if there was nothing in stdin
        if not had_stdin:
            self.get_real_data()

        # Apply the text around Shibe
        self.apply_text()
        return True

    def setup_seasonal(self):
        """Handle seasonal holidays.

        Check if there's some seasonal holiday going on, setup appropriate
        Shibe picture and load holiday words.

        Note: if there are two or more holidays defined for a certain date,
        the first one takes precedence.
        """
        # If we've specified a season, just run that one
        if self.ns.season:
            return self.load_season(self.ns.season)

        # If we've specified another doge or no doge at all, it does not make
        # sense to use seasons.
        if self.ns.doge_path is not None and not self.ns.no_shibe:
            return None

        tz = dateutil.tz.tzlocal()
        now = datetime.datetime.now(tz=tz)

        for season, data in wow.SEASONS.items():
            start, end = data["dates"]
            start_dt = datetime.datetime(now.year, start[0], start[1], tzinfo=tz)

            # Be sane if the holiday season spans over New Year's day.
            end_dt = datetime.datetime(
                now.year + ((start[0] > end[0] and 1) or 0), end[0], end[1], tzinfo=tz
            )

            if start_dt <= now <= end_dt:
                # Wow, much holiday!
                return self.load_season(season)
        return None

    def load_season(self, season_key):
        """Try to load a season, unless 'none' given."""
        if season_key == "none":
            return

        season = wow.SEASONS[season_key]
        self.doge_path = ROOT.joinpath(season["pic"])
        self.words.extend(season["words"])

    def apply_text(self):
        """Apply text around doge."""
        # Calculate a random sampling of lines that are to have text applied
        # onto them. Return value is a sorted list of line index integers.
        linelen = len(self.lines)

        if self.ns.density == 0:
            return

        affected = sorted(
            random.sample(range(linelen), int(linelen * (self.ns.density / 100)))
        )

        for i, target in enumerate(affected, start=1):
            line = self.lines[target]
            line = re.sub("\n", " ", line)

            word = self.words.get()

            # If first or last line, or a random selection, use standalone wow.
            if i == 1 or i == len(affected) or random.choice(range(20)) == 0:
                word = "wow"

            # Generate a new DogeMessage, possibly based on a word.
            self.lines[target] = DogeMessage(self, line, word).generate()

    def load_doge(self):
        """Return pretty ASCII Shibe.

        wow
        """
        if self.ns.no_shibe:
            return [""]

        return self.doge_path.read_text(encoding="utf-8").splitlines(keepends=True)

    def get_real_data(self):
        """Grab actual data from the system."""
        ret = []
        username = os.environ.get("USER")
        if username:
            ret.append(username)

        editor = os.environ.get("EDITOR")
        if editor:
            editor = editor.split("/")[-1]
            ret.append(editor)

        # OS, hostname and... architecture (because lel)
        if hasattr(os, "uname"):
            uname = os.uname()
            ret.extend((uname[0], uname[1], uname[4]))

        # Grab actual files from $HOME.
        filenames = os.listdir(os.environ.get("HOME"))
        if filenames:
            ret.append(random.choice(filenames))

        # Grab some processes
        ret += self.get_processes()[:2]

        # Prepare the returned data. First, lowercase it.
        self.words.extend(map(str.lower, ret))

    @staticmethod
    def filter_words(words, stopwords, min_length):
        """Filter out unwanted words."""
        return [
            word for word in words if len(word) >= min_length and word not in stopwords
        ]

    def get_stdin_data(self):
        """Get words from stdin."""
        if self.tty.in_is_tty:
            # No pipez found
            return False

        stdin_lines = (line for line in sys.stdin.readlines())

        rx_word = re.compile(r"\w+", re.UNICODE)

        # If we have stdin data, we should remove everything else!
        self.words.clear()
        word_list = [
            match.group(0)
            for line in stdin_lines
            for match in rx_word.finditer(line.lower())
        ]
        if self.ns.filter_stopwords:
            word_list = self.filter_words(
                word_list, stopwords=wow.STOPWORDS, min_length=self.ns.min_length
            )

        self.words.extend(word_list)

        return True

    def get_processes(self):
        """Grab a shuffled list of all currently running process names."""
        procs = set()

        try:
            # POSIX ps, so it should work in most environments where doge would
            p = sp.Popen(["ps", "-A", "-o", "comm="], stdout=sp.PIPE)
            output, _error = p.communicate()

            output = output.decode("utf-8")

            for comm in output.split("\n"):
                name = comm.split("/")[-1]
                # Filter short and weird ones
                if name and len(name) >= self.MIN_PS_LEN and ":" not in name:
                    procs.add(name)

        finally:
            # Either it executed properly or no ps was found.
            proc_list = list(procs)
            random.shuffle(proc_list)
            return proc_list

    def print_doge(self):
        """Print doge to terminal."""
        for line in self.lines:
            sys.stdout.write(line)
        sys.stdout.flush()


class DogeMessage:
    """Make a randomly placed and randomly colored message."""

    def __init__(self, doge, occupied, word):
        self.doge = doge
        self.tty = doge.tty
        self.occupied = occupied
        self.word = word

    def generate(self):
        """Add a word to a line, with color, random prefix and suffix."""
        if self.word == "wow":
            # Standalone wow. Don't apply any prefixes or suffixes.
            msg = self.word
        else:
            # Add a prefix.
            msg = f"{wow.PREFIXES.get()} {self.word}"

            # Seldomly add a suffix as well.
            if random.choice(range(15)) == 0:
                msg += f" {wow.SUFFIXES.get()}"

        # Calculate the maximum possible spacer
        interval = self.tty.width - onscreen_len(msg)
        interval -= clean_len(self.occupied)

        if interval < 1:
            # The interval is too low, so the message can not be shown without
            # spilling over to the subsequent line, borking the setup.
            # Return the doge slice that was in this row if there was one,
            # and a line break, effectively disabling the row.
            return self.occupied + "\n"

        # Apply spacing
        msg = "{}{}".format(" " * random.choice(range(interval)), msg)

        if self.tty.pretty:
            # Apply pretty ANSI color coding.
            msg = f"\x1b[1m\x1b[38;5;{wow.COLORS.get()}m{msg}\x1b[39m\x1b[0m"

        # Line ends are pretty cool guys, add one of those.
        return f"{self.occupied}{msg}\n"


class TTYHandler:
    """Get terminal properties."""

    def __init__(self):
        self.height = 25
        self.width = 80
        self.in_is_tty = True
        self.out_is_tty = True
        self.pretty = True

    def setup(self):
        """Calculate terminal properties."""
        self.width, self.height = shutil.get_terminal_size()
        self.in_is_tty = sys.stdin.isatty()
        self.out_is_tty = sys.stdout.isatty()

        self.pretty = self.out_is_tty
        if sys.platform == "win32" and os.getenv("TERM") == "xterm":
            self.pretty = True


def clean_len(s):
    """Calculate the length of a string without its color codes."""
    s = re.sub(r"\x1b\[[0-9;]*m", "", s)

    return len(s)


def onscreen_len(s):
    """Calculate the length of a unicode string on screen.

    Also account for double-width characters.
    """
    length = 0
    for ch in s:
        length += 2 if unicodedata.east_asian_width(ch) == "W" else 1

    return length


def setup_arguments():
    """Make an ArgumentParser."""
    parser = argparse.ArgumentParser("doge")

    parser.add_argument(
        "--shibe",
        help="wow shibe file",
        dest="doge_path",
        choices=[file.name for file in ROOT.iterdir()],
    )

    parser.add_argument("--no-shibe", action="store_true", help="wow no doge show :(")

    parser.add_argument(
        "--season",
        help="wow shibe season congrate",
        choices=[*sorted(wow.SEASONS.keys()), "none"],
    )

    parser.add_argument(
        "-f", "--frequency", help="such frequency based", action="store_true"
    )

    parser.add_argument(
        "--step",
        help="beautiful step",  # how much to step
        #  between ranks in FrequencyBasedDogeDeque
        type=int,
        default=2,
    )

    parser.add_argument(
        "--min_length",
        help="pretty minimum",  # minimum length of a word
        type=int,
        default=1,
    )

    parser.add_argument(
        "-s", "--filter_stopwords", help="many words lol", action="store_true"
    )

    parser.add_argument(
        "-mh",
        "--max-height",
        help="such max height",
        type=int,
    )

    parser.add_argument(
        "-mw",
        "--max-width",
        help="such max width",
        type=int,
    )

    parser.add_argument(
        "-d",
        "--density",
        help="such word density percent, max is 100, default is 30, wow",
        type=float,
        default=30,
    )
    return parser


def main():
    """Run the main CLI script."""
    tty = TTYHandler()
    tty.setup()

    parser = setup_arguments()
    ns = parser.parse_args()
    if ns.max_height:
        tty.height = ns.max_height
    if ns.max_width:
        tty.width = ns.max_width

    try:
        shibe = Doge(tty, ns)
        if not shibe.setup():
            # We assume that setup() prints what went wrong.
            return 1
        shibe.print_doge()

    except (UnicodeEncodeError, UnicodeDecodeError):
        # Some kind of unicode error happened. This is usually because the
        # users system does not have a proper locale set up. Try to be helpful
        # and figure out what could have gone wrong.
        traceback.print_exc()
        print()

        lang = os.environ.get("LANG")
        if not lang:
            print("wow error: broken $LANG, so fail")
            return 3

        if not lang.endswith("UTF-8"):
            print(
                f"wow error: locale '{lang}' is not UTF-8.  doge needs UTF-8 to "
                "print Shibe. Please set your system to use a UTF-8 locale."
            )
            return 2

        print(
            "wow error: Unknown unicode error.  Please report at "
            "https://github.com/thiderman/doge/issues and include output from "
            "/usr/bin/locale"
        )
        return 1
    return 0


# wow very main
if __name__ == "__main__":
    sys.exit(main())
