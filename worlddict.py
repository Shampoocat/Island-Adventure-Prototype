import random
from random import randint

#Function to pick a new sublocation
def pick_sublocation(location):
    location_pick = None

    #Checks if the parent location has sublocations that need to be generated before the maximum number of sublocations is reached
    #This ensures that a forced sublocation is always generated, there might be a problem if a poorly designed location has more forced sublocations than maximum locations
    if location.forced:

        #This is the check to see if the location is running out of sublocations and needs to get the forced sublocations going
        if len(location.sublocations) - 1 + len(location.forced) == location.max_sublocations:
            #Checks if a forced sublocation has already been generated and removes it from the forced location pool
            for sublocation in location.sublocations:
                duplicate_type = sublocation.location_type
                if duplicate_type in location.forced:
                    location.forced.remove(duplicate_type)
            #Picks a random (in most cases there should be just one or two) sublocation from the forced sublocation list and generates it
            if location.forced:
                location_pick = random.choice(location.forced)
                location.forced.remove(location_pick)

    #If the above function failed to generate a forced sublocaion, it generates a normal sublocation instead
    if not location_pick:
        #Gets a list of possible sublocations from the SublocationsDict class
        possible_locations = SublocationsDict.world_dict[location.location_type]

        #This filters out locations that should not be generated
        for sublocation in location.sublocations:
            duplicate_type = sublocation.location_type
            #If a sublocation is singular (there may be only one of these per location) and one already exists, it is removed from the options pool
            if sublocation.singular:
                if duplicate_type in possible_locations:
                    possible_locations.remove(duplicate_type)
            #This checks if a forced location already exists and removes it from the forced pool, potentially removing the need to check for forced locations again the next time a sublocation is generated
            if location.forced:
                if duplicate_type in location.forced:
                    location.forced.remove(duplicate_type)
        #Once everything is done, a random sublocation is picked from the remaining options. Locations should be set up in a way to make sure there is always one valid choice
        location_pick = random.choice(possible_locations)


    return location_pick



#Class holding a dict that contains all sublocations a location can have
class SublocationsDict:
    world_dict = {

        # regions

        'abandoned_island': ['mountains', 'peninsula', 'beach', 'pine_forest_island'],
        # zones

        'mountains': ['path_mountain', 'creek_mountain', 'cave', 'building_observatory'],
        'peninsula': ['foreshore', 'dock', 'building_utility', 'boat_wreck'],
        'beach': ['foreshore', 'dock', 'building_tower', 'plane_wreck'],
        'pine_forest_island': ['small_village', 'building_research', 'cave', 'forest_clearing'],

        # areas

        'path_mountain': ['path_mountain_shelter', 'old_sign', 'path_mountain_bridge', 'path_mountain_shrine'],
        'creek_mountain': ['creek_mountain_waterfall', 'creek_mountain_pool', 'creek_mountain_floodplain', 'branching_brook'],
        'cave': ['cave_chamber', 'cave_pit', 'bat_colony', 'cave_pond'],
        'building_observatory': ['observatory_dome', 'office_research', 'utility_room', 'storage_room'],
        'foreshore': ['islet', 'breakwater_sunken', 'outcrop', 'tide_pool'],
        'dock': ['wharf', 'boathouse', 'utility_room', 'storage_room'],
        'building_utility': ['antenna_platform', 'emergency_shelter', 'utility_room', 'storage_room'],
        'boat_wreck': ['boat_wreck_bridge', 'boat_wreck_engine', 'boat_wreck_cargo', 'boat_wreck_quarters'],
        'building_tower': ['observation_platform', 'emergency_shelter', 'utility_room', 'storage_room'],
        'plane_wreck': ['plane_wreck_cockpit', 'plane_wreck_cargo', 'plane_wreck_cabin', 'plane_wreck_wings'],
        'small_village': ['hut', 'main_hut', 'well', 'kitchen_garden'],
        'building_research': ['laboratory', 'office_research', 'utility_room', 'storage_room'],
        'forest_clearing': ['fruit_trees', 'dead_tree', 'flower_field', 'clearing_pond'],

    }



#Function to generate a dict with all the needed information to generate a location. This needs to be generated every time to ensure random choices works properly.
#There is probably a more efficient way of dealing with this.
#The following information is stored for each location. This is not pretty and might need to be changed in to a dict rather than a list to avoid confusion. The order of these values must not be changed.
# Name: The name of the location displayed to the player
# Preposition: A preposition used by the text generator
# Max sublocations: The maximum number of sublocation a location can have
# Location_type: A unique internal name for the location, not exposed to the player. Should be the same as they key of the dict.
# Location_level: Ranges from 0, regions, to 3, individual rooms. Sublocations should always be a higher number than their parent location. Has very minor impact on the game at this point though.
# Singular: Bool. If true, only one of these can be generated per parent location
# Forced: A list of sublocations that must be generated before the max sublocation number is reached.
# Travel_steps: How many steps it takes to travel to and from a location. Currently useless, but it will be used to fire random events and encounters at some point.
# Explore_steps: Same as above but determining the number of steps it takes to explore an location.
# Search_steps: Same as above but for searching a location. Currently unused.
# Timescale: How much time passes for each step taken, must be between 1 and 4
# Alias: A shortened version of the name. Used by the text generator
# Article: Exists because the english language hates me. Tells the textgenerator to use a/an respectively
# Tags: A dict of tags that are used by the text generator to generate the description. Some of them also impact gameplay. They are entirely optional,
#   but providing none will leave the description very bland. An empty dict must be provided in any case.
#   While I am happy with the principal behind this method, the syntax is a mess, most of the time lists are used, sometimes strings are used, sometimes a mess of a sub-dict is used.
#   I will need to clean these up, make them more consistent and streamline the entire process. Right now it is a bit of a pain to work with.


def return_world_dict(key):
    world_dict = {



        # regions
        'abandoned_island': [

            "Abandoned Island", 'on', 3, 'abandoned_island', 0, False, ['mountains'], randint(10, 20), randint(3, 4), randint(3, 4), 4, "Island", "an ",
            {
             'size': "Small",
             'environmental_effects': {"wind": "moderate", "sounds": ["waves", "seagulls"], "smells": ["salty"]},
             'topography': ["mountain_center", "forest_plateaus", "sparse_ruins"],
             }],
        # zones

        'pine_forest_island': [
            "Pine Forest", 'in', randint(2, 3), 'pine_forest_island', 1, False, None, randint(4, 6), randint(3, 4), randint(3, 4), 3, "Forest", "a ",
            {"situated": ["on_plateau"],
             'environmental_effects': {"sounds": ["birds"]},
             "flora": ["thorny_bushes"],
             'natural_material': {"base_material": ["pine_needles", "soil"]},
             }],

        'beach': [
            "Beach", 'on', randint(2, 3), 'beach', 1, False, None, randint(6, 8), randint(3, 4), randint(3, 4), 3, "Beach", "a ",
            {'environmental_effects': {"wind": "moderate", "sounds": ["waves", "seagulls"], "smells": ["salty"]},
             "situated": random.sample(["under_cliff"], k=randint(0, 1)),
             "scattered_objects": ["driftwood", "seaweed"],
             "fauna": ["seabirds"]
            }],

        'peninsula': [


            "Peninsula", 'on', randint(2, 3), 'peninsula', 1, False, None, randint(4, 6), randint(3, 4), randint(3, 4), 3, "Peninsula", "a ", {
                "situated": random.sample(["under_cliff", "on_cliff", "behind_rocks"], k=1),
                "scattered_objects": random.sample(["rocks"], k=randint(0, 1)),
                "flora": random.sample(["tall_grass", "small_bushes", "small_trees"], k=randint(1, 2)),
                "fauna": random.sample(["seabirds"], k=randint(0, 1)),
                'environmental_effects': {"wind": "moderate", "sounds": ["waves", "seagulls"], "smells": ["salty"]},

                 }],

        'mountains': [


            "Mountainous Area", 'in', randint(2, 3), 'mountains', 1, True, None, randint(6, 8), randint(3, 4), randint(3, 4), 3, "Area", "a ", {
                'being': 'wandering around',
                'environmental_effects': {"wind": "strong"},
                "flora": ["wild_flowers"] + random.sample(["tall_grass", "small_bushes", "small_trees"], k=randint(1, 3)),
                'natural_material': {"base_material": ["rocks", "gravel"]},
                "preservation": 3,
                "situated": ["center_of_island"],
                "access": ["ascend"],

            }],
        # areas

        'small_village': [
            "Abandoned Village", 'in', randint(3, 4), 'small_village', 2, False, None, randint(2, 3), randint(1, 3), randint(1, 3), 2, "Village", "an ", {
                'size': "Small",
                'being': 'standing',
                'topography': ["mountain_center", "forest_plateaus", "sparse_ruins"],
                "surrounded": random.sample(["fence_wood", "wall_wood"], k=randint(0, 1)),
                "flora": random.sample(["tall_grass", "small_bushes"], k=randint(1, 2)),

            }],

        'building_research': [
            "Ruined Research Station", 'in', randint(2, 3), 'building_research', 2, False, None, randint(2, 3), randint(1, 3), randint(1, 3), 2, "Station", "a ", {
                "preservation": 5,
                'construction_material': {"base_material": ["metal_panels", "plastic_panels"], "secondary_material": ["metal_grates", "linoleum"], "repair_material": random.sample(["wooden_panels", "wooden_bars"], k=randint(0, 2))},
                'water': [0, "murky"],
                'environmental_effects': {"smells": ["moldy"]},
                "flora": ["mold"],
                "indoors": True,
                'windows':  ["medium_windows"] + random.sample(["roof_hole", "broken_walls"], k=randint(0, 2)),

            }],

        'cave': [

            "Cave", 'in', randint(2, 3), 'cave', 2, False, None, randint(2, 3), randint(1, 3), randint(1, 3), 2, "Cave", "a ", {
                "indoors": True,
                'windows': ["darkness"],
                'size': "Small",
                'environmental_effects': {"smells": ["stuffy"]},
                "scattered_objects": ["rocks"],
                "flora": ["small_fungus"],
                "access": ["descend"],

            }],

        'forest_clearing': [


            "Forest Clearing", 'on', randint(1, 2), 'forest_clearing', 2, False, None, randint(2, 3), randint(1, 3), randint(1, 3), 2, "Clearing", "a ", {
                "flora": ["tall_grass"] + random.sample(["small_bushes", "small_trees", "wild_flowers"], k=randint(1, 3)),
                "fauna": ["mosquitoes"],
                'environmental_effects': {"wind": "slight"},
                "surrounded": random.sample(["thorny_bushes"], k=randint(0, 1)),

            }],

        'foreshore': [


            "Foreshore Area", 'on', randint(1, 2), 'foreshore', 2, True, None, randint(2, 3), randint(1, 3), randint(1, 3), 2, "Foreshore", "a ", {
                'environmental_effects': {"wind": "moderate", "sounds": ["waves", "seagulls"], "smells": ["salty"]},
                "fauna": ["small_fish"],
                "flora": ["seaweed"],
                'water': [randint(1, 2), "azure"],
                "flavor_text": "I can easily go in to the water here.",

            }],

        'dock': [
            "Abandoned Dock", 'on', randint(1, 2), 'dock', 2, True, ['wharf'], randint(2, 3), randint(1, 3), randint(1, 3), 2, "Dock", "an ", {
                'environmental_effects': {"wind": "moderate", "sounds": ["waves"], "smells": ["salty"]},
                'construction_material': {"base_material": ["concrete"], "secondary_material": ["steel_beams"]},
                "preservation": 5,
            }],

        'building_tower': [

            "Old Observation Tower", 'in', randint(1, 2), 'building_tower', 2, False, ["observation_platform"], randint(2, 3), randint(1, 3), randint(1, 3), 2, "Tower", "an ", {
                'construction_material': {"base_material": ["concrete"], "secondary_material": ["metal"]},
                "indoors": True,
                'windows': ["tiny_windows"],
                "access": ["metal_door"],
                "preservation": 5,
                "scattered_objects": ["junk"],

            }],

        'plane_wreck': [

            "Wrecked Plane", 'at', randint(1, 2), 'plane_wreck', 2, True, None, randint(2, 3), randint(1, 3), randint(1, 3), 2, "Wreck", "a ", {
                'environmental_effects': {"wind": "moderate", "sounds": ["waves"], "smells": ["salty"]},
                'construction_material': {"base_material": ["metal"]},
                "preservation": 5,
                "flavor_text": "It must have been a medium sized multi purpose plane.",

            }],

        'building_utility': [


            "Old Utility Building", 'in', randint(1, 2), 'building_utility', 2, False, None, randint(2, 3), randint(1, 3), randint(1, 3), 2, "Building", "an ", {
                'construction_material': {"base_material": ["concrete"], "secondary_material": ["metal"]},
                "indoors": True,
                'windows': ["tiny_windows"],
                "access": ["metal_hatch"],
                "preservation": 5,
                "scattered_objects": ["junk"],
            }],

        'boat_wreck': [


            "Wrecked Boat", 'at', randint(1, 2), 'boat_wreck', 2, True, None, randint(2, 3), randint(1, 3), randint(1, 3), 2, "Wreck", "a ", {
                'environmental_effects': {"wind": "moderate", "sounds": ["waves"], "smells": ["salty"]},
                'construction_material': {"base_material": ["metal"]},
                "preservation": 5,
                "flavor_text": "It looks like some sort cargo trawler.",
            }],

        'path_mountain': [

            "Mountain Path", 'on', randint(2, 3), 'path_mountain', 2, True, None, randint(2, 3), randint(1, 3), randint(1, 3), 2, "path", "a ", {
                'being': 'wandering',
                'environmental_effects': {"wind": "strong"},
                'natural_material': {"base_material": ["gravel"], "secondary_material": ["rocks"]},
                "preservation": 3,
                "scattered_objects": ["mountain_flowers"],
            }],

        'creek_mountain': [

            "Creek", 'at', randint(2, 3), 'creek_mountain', 2, True, None, randint(2, 3), randint(1, 3), randint(1, 3), 2, "Creek", "a ", {
                'size': "Small",
                "scattered_objects": ["mountain_flowers"],
                'environmental_effects': {"sounds": ["water_rippling"]},
                'natural_material': {"base_material": ["gravel"]},
                "flavor_text": "It flows though a rocky riverbed.",

            }],

        'building_observatory': [
            "Ruined Observatory", 'in', randint(2, 3), 'building_observatory', 2, True, None, randint(2, 3), randint(1, 3), randint(1, 3), 2, "Observatory", "a ", {
                "preservation": 5,
                'construction_material': {"base_material": ["concrete", "bricks"], "secondary_material": ["linoleum"]},
                'environmental_effects': {"smells": ["moldy"]},
                "flora": ["mold"],
                "indoors": True,
                'windows': ["medium_windows"],
            }],

        # rooms
        'observatory_dome': [


            "Observatory Dome", 'in', 0, 'observatory_dome', 3, True, None, 1, 1, 1, 1, "Dome", "an ", {
                'construction_material': "owner",
                "preservation": "owner",
                'environmental_effects': "owner",
                "flora": "owner",
                "indoors": True,
                'windows': ["roof_hole"],
                'water': "owner",

            }],

        'office_research': [

            "Office", 'in', 0, 'office_research', 3, False, None, 1, 1, 1, 1, "Office", "an ", {
                'construction_material': "owner",
                "preservation": "owner",
                'environmental_effects': "owner",
                "flora": "owner",
                "indoors": True,
                'windows': ["medium_windows"],
                'water': "owner",

            }],

        'utility_room': [


            "Utility Room", 'in', 0, 'utility_room', 3, False, None, 1, 1, 1, 1, "Room", "an ", {
                'construction_material': "owner",
                "preservation": "owner",
                'environmental_effects': "owner",
                "flora": "owner",
                "indoors": True,
                'water': "owner",

            }],

        'storage_room': [

            "Storage Room", 'in', 0, 'storage_room', 3, False, None, 1, 1, 1, 1, "Room", "a ", {
                'construction_material': "owner",
                "preservation": "owner",
                'environmental_effects': "owner",
                "flora": "owner",
                "indoors": True,
                'water': "owner",

            }],



        'cave_chamber': [


            "Cave Chamber", 'in', 0, 'cave_chamber', 3, True, None, 1, 1, 1, 1, "Chamber", "a ", {
                "indoors": True,
                'windows': ["darkness"],
                'environmental_effects': {"smells": ["stuffy"]},
                "scattered_objects": ["rocks"],
                "flora": ["small_fungus"],
                'natural_material': {"base_material": ["clay"]},
                "access": random.sample(["narrow_tunnel"], k=randint(0, 1)),

            }],

        'cave_pit': [

            "Deep Pit", 'at', 0, 'cave_pit', 3, False, None, 1, 1, 1, 1, "Pit", "a ", {
                "indoors": True,
                'windows': ["darkness"],
                'environmental_effects': {"wind": "slight"},
                "flavor_text": "It is impossible to tell how deep it truly is.",
                "access": random.sample(["narrow_tunnel"], k=randint(0, 1)),

            }],

        'bat_colony': [


            "Bat Colony", 'in', 0, 'bat_colony', 3, False, None, 1, 1, 1, 1, "Colony", "a ", {
                "indoors": True,
                'windows': ["darkness"],
                'environmental_effects': {"smells": ["disgusting"], "sounds": ["bats"]},
                'natural_material': {"base_material": ["manure"]},
                'fauna': ["bats"],
            }],

        'cave_pond': [
            "Underground Pond", 'at', 0, 'cave_pond', 3, False, None, 1, 1, 1, 1, "pond", "an ", {
                "indoors": True,
                'windows': ["darkness"],
                'environmental_effects': {"sounds": ["water_dripping"]},
                'natural_material': {"base_material": ["clay"]},
                'fauna': ["cave_crustacean"],
                "flora": ["small_fungus"],
                "access": random.sample(["narrow_tunnel"], k=randint(0, 1)),

            }],

        'creek_mountain_waterfall': [


            "Waterfall", 'at', 0, 'creek_mountain_waterfall', 3, False, None, 1, 1, 1, 1, "Waterfall", "a ", {
                'size': "Small",
                'environmental_effects': {"sounds": ["water_fall"]},
                'natural_material': {"base_material": ["gravel"]},
            }],

        'creek_mountain_pool': [


            "Pool", 'at', 0, 'creek_mountain_pool', 3, False, None, 1, 1, 1, 1, "Pool", "a ", {
                "scattered_objects": ["mountain_flowers"],
                'environmental_effects': {"sounds": ["water_rippling"]},
                'natural_material': {"base_material": ["gravel"], "secondary_material": ["soil"]},
                'fauna': ["small_fish"],

            }],

        'creek_mountain_floodplain': [


            "Floodplain", 'on', 0, 'creek_mountain_floodplain', 3, False, None, 1, 1, 1, 1, "Floodplain", "a ", {
                'environmental_effects': {"sounds": ["water_rippling"]},
                'natural_material': {"base_material": ["gravel"]},
            }],

        'branching_brook': [

            #
            "Branching Brook", 'at', 0, 'branching_brook', 3, False, None, 1, 1, 1, 1, "Brook", "a ", {
                'environmental_effects': {"sounds": ["water_rippling"]},
                'natural_material': {"base_material": ["gravel"]},

            }],

        'path_mountain_shelter': [

            "Abandoned Shelter", 'at', 0, 'path_mountain_shelter', 3, False, None, 1, 1, 1, 1, "Shelter", "an ", {
                'environmental_effects': {"wind": "strong"},
                'construction_material': {"base_material": ["wood"]},
                "preservation": 5,
            }],

        'old_sign': [

            "Old Sign", 'at', 0, 'old_sign', 3, False, None, 1, 1, 1, 1, "Sign", "an ", {
                'environmental_effects': {"wind": "strong"},
                'construction_material': {"base_material": ["wood"], "secondary_material": ["metal"]},
                "preservation": 5,
                "flavor_text": "I cannot tell what information it once held.",

            }],

        'path_mountain_bridge': [

            "Worn out Bridge", 'on', 0, 'path_mountain_bridge', 3, False, None, 1, 1, 1, 1, "Bride", "a ", {
                'environmental_effects': {"wind": "strong", "sounds": ["water_rippling"]},
                'construction_material': {"base_material": ["concrete"], "secondary_material": ["metal"], "repair_material": ["wooden_panels", "bamboo"]},
                "preservation": 5,
                "flavor_text": "It crosses a small but deep brook.",

            }],

        'path_mountain_shrine': [


            "Shrine", 'at', 0, 'path_mountain_shrine', 3, False, None, 1, 1, 1, 1, "Shrine", "a ", {
                'environmental_effects': {"wind": "strong"},
                'construction_material': {"base_material": ["wood"]},
                "flavor_text": "I do not know what deity it is dedicated to.",

            }],

        'boat_wreck_bridge': [


            "Bridge", 'on', 0, 'boat_wreck_bridge', 3, True, None, 1, 1, 1, 1, "Bridge", "a ", {
                'environmental_effects': {"wind": "moderate", "sounds": ["waves"], "smells": ["salty"]},
                'construction_material': {"base_material": ["metal"]},
                "preservation": 5,
                "indoors": True,
                'windows': ["large_windows"],
            }],

        'boat_wreck_cargo': [


            "Cargo Hold", 'in', 0, 'boat_wreck_cargo', 3, False, None, 1, 1, 1, 1, "Cargo Hold", "a ", {
                'construction_material': {"base_material": ["metal"]},
                "preservation": 5,
                "indoors": True,
            }],

        'boat_wreck_engine': [

            "Engine Room", 'in', 0, 'boat_wreck_engine', 3, True, None, 1, 1, 1, 1, "Engine Room", "an ", {
                'construction_material': {"base_material": ["metal"]},
                "preservation": 5,
                "indoors": True,
            }],

        'boat_wreck_quarters': [



            "Living Quarter", 'in', 0, 'boat_wreck_quarters', 3, True, None, 1, 1, 1, 1, "Quarter", "a ", {
                'environmental_effects': {"wind": "moderate", "sounds": ["waves"], "smells": ["salty"]},
                'construction_material': {"base_material": ["metal"]},
                "preservation": 5,
                "indoors": True,
                'windows': ["tiny_windows"],

            }],

        'antenna_platform': [

            "Antenna Platform", 'on', 0, 'antenna_platform', 3, True, None, 1, 1, 1, 1, "Platform", "an ", {
                'environmental_effects': {"wind": "moderate", "sounds": ["waves"], "smells": ["salty"]},
                'construction_material': {"base_material": ["metal"]},
                "preservation": 3,
                "access": ["ladder_up"],

            }],

        'emergency_shelter': [


            "Emergency Shelter", 'in', 0, 'emergency_shelter', 3, True, None, 1, 1, 1, 1, "Shelter", "an ", {
                'construction_material': "owner",
                "preservation": "owner",
                'environmental_effects': "owner",
                "flora": "owner",
                "indoors": True,
                "access": ["metal_hatch"],
                'water': "owner",

            }],

        'wharf': [

            "Wharf", 'on', 0, 'wharf', 3, True, None, 1, 1, 1, 1, "Wharf", "a ", {
                'environmental_effects': {"wind": "moderate", "sounds": ["waves"], "smells": ["salty"]},
                'construction_material': {"base_material": ["concrete"], "secondary_material": ["steel_beams"]},
                "preservation": 5,
                "scattered_objects": ["junk"],

            }],

        'boathouse': [


            "Boathouse", 'in', 0, 'boathouse', 3, True, None, 1, 1, 1, 1, "boathouse", "a ", {
                'environmental_effects': {"wind": "moderate", "sounds": ["waves"], "smells": ["salty"]},
                'construction_material': {"base_material": ["wood"]},
                "preservation": 5,
                "indoors": True,
                'windows': ["roof_hole"],
            }],

        'islet': [


            "Islet", 'on', 0, 'islet', 3, True, None, 1, 1, 1, 1, "Islet", "an ", {
                'environmental_effects': {"wind": "moderate", "sounds": ["waves"], "smells": ["salty"]},
                'natural_material': {"base_material": random.sample(["rocks", "sand", "gravel"], k=randint(1, 3))},

            }],

        'breakwater_sunken': [


            "Sunken Breakwater", 'at', 0, 'breakwater_sunken', 3, False, None, 1, 1, 1, 1, "Breakwater", "a ", {
                'environmental_effects': {"wind": "moderate", "sounds": ["waves"], "smells": ["salty"]},
                'construction_material': {"base_material": ["concrete"]},
                "fauna": ["small_fish", "crustacean"],
                "flora": ["seaweed"],
                "preservation": 3,
                'water': [randint(1, 2), "azure"],
            }],

        'outcrop': [

            "Rocky Outcrop", 'at', 0, 'outcrop', 3, False, None, 1, 1, 1, 1, "Outcrop", "a ", {
                'environmental_effects': {"wind": "moderate", "sounds": ["waves"], "smells": ["salty"]},
                'natural_material': {"base_material": ["rocks"]},
                "fauna": ["small_fish", "crustacean"],
                "flora": ["seaweed"],
                'water': [randint(1, 2), "azure"],
            }],

        'tide_pool': [


            "Tide Pool", 'at', 0, 'tide_pool', 3, False, None, 1, 1, 1, 1, "Tide Pool", "a ", {
                'environmental_effects': {"wind": "moderate", "sounds": ["waves"], "smells": ["salty"]},
                "fauna": ["small_fish", "crustacean"],
                'water': [randint(2, 3), "azure"],
            }],

        'plane_wreck_cockpit': [


            "Cockpit", 'in', 0, 'plane_wreck_cockpit', 3, True, None, 1, 1, 1, 1, "Cockpit", "a ", {
                'environmental_effects': {"sounds": ["waves"], "smells": ["salty"]},
                'construction_material': {"base_material": ["metal"]},
                "preservation": 5,
                "indoors": True,
                'windows': ["large_windows"],
            }],

        'plane_wreck_cargo': [


            "Cargo Hold", 'in', 0, 'plane_wreck_cargo', 3, True, None, 1, 1, 1, 1, "Cargo Hold", "a ", {
                'environmental_effects': {"sounds": ["waves"], "smells": ["salty"]},
                'construction_material': {"base_material": ["metal"]},
                "preservation": 5,
                "indoors": True,
            }],

        'plane_wreck_cabin': [


            "Cabin", 'in', 0, 'plane_wreck_cabin', 3, True, None, 1, 1, 1, 1, "Cabin", "a ", {
                'environmental_effects': {"sounds": ["waves"], "smells": ["salty"]},
                'construction_material': {"base_material": ["metal"]},
                "preservation": 5,
                "indoors": True,
                'windows': ["medium_windows"],
            }],

        'plane_wreck_wings': [

            
            "Wing", 'on', 0, 'plane_wreck_wings', 3, True, None, 1, 1, 1, 1, "Wing", "a ", {
                'environmental_effects': {"wind": "moderate", "sounds": ["waves"], "smells": ["salty"]},
                'construction_material': {"base_material": ["metal"]},
                "preservation": 5,
                "access": ["climb_up"],

            }],

        'observation_platform': [


            "Observation Platform", 'on', 0, 'observation_platform', 3, True, None, 1, 1, 1, 1, "Platform", "an ", {
                'environmental_effects': {"wind": "moderate", "sounds": ["waves"], "smells": ["salty"]},
                'construction_material': {"base_material": ["concrete"], "secondary_material": ["metal"]},
                "preservation": 3,
                "access": ["cramped_stairwell"],

            }],

        'fruit_trees': [


            "Patch of Fruit Trees", 'at', 0, 'fruit_trees', 3, False, None, 1, 1, 1, 1, "Patch", "a ", {
                "fauna": ["fruit_flies"],
                "flora": ["tall_grass", "small_bushes"],

            }],

        'dead_tree': [


            "Dead Tree", 'at', 0, 'dead_tree', 3, False, None, 1, 1, 1, 1, "Tree", "a ", {
                "flora": ["tall_grass", "small_bushes", "small_fungus"],

            }],

        'flower_field': [


            "Field of Flowers", 'in', 0, 'flower_field', 3, False, None, 1, 1, 1, 1, "Field", "a ", {
                "flora": ["wild_flowers"],

            }],

        'clearing_pond': [


            "Pond", 'at', 0, 'clearing_pond', 3, False, None, 1, 1, 1, 1, "Pond", "a ", {
                'natural_material': {"base_material": ["mud"], "secondary_material": ["soil"]},
                'fauna': ["amphibians"],
                "flora": ["algae"],

            }],

        'laboratory': [


            "Laboratory", 'in', 0, 'laboratory', 3, False, None, 1, 1, 1, 1, "Laboratory", "a ", {
                'construction_material': "owner",
                "preservation": "owner",
                'environmental_effects': "owner",
                "flora": "owner",
                "indoors": True,
                'windows': ["medium_windows"],
                'water': "owner",

            }],

        'hut': [


            "Hut", 'in', 0, 'hut', 3, False, None, 1, 1, 1, 1, "Hut", "a ", {
                'construction_material': {"base_material": ["wood"], "secondary_material": ["bamboo"]},
                "preservation": randint(3, 5),
                "indoors": True,
                'windows': ["tiny_windows"],
                'size': "Small",

            }],
        'main_hut': [

            "Hut", 'in', 0, 'main_hut', 3, True, None, 1, 1, 1, 1, "Hut", "a ", {
                'construction_material': {"base_material": ["wood"], "secondary_material": ["bamboo"]},
                "preservation": randint(3, 5),
                "indoors": True,
                'windows': ["tiny_windows"],
                'size': "Large",
            }],

        'well': [


            "Well", 'at', 0, 'well', 3, False, None, 1, 1, 1, 1, "Well", "a ", {
                'construction_material': {"base_material": ["bricks"], "secondary_material": ["wood"]},
                "preservation": randint(3, 5),
                'environmental_effects': {"sounds": ["water_dripping"]},

            }],

        'kitchen_garden': [


            "Kitchen Garden", 'in', 0, 'kitchen_garden', 3, False, None, 1, 1, 1, 1, "Garden", "a ", {
                'construction_material': {"base_material": ["wood"], "secondary_material": ["bricks"]},
                "preservation": randint(3, 5),
                "flora": ["small_bushes", "herbs"],
                "surrounded": ["fence_wood"],

            }],
    }
    return world_dict.get(key)

