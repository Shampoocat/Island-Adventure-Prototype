import random
from random import randint


# Function to pick a new sublocation
def pick_sublocation(location):
    location_pick = None

    # Checks if the parent location has sublocations that need to be generated before the maximum number of sublocations is reached
    # This ensures that a forced sublocation is always generated, there might be a problem if a poorly designed location has more forced sublocations than maximum locations
    if location.forced:

        # This is the check to see if the location is running out of sublocations and needs to get the forced sublocations going
        if len(location.sublocations) - 1 + len(location.forced) == location.max_sublocations:
            # Checks if a forced sublocation has already been generated and removes it from the forced location pool
            for sublocation in location.sublocations:
                duplicate_type = sublocation.location_type
                if duplicate_type in location.forced:
                    location.forced.remove(duplicate_type)
            # Picks a random (in most cases there should be just one or two) sublocation from the forced sublocation list and generates it
            if location.forced:
                location_pick = random.choice(location.forced)
                location.forced.remove(location_pick)

    # If the above function failed to generate a forced sublocaion, it generates a normal sublocation instead
    if not location_pick:
        # Gets a list of possible sublocations from the SublocationsDict class
        possible_locations = SublocationsDict.world_dict[location.location_type]

        # This filters out locations that should not be generated
        for sublocation in location.sublocations:
            duplicate_type = sublocation.location_type
            # If a sublocation is singular (there may be only one of these per location) and one already exists, it is removed from the options pool
            if sublocation.singular:
                if duplicate_type in possible_locations:
                    possible_locations.remove(duplicate_type)
            # This checks if a forced location already exists and removes it from the forced pool, potentially removing the need to check for forced locations again the next time a sublocation is generated
            if location.forced:
                if duplicate_type in location.forced:
                    location.forced.remove(duplicate_type)
        # Once everything is done, a random sublocation is picked from the remaining options. Locations should be set up in a way to make sure there is always one valid choice
        location_pick = random.choice(possible_locations)

    return location_pick


# Class holding a dict that contains all sublocations a location can have
class SublocationsDict:
    world_dict = {

        # regions

        'abandoned_island': ['mountains', 'peninsula', 'beach_sand', 'pine_forest_island'],
        # zones

        'mountains': ['path_mountain', 'creek_mountain', 'cave', 'building_observatory'],
        'peninsula': ['surf', 'dock', 'building_utility', 'boat_wreck'],
        'beach_sand': ['surf', 'dock', 'building_tower', 'plane_wreck'],
        'pine_forest_island': ['small_village', 'building_research', 'cave', 'forest_clearing'],

        # areas

        'path_mountain': ['path_mountain_shelter', 'old_sign', 'path_mountain_bridge', 'path_mountain_shrine'],
        'creek_mountain': ['creek_mountain_waterfall', 'creek_mountain_pool', 'creek_mountain_floodplain', 'branching_brook'],
        'cave': ['cave_chamber', 'cave_pit', 'bat_colony', 'cave_pond'],
        'building_observatory': ['observatory_dome', 'office_research', 'utility_room', 'storage_room'],
        'surf': ['islet', 'breakwater_sunken', 'outcrop', 'tide_pool'],
        'dock': ['wharf', 'boathouse', 'utility_room', 'storage_room'],
        'building_utility': ['antenna_platform', 'emergency_shelter', 'utility_room', 'storage_room'],
        'boat_wreck': ['boat_wreck_bridge', 'boat_wreck_engine', 'boat_wreck_cargo', 'boat_wreck_quarters'],
        'building_tower': ['observation_platform', 'emergency_shelter', 'utility_room', 'storage_room'],
        'plane_wreck': ['plane_wreck_cockpit', 'plane_wreck_cargo', 'plane_wreck_cabin', 'plane_wreck_wings'],
        'small_village': ['hut', 'main_hut', 'well', 'kitchen_garden'],
        'building_research': ['laboratory', 'office_research', 'utility_room', 'storage_room'],
        'forest_clearing': ['fruit_trees', 'dead_tree', 'flower_field', 'clearing_pond'],

    }


#Returns the data of a location to be fed in to the location class. I will need to rewrite this damn thing as a dict, it should be self explanatory then.
def return_world_dict(key):
    world_dict = {

        # regions
        'abandoned_island': [
            "abandoned island", 'on', 3, 'abandoned_island', 0, False, ['mountains'], 4, "island", "an ",
            ["wandering", "coastal_ocean_slight_wind", "mountain_center", "small_forests", "sparse_ruins"], [], 25],
        # zones

        'pine_forest_island': [
            "pine forest", 'in', randint(2, 3), 'pine_forest_island', 1, False, None, 3, "forest", "a ", ["pine_forest"], [], 25],

        'beach_sand': [
            "sandy beach", 'on', randint(2, 3), 'beach_sand', 1, False, None, 3, "beach", "a ",
            ["beach_sand", random.choice(["below_cliff", "behind_dunes"])], [], 20],

        'peninsula': [

            "peninsula", 'on', randint(2, 3), 'peninsula', 1, False, None, 3, "peninsula", "a ",
            ["peninsula", "tall_grass", "small_bushes", "small_trees", random.choice(["below_cliff", "behind_dunes", "on_cliff", "behind_rocks"])], [], 20],

        'mountains': [

            "mountainous area", 'in', randint(2, 3), 'mountains', 1, True, None, 3, "area", "a ", ["medium_alpine"], [], 35],
        # areas

        'small_village': [
            "abandoned village", 'in', randint(3, 4), 'small_village', 2, False, None,  2, "village", "an ",
            ["small_village_huts", "generic_overgrown"], ["village"], 10],

        'building_research': [
            "ruined research station", 'in', randint(2, 3), 'building_research', 2, False, None, 2, "station", "a ",
            ["building_research", "severely_decayed", "moist", "mold", random.choice(["murky_water_film", "none_tag"]), random.choice(["roof_hole", "none_tag", "broken_walls"])], ["generic_hallways"], 15],

        'cave': [

            "cave", 'in', randint(2, 3), 'cave', 2, False, None, 2, "cave", "a ", ["cave"], [], 40],

        'forest_clearing': [

            "forest clearing", 'on', randint(1, 2), 'forest_clearing', 2, False, None,  2, "clearing", "a ",
            ["tall_grass", "small_bushes", "birds"], [], 25],

        'surf': [

            "surf", 'in', randint(1, 2), 'surf', 2, True, None, 2, "surf", "a ",
            ["sea_water_shallow", "coastal_ocean_moderate_wind", "small_fish_school"], [], 25],

        'dock': [
            "abandoned dock", 'on', randint(1, 2), 'dock', 2, True, ['wharf'], 2, "dock", "an ",
            ["dock", random.choice(["decayed", "severely_decayed", "somewhat_decayed"])], ["outdoor_industrial"], 10],

        'building_tower': [

            "old observation tower", 'in', randint(1, 2), 'building_tower', 2, False, ["observation_platform"], 2, "tower", "an ",
            ["building_tower_observation", random.choice(["decayed", "severely_decayed", "somewhat_decayed"])], ["generic_hallways"], 5],

        'plane_wreck': [

            "wrecked plane", 'at', randint(1, 2), 'plane_wreck', 2, True, None, 2, "wreck", "a ",
            ["plane_wreck", "coastal_ocean_moderate_wind", "extremely_decayed"], [], 7],

        'building_utility': [

            "old utility building", 'in', randint(1, 2), 'building_utility', 2, False, None, 2, "building", "an ",
            ["building_utility", random.choice(["decayed", "severely_decayed", "somewhat_decayed"])], ["generic_hallways"], 5],

        'boat_wreck': [

            "wrecked boat", 'at', randint(1, 2), 'boat_wreck', 2, True, None, 2, "wreck", "a ",
            ["boat_wreck", "coastal_ocean_moderate_wind", "extremely_decayed"], [], 10],

        'path_mountain': [

            "mountain path", 'on', randint(2, 3), 'path_mountain', 2, True, None, 2, "path", "a ",
            ["wandering", "moderate_wind", "gravel", "mountain_flowers"], [], 15],

        'creek_mountain': [

            "creek", 'at', randint(2, 3), 'creek_mountain', 2, True, None, 2, "creek", "a ",
            ["wandering", "water_rippling", "rocky_riverbed", "rocks", "small_trees"], [], 20],

        'building_observatory': [
            "ruined observatory", 'in', randint(2, 3), 'building_observatory', 2, True, None, 2, "observatory", "a ",
            ["building_observatory", "severely_decayed", "moist", "mold", random.choice(["roof_hole", "none_tag", "broken_walls"])], ["generic_hallways"], 10],

        # rooms
        'observatory_dome': [

            "observatory dome", 'in', 0, 'observatory_dome', 3, True, None, 1, "dome", "an ",
            ["observatory_dome", "severely_decayed", "moist", random.choice(["mold", "none_tag"]), random.choice(["roof_hole", "none_tag", "broken_walls"])], ["observatory"], 10],

        'office_research': [

            "office", 'in', 0, 'office_research', 3, False, None, 1, "office", "an ",
            ["indoor_room_generic_medium_window", "decay_from_parent", "moist", random.choice(["mold", "none_tag"]), random.choice(["roof_hole", "none_tag", "broken_walls"])], ["office"], 5],

        'utility_room': [

            "utility room", 'in', 0, 'utility_room', 3, False, None, 1, "room", "an ",
            ["indoor_room_generic_no_window", "decay_from_parent", random.choice(["mold", "none_tag"])], ["utility_room"], 5],

        'storage_room': [

            "storage room", 'in', 0, 'storage_room', 3, False, None, 1, "room", "a ",
            ["indoor_room_generic_no_window", "decay_from_parent", random.choice(["mold", "none_tag"])], ["storage_room"], 5],

        'cave_chamber': [

            "cave chamber", 'in', 0, 'cave_chamber', 3, True, None, 1, "chamber", "a ",
            ["cave_chamber"], [], 30],

        'cave_pit': [

            "deep pit", 'at', 0, 'cave_pit', 3, False, None, 1, "pit", "a ",
            ["cave_pit"], [], 30],

        'bat_colony': [

            "bat colony", 'in', 0, 'bat_colony', 3, False, None, 1, "colony", "a ",
            ["bat_colony"], [], 30],

        'cave_pond': [
            "underground pond", 'at', 0, 'cave_pond', 3, False, None, 1, "pond", "an ",
            ["cave_pond"], [], 30],

        'creek_mountain_waterfall': [

            "waterfall", 'at', 0, 'creek_mountain_waterfall', 3, False, None, 1, "waterfall", "a ",
            ["water_rippling", "refreshing", "gravel"], [], 15],

        'creek_mountain_pool': [

            "pool", 'at', 0, 'creek_mountain_pool', 3, False, None, 1, "pool", "a ",
            ["water_rippling", "refreshing", "birds", "small_trees", "mountain_flowers"], [], 20],

        'creek_mountain_floodplain': [

            "floodplain", 'on', 0, 'creek_mountain_floodplain', 3, False, None, 1, "floodplain", "a ",
            ["water_rippling", "gravel"], [], 10],

        'branching_brook': [


            "branching brook", 'at', 0, 'branching_brook', 3, False, None, 1, "brook", "a ",
            ["water_rippling", "rocky_riverbed", "rocks", "small_trees"], [], 15],

        'path_mountain_shelter': [

            "abandoned shelter", 'at', 0, 'path_mountain_shelter', 3, False, None, 1, "shelter", "an ",
            ["extremely_decayed", "wood_structure", "moderate_wind"], [], 10],

        'old_sign': [

            "old sign", 'at', 0, 'old_sign', 3, False, None, 1, "sign", "an ",
            ["extremely_decayed", "wood_structure", "moderate_wind", "sign_board"], [], 10],

        'path_mountain_bridge': [

            "worn out bridge", 'on', 0, 'path_mountain_bridge', 3, False, None, 1, "bride", "a ",
            ["extremely_decayed", "wood_structure", "moderate_wind", "makeshift_bridge"], [], 15],

        'path_mountain_shrine': [

            "shrine", 'at', 0, 'path_mountain_shrine', 3, False, None, 1, "shrine", "a ",
            ["wood_structure", "moderate_wind", "shrine"], ["shrine"], 10],

        'boat_wreck_bridge': [

            "bridge", 'on', 0, 'boat_wreck_bridge', 3, True, None, 1, "bridge", "a ",
            ["wreck", "extremely_decayed", "large_windows", "indoors", "coastal_ocean_no_wind"], ["wreck_bridge"], 10],

        'boat_wreck_cargo': [

            "cargo hold", 'in', 0, 'boat_wreck_cargo', 3, False, None, 1, "cargo hold", "a ",
            ["wreck", "extremely_decayed", "indoors", "coastal_ocean_no_wind"], ["wreck_cargo"], 15],

        'boat_wreck_engine': [

            "engine room", 'in', 0, 'boat_wreck_engine', 3, True, None, 1, "engine room", "an ",
            ["wreck", "extremely_decayed", "indoors", "coastal_ocean_no_wind"], ["wreck_engine"], 15],

        'boat_wreck_quarters': [

            "living quarter", 'in', 0, 'boat_wreck_quarters', 3, True, None, 1, "quarter", "a ",
            ["wreck", "extremely_decayed", "tiny_windows", "indoors", "coastal_ocean_no_wind"], ["wreck_quarters"], 15],

        'antenna_platform': [

            "antenna platform", 'on', 0, 'antenna_platform', 3, True, None, 1, "platform", "an ",
            ["decayed", "metal", "exposed", "ladder_up"], [], 10],

        'emergency_shelter': [

            "emergency shelter", 'in', 0, 'emergency_shelter', 3, True, None, 1, "shelter", "an ",
            ["decay_from_parent", "indoors", "tiny_windows", "concrete", "metal_hatch", "building_generic_inside"], ["storage_room"], 10],

        'wharf': [

            "wharf", 'on', 0, 'wharf', 3, True, None, 1, "wharf", "a ",
            ["concrete", "metal", "coastal_ocean_moderate_wind", "building_industrial_outside", random.choice(["decayed", "severely_decayed", "somewhat_decayed"])], [], 15],

        'boathouse': [

            "boathouse", 'in', 0, 'boathouse', 3, True, None, 1, "boathouse", "a ",
            ["wood", "metal", "coastal_ocean_moderate_wind", "wood_structure", random.choice(["decayed", "severely_decayed", "somewhat_decayed"])], ["boathouse"], 10],

        'islet': [

            "islet", 'on', 0, 'islet', 3, True, None, 1, "islet", "an ",
            ["coastal_ocean_moderate_wind", "generic_overgrown"], [], 20],

        'breakwater_sunken': [

            "sunken breakwater", 'at', 0, 'breakwater_sunken', 3, False, None, 1, "breakwater", "a ",
            ["coastal_ocean_moderate_wind", "concrete", "crustacean", "small_fish_school", "sea_water_shallow", "seaweed_grown"], [], 20],

        'outcrop': [

            "rocky outcrop", 'at', 0, 'outcrop', 3, False, None, 1, "outcrop", "a ",
            ["coastal_ocean_moderate_wind", "rocks", "crustacean", "small_fish_school", "sea_water_shallow", "seaweed_grown"], [], 20],

        'tide_pool': [

            "tide pool", 'at', 0, 'tide_pool', 3, False, None, 1, "tide pool", "a ",
            ["coastal_ocean_moderate_wind", "crustacean", "small_fish_school", "sea_water_shallow", "seaweed_grown"], [], 20],

        'plane_wreck_cockpit': [

            "cockpit", 'in', 0, 'plane_wreck_cockpit', 3, True, None, 1, "cockpit", "a ",
            ["wreck", "extremely_decayed", "large_windows", "indoors", "coastal_ocean_no_wind"], ["wreck_cockpit"], 5],

        'plane_wreck_cargo': [

            "cargo hold", 'in', 0, 'plane_wreck_cargo', 3, True, None, 1, "cargo hold", "a ",
            ["wreck", "extremely_decayed", "indoors", "coastal_ocean_no_wind"], ["wreck_cargo"], 10],

        'plane_wreck_cabin': [

            "cabin", 'in', 0, 'plane_wreck_cabin', 3, True, None, 1, "cabin", "a ",
            ["wreck", "extremely_decayed", "medium_windows", "indoors", "coastal_ocean_no_wind"], ["wreck_cabin"], 10],

        'plane_wreck_wings': [

            "wing", 'on', 0, 'plane_wreck_wings', 3, True, None, 1, "wing", "a ",
            ["wreck", "extremely_decayed", "coastal_ocean_moderate_wind", "climb_up"], ["wreck_wing"], 10],

        'observation_platform': [

            "observation platform", 'on', 0, 'observation_platform', 3, True, None, 1, "platform", "an ",
            ["decayed", "metal", "exposed", "ladder_up"], [], 10],

        'fruit_trees': [

            "patch of fruit trees", 'at', 0, 'fruit_trees', 3, False, None, 1, "patch", "a ",
            ["birds", "tall_grass", "small_bushes", "fruit_flies"], [], 5],

        'dead_tree': [

            "dead tree", 'at', 0, 'dead_tree', 3, False, None, 1, "Tree", "a ",
            ["birds", "tall_grass", "small_bushes"], [], 5],

        'flower_field': [

            "field of flowers", 'in', 0, 'flower_field', 3, False, None, 1, "field", "a ",
            ["birds", "wild_flowers"], [], 5],

        'clearing_pond': [

            "pond", 'at', 0, 'clearing_pond', 3, False, None, 1, "pond", "a ",
            ["birds", "amphibians", "algae"], [], 5],

        'laboratory': [

            "laboratory", 'in', 0, 'laboratory', 3, False, None, 1, "laboratory", "a ",
            ["indoor_room_generic_medium_window", "decay_from_parent", "moist", random.choice(["mold", "none_tag"]), random.choice(["roof_hole", "none_tag", "broken_walls"])], ["laboratory"], 10],

        'hut': [

            "hut", 'in', 0, 'hut', 3, False, None, 1, "hut", "a ",
            ["indoors", "tiny_windows", "wood", "indoors", random.choice(["roof_hole", "none_tag", "broken_walls"]), random.choice(["decayed", "severely_decayed", "somewhat_decayed"])], ['hut'], 5],


        'main_hut': [

            "hut", 'in', 0, 'main_hut', 3, True, None, 1, "hut", "a ",
            ["important_building", "indoors", "tiny_windows", "wood", "indoors", random.choice(["roof_hole", "none_tag", "broken_walls"]),
             random.choice(["decayed", "severely_decayed", "somewhat_decayed"])], ['hut_large'], 5],

        'well': [

            "well", 'at', 0, 'well', 3, False, None, 1, "well", "a ",
            ["water_dripping", "bricks", "wood", random.choice(["decayed", "severely_decayed", "somewhat_decayed"])], [], 5],

        'kitchen_garden': [

            "kitchen garden", 'in', 0, 'kitchen_garden', 3, False, None, 1, "garden", "a ",
            ["cultivated_herbs", "small_bushes", random.choice(["decayed", "severely_decayed", "somewhat_decayed"])], [], 5],
    }
    return world_dict.get(key)
