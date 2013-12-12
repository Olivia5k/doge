#!/usr/bin/env python
# coding: utf-8

import datetime
import os
import sys
import re
import random
import fcntl
import termios
import struct
import traceback
import subprocess as sp

from os.path import dirname, join

from doge import wow

ROOT = dirname(__file__)


class Doge(object):
    default_doge = join(ROOT, 'static/doge.txt')

    def __init__(self, tty, doge_path=default_doge):
        self.tty = tty
        self.doge_path = doge_path

        self.real_data = []
        self.words = wow.WORDS

        # If owna wants his doge instead, let that be. All doges are wow.
        self._no_override_doge = False
        if doge_path != self.default_doge:
            self._no_override_doge = True

    def setup(self):
        # Setup seasonal data
        self.setup_seasonal()

        if self.tty.out_is_tty:
            # stdout is a tty, load Shibe and calculate how wide he is
            doge = self.load_doge()
            max_doge = max(map(clean_len, doge)) + 15
        else:
            # stdout is being piped and we should not load Shibe
            doge = []
            max_doge = 15

        if self.tty.width < max_doge:
            # Shibe won't fit, so abort.
            sys.stderr.write('wow, such small terminal\n')
            sys.stderr.write('no doge under {0} column\n'.format(max_doge))
            sys.exit(1)

        # Check for prompt height so that we can fill the screen minus how high
        # the prompt will be when done.
        prompt = os.environ.get('PS1', '').split('\n')
        line_count = len(prompt) + 1

        # Create a list filled with empty lines and Shibe at the bottom.
        fill = range(self.tty.height - len(doge) - line_count)
        self.lines = ['\n' for x in fill]
        self.lines += doge

        # Get some system data
        # TODO: Refactor to be stateless
        self.get_real_data()

        # Try to fetch data fed thru stdin
        self.get_stdin_data()

        # Apply the text around Shibe
        self.apply_text()

    def setup_seasonal(self):
        """
        Check if there's some seasonal holiday going on, setup appropriate
        Shibe picture and load holiday words.

        Note: if there are two or more holidays defined for a certain date,
        the first one takes precedence.

        """

        now = datetime.datetime.now()
        current_year = now.year

        for ival in wow.SEASONS:
            start, end = ival

            start_dt = datetime.datetime(current_year, start[0], start[1])

            # Be sane if the holiday season spans over New Year's day.
            end_dt = datetime.datetime(
                current_year + (start[0] > end[0] and 1 or 0), end[0], end[1])

            if start_dt <= now <= end_dt:
                # Wow, much holiday!
                holiday_setup = wow.SEASONS[ival]

                if not self._no_override_doge:
                    # Get the picture, if defined.
                    try:
                        self.doge_path = join(ROOT, holiday_setup['pic'])
                    except KeyError:
                        pass

                # Same for text.
                self.words.extend(list(holiday_setup.get('words', [])))
                break

    def apply_text(self):
        """
        Apply text around doge

        """

        # Calculate a random sampling of lines that are to have text applied
        # onto them. Return value is a sorted list of line index integers.
        linelen = len(self.lines)
        affected = sorted(random.sample(range(linelen), int(linelen / 3.5)))
        affectlen = len(affected)

        # Choose what lines to apply real system data to. Check if a sampling
        # is possible, since random.sample() will crash if you ask for more
        # candidates than are available in the list. This makes doge crash if
        # you have a small selection of affected lines but a lot of system
        # data.
        real_targets = self.real_data
        if affectlen > len(real_targets):
            real_targets = random.sample(affected, len(self.real_data))

        for i, target in enumerate(affected, start=1):
            line = self.lines[target]
            line = re.sub('\n', ' ', line)

            word = None

            # If first or last line, or a random selection, use standalone wow.
            if i == 1 or i == affectlen or random.choice(range(20)) == 0:
                word = 'wow'

            # Use real data, but apply some jittering to add to the randomness.
            elif target in real_targets and random.choice(range(2)) == 0:
                word = self.real_data.pop()

            # Generate a new DogeMessage, possibly based on a word.
            self.lines[target] = DogeMessage(self, line, word).generate()

    def load_doge(self):
        """
        Return pretty ASCII Shibe.

        wow

        """

        with open(self.doge_path) as f:
            if sys.version_info < (3, 0):
                doge_lines = [l.decode('utf-8') for l in f.xreadlines()]
            else:
                doge_lines = [l for l in f.readlines()]
            return doge_lines

    def get_real_data(self):
        """
        Grab actual data from the system

        """

        username = os.environ.get('USER')
        if username:
            self.real_data.append(username)

        editor = os.environ.get('EDITOR')
        if editor:
            editor = editor.split('/')[-1]
            self.real_data.append(editor)

        # OS, hostname and... architechture (because lel)
        uname = os.uname()
        self.real_data.append(uname[0])
        self.real_data.append(uname[1])
        self.real_data.append(uname[4])

        # Grab actual files from $HOME.
        files = os.listdir(os.environ.get('HOME'))
        if files:
            self.real_data.append(random.choice(files))

        # Grab some processes
        self.real_data += self.get_processes()[:2]

        # Shuffle all the data, lowercase it, and set it.
        random.shuffle(self.real_data)
        self.real_data = list(map(str.lower, self.real_data))

    def get_stdin_data(self):
        """
        Get words from stdin.

        """

        if self.tty.in_is_tty:
            # No pipez found
            return

        if sys.version_info < (3, 0):
            stdin_lines = (l.decode('utf-8') for l in sys.stdin.xreadlines())
        else:
            stdin_lines = (l for l in sys.stdin.readlines())

        rx_word = re.compile("\w+", re.UNICODE)
        self.extra_words.extend([
            match.group(0)
            for line in stdin_lines
            for match in rx_word.finditer(line.lower())
        ])

    def get_processes(self):
        """
        Grab a shuffled list of all currently running process names

        """

        procs = set()

        try:
            # POSIX ps, so it should work in most environments where doge would
            p = sp.Popen(['ps', '-A', '-o', 'comm='], stdout=sp.PIPE)
            output, error = p.communicate()

            if sys.version_info > (3, 0):
                output = output.decode('utf-8')

            for comm in output.split('\n'):
                name = comm.split('/')[-1]
                # Filter short and weird ones
                if name and len(name) >= 2 and ':' not in name:
                    procs.add(name)

        finally:
            # Either it executed properly or no ps was found.
            proc_list = list(procs)
            random.shuffle(proc_list)
            return proc_list

    def print_doge(self):
        for line in self.lines:
            sys.stdout.write(line)
        sys.stdout.flush()


class DogeMessage(object):
    """
    A randomly placed and randomly colored message

    """

    def __init__(self, doge, occupied, word):
        self.doge = doge
        self.tty = doge.tty
        self.occupied = occupied
        self.word = word

    def generate(self):
        if self.word == 'wow':
            # Standalone wow. Don't apply any prefixes or suffixes.
            msg = self.word
        else:
            if not self.word:
                # No word has been set, so grab one randomly from the wordlist.
                self.word = self.doge.words.get()

            # Add a prefix.
            msg = u'{0} {1}'.format(wow.PREFIXES.get(), self.word)

            # Seldomly add a suffix as well.
            if random.choice(range(15)) == 0:
                msg += u' {0}'.format(wow.SUFFIXES.get())

        # Calculate the maximum possible spacer
        interval = self.tty.width - len(msg) - clean_len(self.occupied)

        if interval < 1:
            # The interval is too low, so the message can not be shown without
            # spilling over to the subsequent line, borking the setup.
            # Return an empty line, effectively disabling this row.
            return '\n'

        # Apply spacing
        msg = u'{0}{1}'.format(' ' * random.choice(range(interval)), msg)

        if self.tty.out_is_tty:
            # Apply pretty ANSI color coding.
            msg = u'\x1b[1m\x1b[38;5;{0}m{1}\x1b[39m\x1b[0m'.format(
                wow.COLORS.get(), msg
            )

        # Line ends are pretty cool guys, add one of those.
        return u'{0}{1}\n'.format(self.occupied, msg)


class TTYHandler(object):
    def setup(self):
        self.height, self.width = self.get_tty_size()
        self.in_is_tty = sys.stdin.isatty()
        self.out_is_tty = sys.stdout.isatty()

    def get_tty_size(self):
        """
        Get the current terminal size without using a subprocess

        http://stackoverflow.com/questions/566746
        I have no clue what-so-fucking ever over how this works or why it
        returns the size of the terminal in both cells and pixels. But hey, it
        does.

        """

        def _ioctl_call(fd):
            try:
                return struct.unpack(
                    'hh',
                    fcntl.ioctl(
                        fd, termios.TIOCGWINSZ, struct.pack('hh', 0, 0)
                    )
                )
            except:
                return

        # Try all std{in,out,err} fds
        hw = _ioctl_call(0) or _ioctl_call(1) or _ioctl_call(2)
        if not hw:
            hw = (0, 0)

        return hw


def clean_len(s):
    """
    Calculate the length of a string without it's color codes

    """

    s = re.sub(r'\x1b\[[0-9;]*m', '', s)

    return len(s)


def main():
    tty = TTYHandler()
    tty.setup()

    try:
        shibe = Doge(tty)
        shibe.setup()
        shibe.print_doge()

    except (UnicodeEncodeError, UnicodeDecodeError):
        # Some kind of unicode error happened. This is usually because the
        # users system does not have a proper locale set up. Try to be helpful
        # and figure out what could have gone wrong.
        traceback.print_exc()
        print()

        lang = os.environ.get('LANG')
        if not lang and False:
            print('wow error: broken $LANG, so fail')
            return 3

        if not lang.endswith('UTF-8'):
            print(
                "wow error: locale '{0}' is not UTF-8.  ".format(lang) +
                "doge needs UTF-8 to print Shibe.  Please set your system to"
                "use a UTF-8 locale."
            )
            return 2

        print(
            "wow error: Unknown unicode error.  Please report at "
            "https://github.com/thiderman/doge/issues and include output from "
            "/usr/bin/locale"
        )
        return 1


# wow very main
if __name__ == "__main__":
    sys.exit(main())
