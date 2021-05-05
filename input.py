from worldbuilder import PlayerState, return_steps


#function to process player input
def input_handler(player_input, world):

    #If there is no input(the player just presses enter) some is generated to prevent things from going haywire
    if not player_input:
        player_input = "..."

    #A list of possible commands is retrieved from the input_scope function
    commands = return_input_scope(world)
    #If the commands list is empty(there currently is nothing for the player to do) the player input just gets sent back to the main game loop
    if not commands:
        return {"player_choice": "{0}".format(player_input)}

    #If the first word of the players command is not currently useable, either because of the circomstances or because of a typo, an error is sent back to the main game loop
    elif player_input.split()[0] not in commands:
        options = ", "
        options = options.join(commands)
        return {"player_choice": "{0}".format(player_input), "error": "Possible options are: [cyan]{0}[/].\n".format(options)}
    #If all above tests have been passed, the first word of the players command is processed. If the command is always just a single word (like "quit") the
    #command is sent to the main loop, if it requires additional conditions to be satisfied(like a valid number of a location after "go") a function is called to check these conditions.
    #This opportunity is also used to catch synonymous commands like "go" and "enter" both calling the same function
    else:
        if player_input.split()[0] == "quit":
            return {"player_choice": "quit"}
        elif player_input.split()[0] == "travel":
            return {"player_choice": "travel"}
        elif player_input.split()[0] == "search":
            return {"player_choice": "search"}
        elif player_input.split()[0] == "explore":
            return check_for_valid_explore_destination(world)
        elif player_input.split()[0] == "exit" or player_input.split()[0] == "leave":
            return check_for_valid_exit_destination(world)
        elif player_input.split()[0] == "enter" or player_input.split()[0] == "go":
            return check_for_valid_go_destination(player_input, world)
        elif player_input.split()[0] == "examine":
            return check_for_valid_examine_object(player_input, world)
        elif player_input.split()[0] == "stop":
            return {"player_choice": "stop"}




#This function returns all possible commands that are valid in any given situation.
def return_input_scope(world):
    scope = []
    if world.player_status == PlayerState.IDLE:
        if world.player_location.location_level == 3 or world.player_location.location_level == 2:
            scope = ["go", "enter", "leave", "exit", "explore", "examine", "travel", "quit"]
        else:
            scope = ["go", "enter", "leave", "exit", "explore", "travel", "quit", "search"]

    elif world.player_status == PlayerState.EXPLORING:
        scope = []
    elif world.player_status == PlayerState.GO:
        scope = []
    elif world.player_status == PlayerState.EXAMINE:
        scope = ["stop"]
    elif world.player_status == PlayerState.EXIT:
        scope = []

    return scope



def check_for_valid_go_destination(player_input, world):
    error = None
    destination = None
    #Checks if the players location level is 3 or not. If it is the current locations parent is used instead.
    if not world.player_location.location_level == 3:
        # Checks if the player did enter something besides "go" or "enter"
        if len(player_input.split()) > 1:
            # Checks if the second "word" of the player input is a number
            if player_input.split()[1].isnumeric():
                # Reduces the number by one, since, contrary to popular belief amongst programmers, people usually do not start counting at zero. -.-
                player_input = int(player_input.split()[1])
                player_input -= 1
                # Checks if the desired location exists.
                if player_input in range(len(world.player_location.sublocations)):
                    # Once all the checks have been passed, the travel target is set to the desired sublocation,
                    destination = world.player_location.sublocations[player_input]

                else:
                    error = "Please choose a valid destination.\n"


            else:
                error = "Please choose a destination by inputting the appropriate number after the go/enter command.\n"

        else:
            error = "Please choose a destination by inputting the appropriate number after the go/enter command.\n"

    # Copy paste of the above, for sublocation level 3.
    else:
        if len(player_input.split()) > 1:
            if player_input.split()[1].isnumeric():
                player_input = int(player_input.split()[1])
                player_input -= 1
                if player_input in range(len(world.player_location.owner.sublocations)):
                    destination = world.player_location.owner.sublocations[player_input]

                else:
                    error = "Please choose a valid destination.\n"


            else:
                error = "Please choose a destination by inputting the appropriate number after the go/enter command.\n"

        else:
            error = "Please choose a destination by inputting the appropriate number after the go/enter command.\n"

    #Once all is set an done, this is returned to the main function.
    return {"player_choice": "go", "error": error, "destination": destination}



def check_for_valid_explore_destination(world):
    error = None
    steps = None

    #Checks if the players location level is 3 or not. If it is the current locations parent is used instead.
    if not world.player_location.location_level == 3:
        # This checks if the players current location has not yet reached its maximum number of sublocations.
        #If it does not, the number of required steps is calculated.
        if len(world.player_location.sublocations) <= world.player_location.max_sublocations:
            steps = return_steps(world.player_location, 2)
        else:
            # Tells the player there is nothing left to explore.
            error = "There is nothing left to explore.\n"
    # Same as above, but for locations of level 3.
    else:
        if len(world.player_location.owner.sublocations) <= world.player_location.owner.max_sublocations:
            steps = return_steps(world.player_location.owner, 2)
        else:
            error = "There is nothing left to explore.\n"

    #Once all is set an done, this is returned to the main function.
    return {"player_choice": "explore", "error": error, "steps": steps}


def check_for_valid_examine_object(player_input, world):
    error = None
    examine_object = None
    #Pretty much the same as the above functions, just for objects. the check for the sublocation level is not needed here.
    if len(player_input.split()) > 1:
        if player_input.split()[1].isnumeric():
            player_input = int(player_input.split()[1])
            player_input -= 1
            if player_input in range(len(world.player_location.objects)):
                examine_object = world.player_location.objects[player_input]

            else:
                error = "Please choose a valid object.\n"


        else:
            error = "Please choose an object by inputting the appropriate number after the examine command.\n"

    else:
        error = "Please choose an object by inputting the appropriate number after the examine command.\n"



    return {"player_choice": "examine", "error": error, "examine_object": examine_object}



def check_for_valid_exit_destination(world):
    error = None
    #Currently under construction, just returns an error.
    if world.player_location.location_level == 0:
        error = "I will have to [cyan]travel[/] if I want to leave the {0}.\n".format(world.player_location.name)


    return {"player_choice": "exit", "error": error}




