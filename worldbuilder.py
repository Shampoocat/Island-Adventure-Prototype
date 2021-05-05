import random

from worlddict import *
from enum import Enum
from timefunctions import *
from objects import *
from location_tag_dict import *
#The class that stores all data of a given location
class Location:
    def __init__(self, objects, name, preposition, max_sublocations, location_type, location_level, singular, forced, time_scale, alias, article, tags, wilderness):
        self.objects = []
        self.name = name
        self.preposition = preposition
        self.max_sublocations = max_sublocations
        self.location_type = location_type
        self.location_level = location_level
        self.singular = singular
        self.forced = forced
        self.time_scale = time_scale
        self.visited = False
        self.sublocations = []
        self.alias = alias
        self.article = article
        self.tags = tags
        self.resolve_tags()
        self.familiarity = 0
        self.wilderness = wilderness

        self.indoors = self.check_indoors()
        self.windows = []
        self.check_windows()

    #These were kind of needed, I don't remember why though
    def check_indoors(self):
        if "indoors" in self.tags:
            return True
        else:
            return False

    def check_windows(self):
        for tag in self.tags:
            if tag == "darkness" or tag == "tiny_windows" or tag == "medium_windows" or tag == "large_windows" or tag == "broken_walls" or tag == "roof_hole":
                self.windows.append(tag)

    #Function to add a sublocaion. I would like to use a dict and .get like with the objects, but I cannot be bothered to change it right now.
    def add_sublocation(self):
        #Picks a sublocation and creates a class instance of it.
        sublocation_choice = pick_sublocation(self)
        sublocation_choice = return_world_dict(sublocation_choice)
        sublocation = Location([], sublocation_choice[0], sublocation_choice[1], sublocation_choice[2], sublocation_choice[3], sublocation_choice[4], sublocation_choice[5],
                            sublocation_choice[6], sublocation_choice[7], sublocation_choice[8], sublocation_choice[9],
                            sublocation_choice[10], sublocation_choice[12])
        sublocation.owner = self

        #Runns the add_location_objects function with the locations object templates to generate objects for the location.
        sublocation.add_location_objects(sublocation_choice[11])

        #Checks if there are tags to be used from the new locations owner
        if sublocation.owner:
            sublocation.resolve_inherited_tags(sublocation.owner)

        #Finally the sublocation is appended to this locations sublocation list and is now ready for use
        self.sublocations.append(sublocation)



    #This one was a pain and it is bad. So far damage is the only thing I really need, but if there are more tags I want to make inheritable it needs a rework.
    def resolve_inherited_tags(self, parent):
        if "decay_from_parent" in self.tags:
            if "slightly_decayed" in parent.tags:
                self.add_tag("slightly_decayed")
            if "somewhat_decayed" in parent.tags:
                self.add_tag("somewhat_decayed")
            if "decayed" in parent.tags:
                self.add_tag("decayed")
            if "severely_decayed" in parent.tags:
                self.add_tag("severely_decayed")
            if "extremely_decayed" in parent.tags:
                self.add_tag("extremely_decayed")

    #Removes a tag form the locations tag list
    def remove_tag(self, tag):
        self.tags.remove(tag)

    #adds a tag to the locations tag list and then resolves the tags again
    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)
            self.resolve_tags()


    #function to resolve tags. This allows tags to generate other tags
    def resolve_tags(self):

        #Checks all of the locations tags if they want to generate tags
        for tag in self.tags:
            tag = return_location_tag(tag, self)
            additional_tags = tag.get("generate_tags")
            #If a tag wants to generate a new tag, it checks if the new tag does not already exist and then adds it.
            if additional_tags:
                for additional_tag in additional_tags:
                    if additional_tag not in self.tags:
                        self.tags.append(additional_tag)


    #function to call the add_objects function for every template, so a location can have multible object templates.
    def add_location_objects(self, templates):
        for template in templates:
            add_objects(template, self)

    #function to increase the players familiarity with a location.
    def increase_familiarity(self):
        #Only works if the familiarity is lower than the wilderness.
        if not self.familiarity >= self.wilderness:
            #compares a float between 0 and 1 with the ratio of familiarity to wilderness, this slows down familiarity gain as the location becomes more familiar.
            if (random.random()) > self.familiarity/self.wilderness:
                #diceroll to make high wilderness locations slower to gain familiarity.
                if randint(0, self.wilderness) == 0:
                    self.familiarity += 1


#The world class, it hold pretty much every bit of data the game works with
class World:
    def __init__(self):
        self.daytime = 720
        self.time_buffer = 0
        self.player_status = None
        self.travel_target = None
        self.exiting = None
        self.first_step = False
        self.step_buffer = 0
        self.time_scale = 0
        self.locations = []
        self.player_location = None
        self.weather = None
        self.current_light_level = 1
        self.player_examine_object = None


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
            time_to_advance = randint(1, 2)

        elif self.time_scale == 3:
            time_to_advance = randint(3, 5)

        elif self.time_scale == 4:
            time_to_advance = randint(5, 10)

        #If the day is over, 24 hours are subtracted from the time
        self.daytime += time_to_advance
        if self.daytime > 1440:
            self.daytime -= 1440


    #Is called every "turn" if the player is exploring or moving, the number of steps determines how many "turns" it takes to do these things.
    #It just removes one step from the buffer if there is any and then advances time and calls the function to check if familiarity is gained. Fairly easy.
    def process_step(self):
        if self.step_buffer > 0:
            self.step_buffer -= 1
            self.advance_time()
            self.player_location.increase_familiarity()



    #Sets the timescale of the game.
    def set_timescale(self, player_location):
        if self.exiting:
            self.time_scale = self.exiting.time_scale
        elif self.travel_target:
            self.time_scale = self.travel_target.time_scale
        else:
            self.time_scale = player_location.time_scale





#Simple function to determine how many steps are taken.
def return_steps(location, mod):
    #Baseline is wilderness - familiarity
    steps = location.wilderness - location.familiarity
    #Steps are altered by a modifier, currently used to make exploration cost half as much as actually going somewhere, should have more uses in the future.
    steps = steps//mod
    #Hard floor of three steps for every action.
    if steps < 3:
        steps = 3
    return steps

#Enum for the players states.
class PlayerState(Enum):
    IDLE = 0
    EXPLORING = 1
    GO = 2
    EXAMINE = 3
    EXIT = 4




