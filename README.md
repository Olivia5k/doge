doge
====

![wow screenshot](http://i.imgur.com/kBeMBRo.png)


**doge** is a simple motd script based on the slightly stupid but very funny
[doge meme][doge]. It prints random grammatically incorrect statements that are
sometimes based on things from your computer.

## Features

* Randomly placed and colored random strings, complete with broken english.
* Awesome Shibe in the terminal.
* Fetching of system data, such as hostname, running processes, current user
  and `$EDITOR`.
* If you have [lolcat][lolcat], you can do this gem:
  `while true; do doge | lolcat -a -d 100 -s 100 -p 1; done`
  (thx [hom3chuk][hom3chuk])

## Installation

`pip install doge`

If you don't want to do that for whatever reason, there is a proper `setup.py`
included, so `python setup.py install` should be just fine for that.

Then, just add a call to `doge` at the bottom of your shell rc file.

## Notes

**doge** optionally requires the `ps` binary on your path to be able to show
processes. If you don't have `ps`, chances are that **doge** won't run anyway.
Oh, and you need a terminal that supports 256 colors, but that should not be
a problem given that is, you know, 2013.

The terminal Shibe was created with hax0r Gimp skills and [img2xterm][i2x].

[doge]: http://knowyourmeme.com/memes/doge
[i2x]: https://github.com/rossy2401/img2xterm
[hom3chuk]: https://github.com/hom3chuk
[lolcat]: https://github.com/busyloop/lolcat
