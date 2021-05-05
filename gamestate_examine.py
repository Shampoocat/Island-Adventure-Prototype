
from input import return_input_scope


#Function to handle examining an object
def handle_game_state_examine(world, console, player_enter):
    console.rule(title="{0}".format(world.player_examine_object.name.title()), style=" white")
    #Prints the objects description and tells the player about the default "stop" command.
    console.print(world.player_examine_object.description)
    console.print("")
    console.print("I can [cyan]stop[/] examining the {0} at any time.\n".format(world.player_examine_object.simple_name.title()))

    #prints a list of all possible interactions with the object, currently this is always empty, as they are not in the game yet.
    #The stop command is removed, as the player has already been informed about it.
    possible_options = return_input_scope(world)
    possible_options.remove("stop")
    if possible_options:
        possible_options = ' ,'.join(possible_options)
        possible_options = "I could also [cyan]{0}[/] the {1}.".format(possible_options, world.player_examine_object.name.title())
        console.print(possible_options)
    #If there are no interactions possible, the player is told about it.
    else:
        console.print("I don't see any way to further interact with the {0}.".format(world.player_examine_object.name.title()))

    return player_enter
