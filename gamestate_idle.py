
from textgenerator import *



def handle_game_state_idle(world, console, player_enter):
    # Sanity check to make sure there is no exit location stored by accident
    world.exiting = None

    # Prints out the description of the players location as well as the time of day and the light conditions
    console.rule(title="{0}".format(world.player_location.name.title()), style=" white")


    console.print("{0}\n".format(generate_description(world.player_location, "description", world)))
    console.print("{0}\n".format(world.return_time_and_light(world.player_location)))




    # Prints out options to let the player travel to sublocations of their current location
    # There is a special case here for locations of location level 3, as they do not have sublocations. Here the game uses their parent location instead. This allows the player
    # to go from one room to another room in the same building, without first going back to the building
    location_names = []
    if not world.player_location.location_level == 3:
        # If there are sublocations discovered, they are listed and printed out to the player
        if world.player_location.sublocations:
            console.print("I can [cyan]go[/] to:", )

            # The number of the location is added before printing. It needs the +1 since lists start at 0 because why not -.-
            for location in world.player_location.sublocations:
                location_names.append(location.name.title())
                location_names.append("[cyan]({0})[/]".format(str(world.player_location.sublocations.index(location) + 1)))
        # If no sublocations are known, the player is told to go and explore
        else:
            location_names.append("I do not know of any locations I could go to. I should [cyan]explore[/] this location.")

    # Same as above, but using the locations parent location instead
    else:
        if world.player_location.owner.sublocations:
            console.print("I can [cyan]go[/] to:", )

            for location in world.player_location.owner.sublocations:
                location_names.append(location.name.title())
                location_names.append("[cyan]({0})[/]".format(str(world.player_location.owner.sublocations.index(location) + 1)))

        else:
            location_names.append("I do not know of any locations I could go to. I should [cyan]explore[/] this location.")

    # Prints the entire thing to screen
    console.print(' '.join(location_names), )
    console.print("", )

    # Same as above, but with objects in the players location. there is no need to use the parent location for lv3 locations so this is gone.
    #Objects are also only shown on the lower level locations.
    if world.player_location.location_level == 3 or world.player_location.location_level == 2:

        objects_names = []
        if world.player_location.objects:
            console.print("I can [cyan]examine[/] the following objects {0} the {1}.".format(world.player_location.preposition, world.player_location.name))

            for entity in world.player_location.objects:
                name = "{0}".format(entity.name)
                objects_names.append(name.title())
                objects_names.append("[cyan]({0})[/]".format(str(world.player_location.objects.index(entity) + 1)))
        else:
            objects_names.append("I can not find any interesting objects {0} the {1}.".format(world.player_location.preposition, world.player_location.name))

        console.print(' '.join(objects_names))
    else:
        console.print("The {0} is way too big to account for every single object here.\nI could try to [cyan]search[/] the place though and see what I can find.".format(world.player_location.name))

    console.print("")
    return player_enter

