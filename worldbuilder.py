
from worlddict import *
from enum import Enum
from textgenerator import *
from materialdict import *
from timefunctions import *


#The class that stores all data of a given location
class Location:
    def __init__(self, entities, name, preposition, max_sublocations,
                 location_type, location_level, singular, forced, travel_steps, explore_steps, search_steps, time_scale, alias, article):
        self.entities = entities
        self.name = name
        self.preposition = preposition
        self.max_sublocations = max_sublocations
        self.location_type = location_type
        self.location_level = location_level
        self.singular = singular
        self.forced = forced
        self.travel_steps = travel_steps
        self.explore_steps = explore_steps
        self.search_steps = search_steps
        self.time_scale = time_scale
        self.visited = False
        self.sublocations = []
        self.alias = alias
        self.article = article
        #anything beneath here is optional
        self.surrounded = None
        self.access = None
        self.being = None
        self.scattered_objects = None
        self.environmental_effects = None
        self.light_level = None
        self.construction_material = None
        self.natural_material = None
        self.fauna = None
        self.flora = None
        self.temperature_modifier = None
        self.water = None
        self.indoors = None
        self.windows = None
        self.lights = None
        self.size = None
        self.topography = None
        self.preservation = None
        self.situated = None
        self.access = None
        self.flavor_text = None



    #returns descriptions based of the current situation, this is what calls the text generator
    @property
    def description(self):

        return return_description(self)


    @property
    def description_on_discovery(self):
        return return_discovery(self)

    @property
    def description_on_enter(self):
        return return_enter(self)


    @property
    def description_on_exit(self):
        return return_exit(self)



    #This adds a new sublocation to a location. It works pretty much the same as the initialize_world function in the main file, just without creating a new world and the pick_sublocation
    #function from the worlddict file is used instead
    def add_sublocation(self):
        sublocation_choice = pick_sublocation(self)
        sublocation_choice = return_world_dict(sublocation_choice)
        sublocation = Location([], sublocation_choice[0], sublocation_choice[1], sublocation_choice[2], sublocation_choice[3], sublocation_choice[4], sublocation_choice[5],
                               sublocation_choice[6], sublocation_choice[7], sublocation_choice[8], sublocation_choice[9],
                               sublocation_choice[10], sublocation_choice[11], sublocation_choice[12])
        sublocation.set_location_parameters(sublocation_choice[13])
        sublocation.owner = self

        #once a sublocation is initialized it checks its arguments for "owner", if it finds one it sets this argument to be the same as this locations.
        #This allows for easy reusability of locations. for example: there are two buildings one with bricks as its construction material, one with concrete.
        #We can create a room location as a sublocation for both of them and set its construction material to "owner". If it is generated in the brick building it will be made out of brick,
        #if it is generated in the concrete building it will be made out of concrete
        for arg in vars(sublocation):
            if getattr(sublocation, arg) == "owner":
                parameter = vars(self).get(arg)
                setattr(sublocation, arg, parameter)

        #Applies damage to the materials of the sublocation
        sublocation.set_material_damage()

        #Finally the sublocation is appended to this locations sublocation list and is now ready for use
        self.sublocations.append(sublocation)


    #This function simply sets up the optional parameters from the tags provided in the return_world_dict function of the worlddict file
    def set_location_parameters(self, tags):
        self.surrounded = tags.get("surrounded")
        self.access = tags.get("access")
        self.being = tags.get("being")
        self.scattered_objects = tags.get("scattered_objects")
        self.environmental_effects = tags.get("environmental_effects")
        self.construction_material = tags.get("construction_material")
        self.natural_material = tags.get("natural_material")
        self.fauna = tags.get("fauna")
        self.flora = tags.get("flora")
        self.temperature_modifier = tags.get("temperature_modifier")
        self.water = tags.get("water")
        self.indoors = tags.get("indoors")
        self.windows = tags.get("windows")
        self.lights = tags.get("lights")
        self.size = tags.get("size")
        self.preservation = tags.get("preservation")
        self.topography = tags.get("topography")
        self.situated = tags.get("situated")
        self.access = tags.get("access")
        self.flavor_text = tags.get("flavor_text")

    #Function to set the damage to the construction and natural materials. Can easily be expanded.
    def set_material_damage(self):
        if self.construction_material:
            self.calculate_construction_damage()
        if self.natural_material:
            self.calculate_natural_material_damage()



    #Damage calculation function for construction materials
    def calculate_construction_damage(self):

        #Initializes the chances for damage to occur based on the preservation value of the location
        chance_dict = {0: [0, 0], 1: [0, 0], 2: [25, 0], 3: [50, 0], 4: [75, 25], 5: [100, 50]}
        odds = chance_dict.get(self.preservation)

        #If there is no chance of damage to be done, there is no point in doing the damage check.
        if odds:

            #Takes the materials to be damaged, in this case the base_materials
            base_materials = self.construction_material.get("base_material")
            #Initialises a dict for the damages to be stored in
            primary_damage_dict = {}

            #Goes over every material in the locations base_materials and checks RNG to determine if damage should be applied to the material.
            #If RNG decides to damage the material, an appropriate damage is picked from the material_dict and added to the construction_materials of the location
            if base_materials:
                for material in base_materials:
                    chance = random.randint(1, 100)
                    if chance <= odds[0]:
                        primary_damage_dict.update({"{0}".format(material): return_construction_damage(material)})
                self.construction_material.update({"primary_damage": primary_damage_dict})


            #This is done again for all other types of materials a location has.
            secondary_materials = self.construction_material.get("secondary_material")
            secondary_damage_dict = {}
            if secondary_materials:
                for material in secondary_materials:
                    chance = random.randint(1, 100)
                    if chance <= odds[0]:
                        secondary_damage_dict.update({"{0}".format(material): return_construction_damage(material)})
                self.construction_material.update({"secondary_damage": secondary_damage_dict})



            repair_materials = self.construction_material.get("repair_material")
            repair_damage_dict = {}
            if repair_materials:
                for material in repair_materials:
                    chance = random.randint(1, 100)
                    if chance <= odds[1]:
                        repair_damage_dict.update({"{0}".format(material): return_construction_damage(material)})
                self.construction_material.update({"repair_damage": repair_damage_dict})



    #Same as above but for natural materials
    def calculate_natural_material_damage(self):

        chance_dict = {0: [0, 0], 1: [0, 0], 2: [0, 50], 3: [25, 75], 4: [75, 100], 5: [100, 100]}
        odds = chance_dict.get(self.preservation)

        if odds:
            base_materials = self.natural_material.get("base_material")
            primary_damage_dict = {}
            if base_materials:
                for material in base_materials:
                    chance = random.randint(1, 100)
                    if chance <= odds[0]:
                        primary_damage_dict.update({"{0}".format(material): return_natural_material_damage(material)})
                self.natural_material.update({"primary_damage": primary_damage_dict})



            secondary_materials = self.natural_material.get("secondary_material")
            secondary_damage_dict = {}
            if secondary_materials:
                for material in secondary_materials:
                    chance = random.randint(1, 100)
                    if chance <= odds[0]:
                        secondary_damage_dict.update({"{0}".format(material): return_natural_material_damage(material)})
                self.natural_material.update({"secondary_damage": secondary_damage_dict})



            repair_materials = self.natural_material.get("anthropogenic_material")
            repair_damage_dict = {}
            if repair_materials:
                for material in repair_materials:
                    chance = random.randint(1, 100)
                    if chance <= odds[1]:
                        repair_damage_dict.update({"{0}".format(material): return_natural_material_damage(material)})
                self.natural_material.update({"repair_damage": repair_damage_dict})

#The world class, it hold pretty much every bit of data the game works with
class World:
    def __init__(self):
        self.daytime = 720
        self.time_buffer = 0
        self.player_status = None
        self.travel_target = None
        self.exiting = None
        self.exit_first_step = False
        self.step_buffer = 0
        self.time_scale = 0
        self.locations = []
        self.player_location = None
        self.weather = None
        self.current_light_level = 1


    #function to return a message describing the time of day and light level at the location
    def return_time_and_light(self, location):
        results = []
        #First we grab the light level based on the time of day.
        outside_light_level = return_light_daytime(self.daytime)

        results.append("It is {0}.".format(return_daytime(self.daytime)))

        #If the location is not indoors we simply take the previously determined light level and generate a message out of it. Also sets the current_light_level of the location, so this
        #Can be used to determine the chance of finding stuff or getting lost and so on at some later point in development.
        if not location.indoors:
            self.current_light_level = outside_light_level
            results.append("The {0} is {1}.".format(location.name, LightLevel.light.get(self.current_light_level)))

        #If the location is an indoors location we check how much of the outside light can come in from the windows.
        else:
            #First we check if the location has windows.
            if location.windows:
                window_level_list = []
                #We only care about the highest level of windows a location has. Window levels do not stack.
                for window in location.windows:
                    window_level_list.append(Windows.windows[window]['light_level'])
                window_level = max(window_level_list)
                window_level = window_level

                #The window level determines the maximum level of light a indoor location can have. If it is bigger than the light level outside, the light level is set to that level.
                if window_level > outside_light_level:
                    self.current_light_level = outside_light_level
                #If the outside provides more light than the locations window level would allow, the locations light level is set to this instead.
                else:
                    self.current_light_level = window_level


                #This generates a message to display to the player. If the light level is 0 a special message is used instead.
                if self.current_light_level != 0:

                    results.append("The {0} is {1} through some {2}.".format(location.name, LightLevel.light.get(self.current_light_level), return_window_lighting(location.windows)))
                else:
                    results.append("The {0} is {1}.".format(location.name, LightLevel.light.get(self.current_light_level)))

            #If the location is indoors and has now windows and there is any sort of light outside the light level is set to 1,
            #this is supposed to represent a bit of light entering though a door or something. Otherwise the location will be light level 0,
            #this currently can not happen in game but is there just to be sure.
            else:
                if outside_light_level != 0:
                    self.current_light_level = 1
                    results.append("The {0} is {1} by some ambient light.".format(location.name, LightLevel.light.get(self.current_light_level)))

                else:
                    self.current_light_level = 0
                    results.append("The {0} is {1}.".format(location.name, LightLevel.light.get(self.current_light_level)))


        results = " ".join(results)
        return results


    #Advances the time of day. Time is measured in minutes. The time scale determines how much time passes every time this function is called. The exact time is always more or less random.
    def advance_time(self):
        time_to_advance = 0

        if self.time_scale == 1:
            time_to_advance = randint(0, 1)

        elif self.time_scale == 2:
            time_to_advance = randint(1, 5)

        elif self.time_scale == 3:
            time_to_advance = randint(5, 15)

        elif self.time_scale == 4:
            time_to_advance = randint(30, 60)

        #If the day is over, 24 hours are subtracted from the time
        self.daytime += time_to_advance
        if self.daytime > 1440:
            self.daytime -= 1440


    #Is called every "turn" if the player is exploring or moving, the number of steps determines how many "turns" it takes to do these things.
    #It just removes one step from the buffer if there is any and then advances time. Fairly easy.
    def process_step(self):
        if self.step_buffer > 0:
            self.step_buffer -= 1
            self.advance_time()


    #Sets the timescale of the game.
    def set_timescale(self, player_location):
        if self.exiting:
            self.time_scale = self.exiting.time_scale
        elif self.travel_target:
            self.time_scale = self.travel_target.time_scale
        else:
            self.time_scale = player_location.time_scale


#Simple function to slightly randomise the number of steps something takes.
def return_steps(steps):
    steps = randint(steps-1, steps+1)
    if steps == 0:
        steps = 1
    return steps

#Enum for the players states.
class PlayerState(Enum):
    IDLE = 0
    EXPLORING = 1
    TRAVELING = 2



