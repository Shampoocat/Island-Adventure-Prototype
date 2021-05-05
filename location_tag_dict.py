

#This stores all the data associated with object tags. This needs to be a function so the format function can work its magic properly.
#It also allows for random to be used in the future if so desired.
#More data will be stored here eventually.
def return_location_tag(tag, location):

    location_tags = {
        "none_tag": {},
        "coastal_ocean_slight_wind": {"generate_tags": ["waves", "gulls", "salty_air", "slight_wind"]},
        "coastal_ocean_moderate_wind": {"generate_tags": ["waves", "gulls", "salty_air", "moderate_wind"]},
        "coastal_ocean_no_wind": {"generate_tags": ["waves", "gulls", "salty_air"]},
        "mountain_center": {"topography_message": [10, "A mountain range dominates its center."]},
        "small_forests": {"topography_message": [10, "There are some small forested areas dotted around the landscape."]},
        "sparse_ruins": {"topography_message": [10, "A handful of sparse ruins can be found in this area."]},
        "wandering": {"being": "wandering around {0} the {1}".format(location.preposition, location.name)},
        "waves": {"environment_message": [10, "I can hear the waves crashing on the shore."]},
        "gulls": {"environment_message": [10, "Flocks of seagulls are screeching in the distance."]},
        "salty_air": {"environment_message": [10, "The air tastes somewhat salty."]},
        "slight_wind": {"environment_message": [10, "There is a sight wind is blowing here."]},
        "moderate_wind": {"environment_message": [10, "There is a moderate wind is blowing here."]},
        "strong_wind": {"environment_message": [10, "There is a strong wind is blowing here."]},
        "pine_forest": {"generate_tags": ["thorny_bushes", "birds", "pine_needles", "on_plateau"]},
        "thorny_bushes": {"topography_message": [20, "Thorny bushes are growing all over the place."]},
        "birds": {"environment_message": [10, "Plenty of birds can be heard singing."]},
        "pine_needles": {"environment_message": [10, "Dry pine needles are covering the ground."]},
        "beach_sand": {"generate_tags": ["waves", "gulls", "salty_air", "moderate_wind", "driftwood", "seaweed_beach", "sand"]},
        "on_plateau": {"topography_message": [10, "It is situated on a small plateau."]},
        "driftwood": {"environment_message": [10, "Random bits of driftwood can be found all over the {0}.".format(location.alias)]},
        "seaweed_beach": {"environment_message": [10, "Plenty of seaweed has been washed ashore."]},
        "below_cliff": {"topography_message": [10, "It is located beneath some steep cliffs."]},
        "behind_dunes": {"topography_message": [10, "It is situated behind some sandy dunes."]},
        "sand": {},
        "peninsula": {"generate_tags": ["waves", "gulls", "salty_air", "moderate_wind"]},
        "on_cliff": {"topography_message": [10, "It is situated on top of some cliffs."]},
        "behind_rocks": {"topography_message": [10, "It is separated off from the surrounding area by some large rocks."]},
        "small_trees": {"topography_message": [20, "A few small trees can be found growing here."]},
        "small_bushes": {"topography_message": [20, "Small bushes are scattered all over the place."]},
        "tall_grass": {"topography_message": [20, "Tall grass covers the ground."]},
        "medium_alpine": {"generate_tags": ["gravel", "rocks", "ascend", "slight_wind", "small_bushes", "hiking"],
                          "topography_message": [5, "The mountains are midsized, forming distinct valleys ridges and peaks but the overall elevation remains moderate."]},
        "rocks": {"topography_message": [20, "Large rocks are strewn about the place."]},
        "gravel": {"environment_message": [10, "It looks like gravel can be found here in large quantities."]},
        "ascend": {},
        "climb_up": {},
        "climb_down": {},
        "ladder_up": {},
        "ladder_down": {},
        "hiking": {"being": "hiking {0} the {1}".format(location.preposition, location.name)},
        "small_village_huts": {"generate_tags": ["plank_path", "birds_nesting"], "topography_message": [5, "The buildings are arranged around a central area."]},
        "generic_overgrown": {"environment_message": [10, "A variety of plant life has taken a hold of the {0} and is growing everywhere.".format(location.alias)]},
        "plank_path": {"topography_message": [10, "There are various pathways, formed by wooden planks implanted in to the ground."]},
        "birds_nesting": {"environment_message": [10, "I can see and hear quite few birds, they must have chosen this place for their nests."]},
        "building_research": {"generate_tags": ["indoors", "medium_windows", "building_industrial_inside_makeshift"], "topography_message": [5, "It appears it was originally constructed out of several portable shelters."]},
        "indoors": {},
        "slightly_decayed": {"environment_message": [5, "The {0} is showing some slight signs of degradation but is overall well preserved.".format(location.alias)]},
        "somewhat_decayed": {"environment_message": [5, "The {0} seems to have taken some damage from the elements, but nothing too severe.".format(location.alias)]},
        "decayed": {"environment_message": [5, "The {0} is showing clear signs of decay.".format(location.alias)]},
        "severely_decayed": {"environment_message": [5, "The {0} is severely degraded, the elements sure have taken their toll.".format(location.alias)]},
        "extremely_decayed": {"environment_message": [5, "The {0} is in an utter state of ruin.".format(location.alias)]},
        "moist": {"environment_message": [11, "The air feels very moist and stuffy."]},
        "mold": {"environment_message": [12, "I can smell something rotten {0} here, probably mold.".format(location.preposition)]},
        "murky_water_film": {"environment_message": [20, "There is a thin film of disgusting murky water covering the ground."]},
        "darkness": {},
        "tiny_windows": {},
        "medium_windows": {},
        "large_windows": {},
        "broken_walls": {},
        "roof_hole": {},
        "cave": {"generate_tags": ["indoors", "darkness", "descend", "small_fungus", "stuffy_air"], "topography_message": [5, "It is narrow and some parts make it difficult for me to advance."]},
        "descend": {},
        "small_fungus": {"environment_message": [10, "I can find patches of strange small fungi growing everywhere."]},
        "stuffy_air": {"environment_message": [20, "The air {0} here is awfully stuffy, making it hard to breathe.".format(location.preposition)]},
        "mosquitoes": {"environment_message": [10, "Myriads of mosquitoes are buzzing around in the air."]},
        "fruit_flies": {"environment_message": [10, "Myriads of fruit flies are buzzing around in the air."]},
        "sea_water_shallow": {"topography_message": [5, "The water here is fairly shallow. It reaches no further than my knees."], "generate_tags": ["low_waves_in_water", "wading"]},
        "low_waves_in_water": {"environment_message": [10, "Low waves are pushing me around a little bit."]},
        "strong_waves_in_water": {"environment_message": [10, "Strong waves are pushing me around a fair bit. It is tricky to remain steady"]},
        "extreme_waves_in_water": {"environment_message": [10, "Extremely strong waves are knocking me around as they please. They are way to strong for me to resist them."]},
        "seaweed_grown": {"environment_message": [10, "Seaweed is growing all over the {0}.".format(location.alias)]},
        "small_fish_school": {"environment_message": [10, "Plenty of tiny fishes are swimming around."]},
        "wading": {"being": "wading through the water of the {0}".format(location.name)},
        "dock": {"generate_tags": ["concrete", "metal", "coastal_ocean_moderate_wind", "building_industrial_outside"], "topography_message": [5, "A concrete structure lining a basin that leads out to the sea."]},
        "concrete": {},
        "metal": {},
        "bricks": {},
        "wreck": {},
        "wood": {},
        "wood_structure": {"generate_tags": ["wood"], "topography_message": [5, "It is just a simple wooden structure."]},
        "makeshift_bridge": {"generate_tags": ["wood"], "topography_message": [5, "A primitive but functional bridge."]},
        "sign_board": {"environment_message": [10, "The sign is too degraded to make any sense of it."]},
        "shrine": {"generate_tags": ["wood"], "environment_message": [5, "I can not tall what deity the shrine is dedicated to."]},
        "building_generic_inside": {},
        "building_generic_outside": {},
        "building_industrial_outside": {},
        "building_industrial_inside": {},
        "building_industrial_inside_makeshift": {},
        "building_observatory": {"generate_tags": ["indoors", "medium_windows", "bricks", "building_generic_inside"],
                                 "topography_message": [5, "A fairly large building, constructed out of bricks. It features a tower like structure with a dome shaped roof."]},
        "building_tower_observation": {"generate_tags": ["indoors", "tiny_windows", "concrete", "metal_door", "building_generic_inside"], "topography_message": [5, "A small concrete tower with an metal platform on top."]},
        "metal_door": {},
        "plane_wreck": {"generate_tags": ["metal", "wreck"], "topography_message": [5, "It must have been a medium sized multi purpose plane."]},
        "building_utility": {"generate_tags": ["indoors", "tiny_windows", "concrete", "metal_hatch", "building_generic_inside"], "topography_message": [5, "A tiny, plain and inconspicuous concrete building."]},
        "metal_hatch": {},
        "boat_wreck": {"generate_tags": ["metal", "wreck"], "topography_message": [5, "It looks like some sort cargo trawler."]},
        "rocky_riverbed": {"generate_tags": ["gravel"], "topography_message": [5, "It flows though a rocky riverbed."]},
        "mountain_flowers": {"environment_message": [10, "Patches of mountain flowers can be found growing everywhere."]},
        "water_rippling": {"environment_message": [10, "I can hear the water rippling."]},
        "water_dripping": {"environment_message": [10, "I can hear the water dripping."]},
        "observatory_dome": {"generate_tags": ["indoors", "medium_windows"], "topography_message": [5, "A large circular room with a dome shaped roof."]},
        "indoor_room_generic_medium_window": {"generate_tags": ["indoors", "medium_windows"]},
        "indoor_room_generic_no_window": {"generate_tags": ["indoors"]},
        "decay_from_parent": {},
        "cave_chamber": {"generate_tags": ["indoors", "darkness", "small_fungus", "stuffy_air"], "topography_message": [5, "A fairly spacious chamber. Barren but more welcoming than the narrow tunnels."]},
        "cave_pit": {"generate_tags": ["indoors", "darkness", "stuffy_air"], "topography_message": [5, "This part of the caves continues in to a pitch black pit."]},
        "bat_colony": {"generate_tags": ["indoors", "darkness", "bats", "stink", "manure"]},
        "cave_pond": {"generate_tags": ["indoors", "darkness", "water_dripping", "cave_crustacean", "small_fungus", "moist"], "topography_message": [10, "A tranquil little pond can be found here."]},
        "bats": {"environment_message": [10, "There are countless bats fluttering around here."]},
        "stink": {"environment_message": [10, "The smell {0} the {1} is unbearable.".format(location.preposition, location.alias)]},
        "manure": {"environment_message": [10, "Manure covers the ground of this place. Yuck!."]},
        "cave_crustacean": {"environment_message": [10, "A bunch of bizarre crustaceans live here. They are completely pale."]},
        "refreshing": {"environment_message": [10, "The air here feels very refreshing."]},
        "exposed": {"generate_tags": ["strong_wind", "good_view"], "environment_message": [5, "The {0} is very exposed to the elements.".format(location.alias)]},
        "good_view": {"environment_message": [10, "The view from here is fantastic."]},
        "crustacean": {"environment_message": [10, "A bunch of crustaceans live here."]},
        "wild_flowers": {"environment_message": [10, "Plenty of beautiful flowers are blooming everywhere."]},
        "amphibians": {"environment_message": [10, "Various amphibians are making a lot of noise."]},
        "algae": {"environment_message": [10, "Algae are growing all over the {0}.".format(location.alias)]},
        "important_building": {"topography_message": [5, "This building is located in a central location, it might be important."]},
        "cultivated_herbs": {"environment_message": [10, "It appears some one grew some herbs here in the past. Some of them might still be useful."]},

    }
    return location_tags.get(tag)




#This function allows for tags to be used conditionally. Currently very rudimentary and probably a bad implementation anyways.
#Also this might be moved to another file or something. IDK.
def check_message_condition(tag, world):

    #Makes sure birds only make noise during the day.
    if tag in ["gulls", "birds"]:
        if 180 <= world.daytime <= 1200:
            return True
        else:
            return False
    else:
        return True





