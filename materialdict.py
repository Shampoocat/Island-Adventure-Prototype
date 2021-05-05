

#This file has been nuked. Maybe this stuff could be put somewhere else.


#class used to look up a neat string to present to the player describing the light level. Could probably be a function in the same vain as the stuff in timefunctions.
class LightLevel:
    light = {
        0: "pitch black",
        1: "barely lit",
        2: "dimly lit",
        3: "adequately lit",
        4: "well lit",

    }


#Class storing info about windows. Provides a name for the player to see and a maximum light level used to determine how will lit an indoor location can be, based on the size of the windows.
class Windows:
    windows = {
        "darkness": {"name": "", "light_level": 0},
        "tiny_windows": {"name": "tiny windows", "light_level": 1},
        "medium_windows": {"name": "medium sized windows", "light_level": 2},
        "large_windows": {"name": "large windows", "light_level": 3},
        "broken_walls": {"name": "broken wall parts", "light_level": 1},
        "roof_hole": {"name": "massive holes in the roof", "light_level": 4},
    }



