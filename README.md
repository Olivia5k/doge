doge
====

![wow screenshot](http://i.imgur.com/HxH9qka.png)


**doge** is a simple motd script based on the slightly stupid but very funny
[doge meme][doge]. It prints random grammatically incorrect statements that are
sometimes based on things from your computer.

For more information about getting a setup like the one in the screenshot, see
[this dotfiles repo][shameless].

## Features

* Randomly placed and colored random strings, complete with broken english.
* Awesome Shibe in the terminal.
* Fetching of system data, such as hostname, running processes, current user
  and `$EDITOR`.
* If you have [lolcat][lolcat], you can do this gem:
  `while true; do doge | lolcat -a -d 100 -s 100 -p 1; done`
  (thx [hom3chuk][hom3chuk])
* stdin support: `ls /usr/bin | doge` will doge-print some of the executables
  found in /usr/bin. wow. There are also multiple command line switches that
  control filtering and statistical frequency of words. See `doge -h`, wow.

## Installation

`pip install doge`

If you don't want to do that for whatever reason, there is a proper `setup.py`
included, so `python setup.py install` should be just fine for that.

Note that if you are one of the unlucky doges to still run a Python that does
not have argparse (<=Python2.6) you will have to install argparse manually from
pypi. so old, very update need.

Then, just add a call to `doge` at the bottom of your shell rc file.

## Notes

You need a terminal that supports 256 colors running on a system that supports
unicode.

The terminal Shibe was created with hax0r Gimp skills and [img2xterm][i2x].

[doge]: http://knowyourmeme.com/memes/doge
[i2x]: https://github.com/rossy2401/img2xterm
[hom3chuk]: https://github.com/hom3chuk
[lolcat]: https://github.com/busyloop/lolcat
[shameless]: https://github.com/thiderman/dotfiles
