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
