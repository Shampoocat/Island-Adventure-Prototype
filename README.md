# Island Adventure Prototype


This is a Prototype of a Text based Roguelike game with heavy emphasis on exploration. It is far from feature complete. Currently it includes a procedurally generated island that can be explored and a rudimentary time system. 


It is written in Python and uses the rich (https://github.com/willmcgugan/rich) module.


## How to Run

For Linux(Only tested on Mint) and Windows you can use these executables:

(Note: I do not fully trust pyinstaller so these might be a bit janky. Also your antivirus might go haywire. When in doubt use the script.)

https://github.com/Shampoocat/Island-Adventure-Prototype/releases/tag/0.2


Alternatively you can just run the python script.

 


Python 3.8 was used to program this game, although I am fairly sure it should work with an up to date version of 3.6.

The rich module is needed for this to run, use:

```
pip install rich
```

To install it.

Then just run the main.py file.

## Changelog

(Mar 9, 2021) 0.1:

Initial Release.

(May 5, 2021) 0.2:

New way of handling data for locations.

Rework of the Textgenerator.

Added basic Objects.

Reworked how steps are shown to the player.

Some more minor stuff.


## Roadmap for Future Development



A lot of refactoring.(mostly done)

Objects(Like furniture etc.)(basics are in place, just not much interaction as of now)

Character stats.

Events and Encounters.

A rework of the world generation, including a better random generator that supports weighted random chances based on circumstances. 

Items, Inventory, Equipment, Crafting, Collecting Resources.
