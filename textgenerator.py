
from materialdict import *
from location_tag_dict import *
from object_tag_dict import *


#Function to generate a description for a location
def generate_description(location, occasion, world):
    results = []
    #occasion is used to differentiate between a description for a location the player is currently in and a location the player has discovered. It alters some part of the text and on discovery it does
    #not describe the environment. Not too big a deal.

    if occasion == "description":

        #This generates a message describing the players state of being, like "I am swimming, I am wandering, etc."
        #Only one such message can exist. If more than one of these messages are provided, only the first one is shown to the player.
        being_messages = []
        #Goes over the locations tags and looks for appropriate messages
        for tag in location.tags:
            tag = return_location_tag(tag, location)
            being = tag.get("being")
            if being:
                being_messages.append(being)
        #If a being message has been found, it is displayed to the player, else a default one is shown.
        if being_messages:
            being_messages = "I am {0}.\n".format(being_messages[0])
            results.append(being_messages)

        else:
            being_messages = "I am {0} the {1}.\n".format(location.preposition, location.name)
            results.append(being_messages)

    #On discovery a different message is shown
    elif occasion == "discovery":
        results.append("I have discovered {0}{1}.\n".format(location.article, location.name))


    messages_buffer = []

    #This looks for topography messages in the locations tags
    for tag in location.tags:
        tag = return_location_tag(tag, location)
        message = tag.get("topography_message")
        if message:
            messages_buffer.append(message)

    #If it finds any it sorts them according to their priority and shows them to the player in that order.
    if messages_buffer:
        messages = []
        messages_buffer.sort(key=lambda i: i[0])
        for message in messages_buffer:
            messages.append(message[1])
        messages.append("\n")
        messages = " ".join(messages)
        results.append(messages)

    #If the player is currently at the location, the above is repeated for environmental messages, this is omitted when the location is being discovered.
    if occasion == "description":

        messages_buffer = []
        for tag in location.tags:
            if check_message_condition(tag, world):
                tag = return_location_tag(tag, location)
                message = tag.get("environment_message")
                if message:
                    messages_buffer.append(message)

        if messages_buffer:
            messages = []
            messages_buffer.sort(key=lambda i: i[0])
            for message in messages_buffer:
                messages.append(message[1])
            messages = " ".join(messages)
            results.append(messages)

    results = "".join(results)
    return results

#function to convert the ratio of the players familiarity with a location and its wilderness level in to a text message.
def return_familiarity(location):
    familiarity = location.familiarity/location.wilderness
    if familiarity == 0:
        return "very unfamiliar"
    elif 0 <= familiarity < 0.3:
        return "unfamiliar"
    elif 0.3 <= familiarity < 0.5:
        return " somewhat familiar"
    elif 0.5 <= familiarity <= 0.7:
        return "familiar"
    elif 0.7 <= familiarity < 0.9:
        return "very familiar"
    else:
        return "extremely familiar"

#Turns numbers in to words. I really need to find a good place for these kind of functions.
def return_numbers(number):
    if number <= 10:
        numbers = {
            0: "zero",
            1: "one",
            2: "two",
            3: "three",
            4: "four",
            5: "five",
            6: "six",
            7: "seven",
            8: "eight",
            9: "nine",
            10: "ten",
        }
        return numbers.get(number)
    elif 10 < number < 15:
        return "about a dozen"
    elif 15 < number < 30:
        return "about two dozen"
    else:
        return "a lot of"

#A function to describe a rooms windows
def return_window_lighting(windows):
    results = []
    #If the location has windows it checks how many there are. If it is just one it generates a simple message.
    #Otherwise it creates a more complex string with all the windows first.
    if windows:
        if len(windows) == 1:
            material_results = "{0}".format(Windows.windows[windows[0]]['name'])
            results.append(material_results)
        else:
            material_results = []
            for window in windows:
                index = windows.index(window)
                if index == 0:
                    material_results.append(Windows.windows[window]['name'])
                elif index == len(windows) - 1:
                    material_results.append(" and {0}".format(Windows.windows[window]['name']))
                else:
                    material_results.append(", {0}".format(Windows.windows[window]['name']))
            material_results = "".join(material_results)
            material_results = "{0}".format(material_results)
            results.append(material_results)


    results = "".join(results)
    return results

#The function to generate descriptions for objects. It works pretty much the same as the one for locations.
#Materials and features are getting the same treatment as windows do in the function above. Messages are handled like the messages for locations.
def generate_object_description(game_object):
    results = []

    results.append("{0}. ".format(game_object.name).capitalize())

    messages_buffer = []
    for tag in game_object.tags:
        tag = return_object_tag(tag, game_object)
        message = tag.get("material")
        if message:
            messages_buffer.append(message)
    if messages_buffer:
        messages = []
        for message in messages_buffer:
            index = messages_buffer.index(message)
            if index == 0:
                messages.append(message)
            elif index == len(messages_buffer) - 1:
                messages.append(" and {0}".format(message))
            else:
                messages.append(", {0}".format(message))
        messages = "".join(messages)
        messages = "{1} {2} made out of {0}. ".format(messages, game_object.pronoun, game_object.object_being).capitalize()

        results.append(messages)

    messages_buffer = []
    for tag in game_object.tags:
        tag = return_object_tag(tag, game_object)
        message = tag.get("feature")
        if message:
            messages_buffer.append(message)
    if messages_buffer:
        messages = []
        for message in messages_buffer:
            index = messages_buffer.index(message)
            if index == 0:
                messages.append(message)
            elif index == len(messages_buffer) - 1:
                messages.append(" and {0}".format(message))
            else:
                messages.append(", {0}".format(message))
        messages = "".join(messages)
        messages = "{1} {2} {0}. ".format(messages, game_object.pronoun, game_object.object_feature).capitalize()

        results.append(messages)

    messages_buffer = []
    for tag in game_object.tags:
        tag = return_object_tag(tag, game_object)
        message = tag.get("message")
        if message:
            messages_buffer.append(message)

    if messages_buffer:
        messages = []
        messages_buffer.sort(key=lambda i: i[0])
        for message in messages_buffer:
            messages.append(message[1].capitalize())
        messages = " ".join(messages)
        results.append(messages)

    results = "".join(results)
    return results



