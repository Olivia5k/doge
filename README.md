doge
====

![wow screenshot](http://i.imgur.com/Z2EoUmn.png)


**doge** is a simple motd script based on the slightly retarded but very funny
[doge meme][doge]. It prints random grammatically incorrect statements that are
sometimes based on things from your computer.

## Features

* Randomly placed and colored random strings, complete with broken english.
* Awesome Shibe in the terminal.
* Fetching of system data, such as hostname, current user and `$EDITOR`.
* If you have [lolcat][lolcat], you can do this gem: `while true; do doge | lolcat -a -d 100 -s 100 -p 1; done`
  (thx [hom3chuk][hom3chuk])

## Installation

It's on PyPi, so `pip install doge` should be just fine. If you don't want to
do that for whatever reason, there is a `setup.py` included, so `python
setup.py install` should be just fine for that.

## Notes

To run, **doge** requires the `stty` binary on your path because of lazy, and
a terminal that supports 256 colors. Other than that, it just uses the Python
stdlib.

The terminal Shibe was created with hax0r Gimp skills and [img2xterm][i2x]

[doge]: http://knowyourmeme.com/memes/doge
[i2x]: https://github.com/rossy2401/img2xterm
[hom3chuk]: https://github.com/hom3chuk
[lolcat]: https://github.com/busyloop/lolcat
