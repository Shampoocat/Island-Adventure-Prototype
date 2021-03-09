# Island Adventure Prototype


This is a Prototype of a Text based Roguelike game with heavy emphasis on exploration. It is far from feature complete. Currently it includes a procedurally generated island that can be explored and a rudimentary time system. 


It is written in Python and uses the rich (https://github.com/willmcgugan/rich) module.


## How to Run

For Linux(Only tested on Mint) and Windows you can use these executables:
(Note: I do not fully trust pyinstaller so these might be a bit janky. Also your antivirus might go haywire. When in doubt use the script.)

*put exes here*

Alternatively you can just run the python script.

 


Python 3.8 was used to program this game, although I am fairly sure it should work with an up to date version of 3.6.

The rich module is needed for this to run, use:

```
pip install rich
```

To install it.

Then just run the main.py file.


## Roadmap for Future Improvements


Some minor improvements for existing features.

A lot of refactoring.

Objects(Like furniture etc.)

Events and Encounters.

A rework of the world generation, including a better random generator that supports weighted random chances based on circumstances. 

Items, Inventory, Equipment, Crafting, Collecting Resources.
