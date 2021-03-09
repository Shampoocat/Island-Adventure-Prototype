import random



#This function returns a prefix from the prefix lists in the ConstructionMaterials class, to be used in the text generator. It will work for both construction and natural materials.
#The Index and plural values are stored in the damages dict of the ConstructionMaterials/NaturalMaterials class.
#This function can not get these values from the dict. This should be refactored so this function looks them up in the dict with just the damage being the only input.
def return_damage_prefixes(index, plural):
    if not plural:
        return ConstructionMaterials.damage_prefixes_singular[index]
    else:
        return ConstructionMaterials.damage_prefixes_plural[index]



#These two functions return an appropriate type of damage for a material. It is used by the calculate_construction_damage/calculate_natural_material_damage functions of the
#worldbuilder, when ever a new location is generated.
def return_construction_damage(material):
    material = ConstructionMaterials.materials.get(material)
    damages = material.get("damages")
    return random.choice(damages)


def return_natural_material_damage(material):
    material = NaturalMaterials.materials.get(material)
    damages = material.get("damages")
    return random.choice(damages)



#This class stores all information regarding construction materials, also has the damage prefixes for some reason, I do not remember why I put them there. Might be laziness.
class ConstructionMaterials:

    #Every material has a name to be displayed, a bool determining if it is plural or singular(the text generator needs this) and a list of damages that can be applied by the world generator
    #I plan on expanding this dict to eventually include things like harvestable resources comfort ratings etc.
    materials = {"concrete": {"name": "Concrete", "plural": False, "damages": ["exposed_rebar", "cracked", "degraded", "washed_out"]},
                 "wood": {"name": "Wood", "plural": False, "damages": ["rotten", "moldy", "degraded", "washed_out"]},
                 "metal": {"name": "Metal", "plural": False, "damages": ["rust"]},
                 "ceramic_tiles": {"name": "Ceramic Tiles", "plural": True, "damages": ["cracked", "degraded"]},
                 "wooden_panels": {"name": "Wooden Panels", "plural": True, "damages": ["moldy", "rotten", "degraded"]},
                 "wooden_bars": {"name": "Wooden Poles", "plural": True, "damages": ["moldy", "rotten", "degraded"]},
                 "metal_bars": {"name": "Metal Bars", "plural": True, "damages": ["rust", "degraded", "washed_out"]},
                 "metal_grates": {"name": "Metal Grates", "plural": True, "damages": ["rust", "degraded", "washed_out"]},
                 "metal_panels": {"name": "Metal Panels", "plural": True, "damages": ["rust", "degraded", "washed_out"]},
                 "bricks": {"name": "Bricks", "plural": True, "damages": ["cracked", "degraded", "washed_out"]},
                 "bamboo": {"name": "Bamboo", "plural": False, "damages": ["rotten", "degraded", "moldy"]},
                 "plastic_panels": {"name": "Plastic Panels", "plural": True, "damages": ["cracked", "degraded", "washed_out"]},
                 "linoleum": {"name": "Linoleum", "plural": False, "damages": ["rotten", "moldy", "degraded", "washed_out"]},
                 "steel_beams": {"name": "Steel Beams", "plural": True, "damages": ["rust"]},
                 }

    #These are used by the return_damage_prefixes function, again i do not remember why I put them here of all places.
    damage_prefixes_singular = ["is", "has some", "shows signs of", "shows some"]
    damage_prefixes_plural = ["are", "have some", "show signs of", "show some"]

    damages = {"exposed_rebar": {"name": "exposed rebar", "prefix": 3},
               "rust": {"name": "rusted", "prefix": 0},
               "cracked": {"name": "cracked", "prefix": 0},
               "rotten": {"name": "rotten", "prefix": 0},
               "moldy": {"name": "moldy", "prefix": 0},
               "degraded": {"name": "degraded", "prefix": 0},
               "washed_out": {"name": "washed out", "prefix": 0},
               }

#The same as the ConstructionMaterials class but for natural materials, rather than materials used in buildings.
#A location can have both, but there is a risk of creating very long descriptions. So it should be avoided.
class NaturalMaterials:
    materials = {"sand": {"name": "Sand", "plural": False, "damages": ["cracked", "weeds"]},
                 "gravel": {"name": "Gravel", "plural": False, "damages": ["weeds"]},
                 "mud": {"name": "Mud", "plural": False, "damages": ["cracked", "weeds"]},
                 "soil": {"name": "Soil", "plural": False, "damages": ["cracked", "weeds"]},
                 "rocks": {"name": "Rocks", "plural": True, "damages": ["cracked", "degraded", "moss", "bleached"]},
                 "clay": {"name": "Clay", "plural": False, "damages": ["cracked", "moss"]},
                 "rubble": {"name": "Rubble", "plural": False, "damages": ["cracked", "degraded"]},
                 "debris": {"name": "Debris", "plural": True, "damages": ["cracked", "degraded"]},
                 "trash": {"name": "Trash", "plural": False, "damages": ["rotten", "moldy", "bleached"]},
                 "pine_needles": {"name": "Dried Pine Needles", "plural": True, "damages": ["rotten", "moss"]},
                 "manure": {"name": "Manure", "plural": False, "damages": ["rotten", "moldy"]},

                 }

    damages = {"eroded": {"name": "erosion", "prefix": 2},
               "bleached": {"name": "bleached by the sun", "prefix": 0},
               "cracked": {"name": "cracked", "prefix": 0},
               "rotten": {"name": "rotten", "prefix": 0},
               "moldy": {"name": "moldy", "prefix": 0},
               "degraded": {"name": "degraded", "prefix": 0},
               "washed_out": {"name": "washed out", "prefix": 0},
               "weeds": {"name": "overgrown with weeds", "prefix": 0},
               "moss": {"name": "overgrown with moss", "prefix": 0},

               }

#This class stores a dict with information about fauna. So far they only have a name to be displayed to the player. But I plan to do more with them once food sources are in the game.
#They are always plural and should be used for small critters that just sort of exist in the background. For single larger animals i will probably use some sort of encounter/event system.
class Fauna:
    animals = {
        "crustacean": {"name": "Crustaceans"},
        "mosquitoes": {"name": "Mosquitoes"},
        "fruit_flies": {"name": "Fruit Flies"},
        "seabirds": {"name": "Seabirds"},
        "small_fish": {"name": "Small Fish"},
        "bats": {"name": "Bats"},
        "cave_crustacean": {"name": "Strangely Pale Crustaceans"},
        "amphibians": {"name": "Amphibians"},

    }

#Same as the fauna but with a value for singular/plural. So far just window dressing but will be used for foraging related gameplay at some point.
class Flora:
    plants = {
        "tall_grass": {"name": "Tall Grass", "plural": False},
        "small_bushes": {"name": "Small Bushes", "plural": True},
        "small_trees": {"name": "Small Trees", "plural": True},
        "thorny_bushes": {"name": "Thorny Bushes", "plural": True},
        "wild_flowers": {"name": "Wild Flowers", "plural": True},
        "mold": {"name": "Mold", "plural": False},
        "moss": {"name": "Moss", "plural": False},
        "small_fungus": {"name": "Small Mushrooms", "plural": True},
        "seaweed": {"name": "Seaweed", "plural": False},
        "algae": {"name": "Algae", "plural": True},
        "herbs": {"name": "Herbs", "plural": True},

    }


#Very simple class containing objects scattered around a location, it is always plural and has just a name so far. Same as the above two classes really.
class ScatteredObjects:
    objects = {
        "rocks": {"name": "Rocks"},
        "driftwood": {"name": "Driftwood"},
        "junk": {"name": "A Variety of Junk"},
        "seaweed": {"name": "Washed up Seaweed"},
        "mountain_flowers": {"name": "Mountain Flowers"},
    }



#This class provides all the information needed for something that surrounds a location. Besides the usual name and plural values it has a preposition value, used by the text generator once again.
#I did a fair bit of experimenting, there is a direction value that is empty, I do not remember if it is even used at all. There also are two messages for entering and exiting a location,
#that is surrounded by something. There must be lists because the text generator picks a random one each time. It was an early attempt to get some more variety in to the game.
#Eventually it will probably be replaced with some sort of event, giving the player a choice how to navigate the obstacle. Don't pay to much mind to it for now. ;)
class Surrounded:
    objects = {
        "fence_wood": {"name": "Wooden Fence", "plural": False, "direction": "", "preposition": "a ", "enter_message": ["I manage to climb over the Fence", "I find a Gap in the Fence"], "exit_message": ["I manage to climb over the Fence", "I find a Gap in the Fence"]},
        "fence_wire": {"name": "Wire Mesh Fence", "plural": False, "direction": "", "preposition": "a ", "enter_message": ["I manage to climb over the Fence", "I find a Gap in the Fence"], "exit_message": ["I manage to climb over the Fence", "I find a Gap in the Fence"]},
        "wall_wood": {"name": "Wooden Wall", "plural": False, "direction": "", "preposition": "a ", "enter_message": ["I manage to climb over the Wall", "I find a collapsed bit of Wall"], "exit_message": ["I manage to climb over the Wall", "I find a collapsed bit of Wall"]},
        "wall_brick": {"name": "Brick Wall", "plural": False, "direction": "", "preposition": "a ", "enter_message": ["I manage to climb over the Wall", "I find a collapsed bit of Wall"], "exit_message": ["I manage to climb over the Wall", "I find a collapsed bit of Wall"]},
        "thorny_bushes": {"name": "Thorny Bushes", "plural": True, "direction": "", "preposition": "", "enter_message": ["I force my way though the Thorny Bushes", "I force my way though the Thorny Bushes"],
                          "exit_message": ["I manage to climb over the Wall", "I find a collapsed bit of Wall"]},

    }


#Class containing information regarding where a location is situated, used mostly when entering and exiting, functions somewhat like the Surrounded class above.
class SituatedObjects:
    objects = {
        "on_plateau": {"name": "On a Plateau", "enter_message": ["Make my way on to the Plateau"], "exit_message": ["Find my way of the Plateau"]},
        "under_cliff": {"name": "Beneath a Steep Cliff", "enter_message": ["Climb down the Cliff"], "exit_message": ["Climb back up the Cliff"]},
        "on_cliff": {"name": "On top of a Steep Cliff", "enter_message": ["Climb up the Cliff"], "exit_message": ["Climb back down the Cliff"]},
        "behind_rocks": {"name": "Behind some huge Rocks", "enter_message": ["Climb over some of the huge Rocks"], "exit_message": ["Climb over some of the huge Rocks"]},
        "center_of_island": {"name": "In the Center of the Island", "enter_message": ["Make my way in to the Center of the Island"], "exit_message": ["Make my way out of the Center of the Island"]},

    }



#This class works the same as the above two, but deals with doors and such. All of these can be combined, but the message might end up very long.
class AccessMethods:
    methods = {
        "ladder_up": {"enter_message": ["Climb up the Ladder"], "exit_message": ["Climb down the Ladder"],
                      "name": "Ladder leading up", "plural": False, "preposition": "a "},
        "ascend": {"enter_message": ["Ascend"], "exit_message": ["Descend"],
                   "name": "Steep Ascent", "plural": False, "preposition": "a "},
        "metal_door": {"enter_message": ["Pry open the Metal Door and enter"], "exit_message": ["Pry open the Metal Door and exit"],
                       "name": "Metal Door", "plural": False, "preposition": "a "},
        "metal_hatch": {"enter_message": ["Pry open the Metal hatch and enter"], "exit_message": ["Pry open the Metal hatch and exit"],
                        "name": "Metal Hatch", "plural": False, "preposition": "a "},
        "descend": {"enter_message": ["Descend"], "exit_message": ["Ascend"],
                    "name": "Steep Descend", "plural": False, "preposition": "a "},
        "narrow_tunnel": {"enter_message": ["Crawl though a narrow tunnel"], "exit_message": ["Crawl though a narrow tunnel"],
                          "name": "Narrow Tunnel", "plural": False, "preposition": "a "},
        "climb_up": {"enter_message": ["Climb up"], "exit_message": ["Climb down"],
                     "name": "Bit of Climbing", "plural": False, "preposition": "a "},
        "cramped_stairwell": {"enter_message": ["Climb up the Stairs"], "exit_message": ["Climb down the Stairs"],
                              "name": "Cramped Stairwell", "plural": False, "preposition": "a "},
    }



#Class that contains some information that can be used to provide the player with some hints on what sublocations might be found. This was made before I introduced the
#generic flavor text and it is made somewhat obsolete by it. I am reluctant to get rid of it though as it might be useful, since the flavor text can not contain anything influencing
#actuall gameplay, while this provides the infrastructure for it.
class TopographyObjects:
    objects = {
        "mountain_center": {"name": "Mountainous Area in the Center", "plural": False, "preposition": "a "},
        "forest_plateaus": {"name": "Small Forests on Plateaus", "plural": True, "preposition": ""},
        "sparse_ruins": {"name": "Some Sparse Ruins", "plural": True, "preposition": ""},
        "abandoned_huts": {"name": "Several Huts in various states of disrepair", "plural": True, "preposition": ""},

    }


#Contains the environmental effects of wind, sound and smells. working pretty much the same as anything else in here.
#The sounds are a bit awkward in that they always need a verb to construct a sentence like "the verb of name". I found this to be obnoxious and will probably change it at some point.
#I might also merge these and the light level class and anything to do with environment with the timefunctions file. As it is a bit empty and it might make more sense there.

class EnvironmentalEffects:
    wind = {
        "slight": {"name": "Slight"},
        "moderate": {"name": "Moderate"},
        "strong": {"name": "Strong"},
    }
    sounds = {
        "waves": {"name": "Waves", "verb": "Crashing"},
        "seagulls": {"name": "Seagulls", "verb": "Screeching"},
        "birds": {"name": "Birds", "verb": "Singing"},
        "water_rippling": {"name": "Water", "verb": "Rippling"},
        "bats": {"name": "Bats", "verb": "squeaking"},
        "water_dripping": {"name": "Water", "verb": "Dripping"},
        "water_fall": {"name": "Water", "verb": "Crashing"},

    }
    smells = {
        "salty": {"name": "Salty"},
        "moldy": {"name": "Moldy"},
        "stuffy": {"name": "Stuffy"},
        "disgusting": {"name": "Disgusting"},

    }



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
        "tiny_windows": {"name": "Tiny Windows", "light_level": 1},
        "medium_windows": {"name": "Medium Sized Windows", "light_level": 2},
        "large_windows": {"name": "Large Windows", "light_level": 3},
        "broken_walls": {"name": "Broken Wall Parts", "light_level": 1},
        "roof_hole": {"name": "massive Holes in the Roof", "light_level": 4},
    }