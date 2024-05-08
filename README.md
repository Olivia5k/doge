# doge

[![GitHub License](https://img.shields.io/github/license/Olivia5k/doge)](https://github.com/Olivia5k/doge?tab=MIT-1-ov-file#readme)
[![PyPI - Version](https://img.shields.io/pypi/v/doge)][doge_pypi]
[![PyPI - Downloads](https://img.shields.io/pypi/dm/doge)][doge_pypi]
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/doge)][doge_pypi]
[![latest packaged version(s)](https://repology.org/badge/latest-versions/doge.svg?exclude_sources=pypi)][doge_rep]
[![Packaging status](https://repology.org/badge/tiny-repos/doge.svg)][doge_rep]

 [doge_pypi]: https://pypi.org/project/doge/ "doge (PyPI)"
 [doge_rep]:  https://repology.org/project/doge/versions "Versions for doge (Repology)"


![wow screenshot](https://raw.githubusercontent.com/Olivia5k/doge/main/example_doge.png)

**doge** is a simple motd script based on the slightly stupid but very funny
[doge meme][doge]. It prints random grammatically incorrect statements that are
sometimes based on things from your computer.

If you have [pipx][] (you should!), you can try out `doge` without installing
it permanently.\
Just type `pipx run doge` in your terminal to see if you enjoy it. 🐶

## Features

* Randomly placed and colored random strings, complete with broken english.
* Awesome Shibe 😎 in the terminal.
* Fetching of system data, such as hostname, running processes, current user
  and `$EDITOR`.
* If you have [lolcat][], you can do this gem:
  `while true; do doge | lolcat -a -d 100 -s 100 -p 1; done`
  (thx [hom3chuk][])
* stdin support: `ls /usr/bin | doge` will doge-print some of the executables
  found in /usr/bin. wow. There are also multiple command line switches that
  control filtering and statistical frequency of words. See `doge -h`, wow.
  * To use all dictionary words that start or end with "dog", try:\
    `egrep '(^dog|dog$)' /usr/share/dict/words | fgrep -v "'s" | doge`

## Installation

* `pipx install doge` -- this is the recommended method, but you need [pipx][]
  installed and configured.
  * [pipx][] is usually the best way to install and run Python-based
    applications from PyPI, so if you don't yet have it, you should! 👍
  * To install newer versions, run `pipx upgrade doge` or `pipx upgrade-all`.
* Make a Python [zipapp][] with [pex][] or [shiv][], and put it in your
  `$PATH`, for example:
  * `shiv doge -c doge -o ~/bin/doge`
  * `pex doge -c doge -o ~/bin/doge`
* Install with *pip*, see Brett Cannon's
  [A quick-and-dirty guide on how to install packages for Python][install_guide]
  for more information. TLDR; basically use your preferred Python and run:\
  `python3 -m pip install doge`

Then, just add a call to `doge` at the bottom of your shell rc file.

If you don't want to install doge with the options above for whatever reason,
there is a proper `pyproject.toml` included, so inside a virtual
environment, `python -m pip install -e .` should work just fine.

## Notes

You need a terminal that supports 256 colors running on a system that supports
unicode.

The terminal Shibe was created with hax0r Gimp skills and [img2xterm][i2x].

[doge]: http://knowyourmeme.com/memes/doge
[i2x]: https://github.com/rossy2401/img2xterm
[hom3chuk]: https://github.com/hom3chuk
[lolcat]: https://github.com/busyloop/lolcat
[pipx]: https://pipx.pypa.io
[install_guide]: https://snarky.ca/a-quick-and-dirty-guide-on-how-to-install-packages-for-python/
[zipapp]: https://docs.python.org/3/library/zipapp.html
[shiv]: https://github.com/linkedin/shiv
[pex]: https://github.com/pantsbuild/pex
