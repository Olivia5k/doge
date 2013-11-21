#!/usr/bin/env python
# coding: utf-8

import os
import sys
import re
import random
import fcntl
import termios
import struct
import subprocess as sp

from os.path import dirname, join
from os import environ

from doge import wow

ROOT = dirname(__file__)


class Doge(object):
    default_doge = join(ROOT, 'static/doge.txt')

    def __init__(self, tty, doge_path=default_doge):
        self.tty = tty
        self.doge_path = doge_path

        self.real_data = []

    def setup(self):
        if self.tty.is_tty:
            # is tty, wow get doge
            doge = self.load_doge()
            max_doge = max(map(clean_len, doge)) + 15
        else:
            # no tty, such no doge
            doge = []
            max_doge = 15

        if self.tty.width < max_doge:
            sys.stderr.write('wow, such small terminal\n')
            sys.stderr.write('no doge under {0} column\n'.format(max_doge))
            sys.exit(1)

        # so many line
        ps1 = environ.get('PS1', '')
        lines = ps1.split('\n')
        line_count = len(lines) + 1

        self.lines = ['\n' for x in
                      range(self.tty.height - len(doge) - line_count)]
        self.lines += doge

        self.get_real_data()
        self.apply_text()

    def apply_text(self):
        linelen = len(self.lines)
        affected = random.sample(range(linelen), int(linelen / 3.5))

        real_targets = self.real_data
        # wow only sample if more than need
        if len(affected) > len(real_targets):
            real_targets = random.sample(affected, len(self.real_data))

        for x in affected:
            line = self.lines[x]
            line = re.sub('\n', ' ', line)

            word = None
            if x in real_targets and random.choice(range(2)) == 0:
                word = self.real_data.pop()
            elif x in affected[-2:]:
                word = 'wow'

            msg = DogeMessage(self.tty, clean_len(line), word=word)
            self.lines[x] = '{0}{1}'.format(line, msg)

    def load_doge(self):
        with open(self.doge_path) as f:
            return f.readlines()

    def get_real_data(self):
        username = os.environ.get('USER')
        if username:
            self.real_data.append(username)

        editor = os.environ.get('EDITOR')
        if editor:
            editor = editor.split('/')[-1]
            self.real_data.append(editor)

        uname = os.uname()
        self.real_data.append(uname[0])
        self.real_data.append(uname[1])
        self.real_data.append(uname[4])  # lel

        # much functional
        files = filter(
            lambda s: s[0] != '.', os.listdir(os.environ.get('HOME'))
        )
        files = list(files)

        # wow so many file
        if files:
            self.real_data.append(random.choice(files))

        for proc in self.get_processes():
            if proc in wow.KNOWN_PROCESSES:
                self.real_data.append(proc)
                break

        random.shuffle(self.real_data)
        self.real_data = list(map(str.lower, self.real_data))

    def get_processes(self):
        procs = set()

        try:
            p = sp.Popen(['ps', '-A', '-o', 'comm='], stdout=sp.PIPE)
            output, error = p.communicate()

            if sys.version_info > (3, 0):
                output = output.decode('utf-8')

            for comm in output.split('\n'):
                name = comm.split('/')[-1]
                if name:
                    procs.add(name)

        finally:
            # wow no ps or many error
            proc_list = list(procs)
            random.shuffle(proc_list)
            return proc_list

    def generate(self):
        for line in self.lines:
            sys.stdout.write(line)
        sys.stdout.flush()


class DogeMessage(object):
    def __init__(self, tty, occupied, word=None):
        self.tty = tty
        self.occupied = occupied
        self.word = word

        self.message = ""

    def __str__(self):
        # such lazy fallback
        if not self.message:
            self.generate()
            self.colorize()
            self.displace()

        # wow need line end
        return self.message + '\n'

    def __repr__(self):
        return self.__str__()

    def displace(self):
        interval = self.tty.width - len(self.orig_message) - self.occupied

        # wow don't fit
        if interval < 1:
            self.message = ''
            return

        space = ' ' * random.choice(range(interval))
        self.message = '{0}{1}'.format(space, self.message)

    def generate(self):
        if self.word == 'wow':
            # wow standalone wow
            msg = self.word
        else:
            if not self.word:
                self.word = random.choice(wow.WORDS)

            msg = '{0} {1}'.format(random.choice(wow.PREFIXES), self.word)

            if random.choice(range(15)) == 0:
                msg += ' {0}'.format(random.choice(wow.SUFFIXES))

        self.orig_message = msg
        self.message = msg

    def colorize(self):
        # wow piped
        if not self.tty.is_tty:
            return

        # very ansi code wow
        self.message = '[1m[38;5;{0}m{1}[39m[0m'.format(
            random.choice(wow.COLORS), self.message
        )


class TTYHandler(object):
    def setup(self):
        self.height, self.width = self.get_tty_size()
        self.is_tty = sys.stdout.isatty()

    def get_tty_size(self):
        # http://stackoverflow.com/questions/566746
        # lol no idea what actually happen
        h, w, hp, wp = struct.unpack(
            'HHHH',
            fcntl.ioctl(
                0, termios.TIOCGWINSZ, struct.pack('HHHH', 0, 0, 0, 0)
            )
        )
        return h, w


def clean_len(s):
    # wow encoding trouble
    # such 2013
    if sys.version_info < (3, 0):
        s = s.decode('utf-8')

    s = re.sub(r'\[[0-9;]*m', '', s)

    return len(s)


def main():
    tty = TTYHandler()
    tty.setup()

    shibe = Doge(tty)
    shibe.setup()
    shibe.generate()

# wow very main
if __name__ == "__main__":
    sys.exit(main())
