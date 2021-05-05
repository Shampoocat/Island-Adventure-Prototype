from worldbuilder import PlayerState
from textgenerator import *




def handle_game_state_exploring(world, console, player_enter):

    #If there are no more steps to take the new location is generated and the gamestate is reset
    if not world.step_buffer:
        if not world.player_location.location_level == 3:
            console.rule(title="Exploring the {0}".format(world.player_location.name.title()), style=" white")

            world.player_location.add_sublocation()
            console.print("{0}\n".format(generate_description(world.player_location.sublocations[-1], "discovery", world)))

        else:
            console.rule(title="Exploring the {0}".format(world.player_location.owner.name.title()), style=" white")

            world.player_location.owner.add_sublocation()
            console.print("{0}\n".format(generate_description(world.player_location.owner.sublocations[-1], "discovery", world)))

        if not world.player_location.location_level == 3:

            console.print("{0}\n".format(world.return_time_and_light(world.player_location)))
        else:
            console.print("{0}\n".format(world.return_time_and_light(world.player_location.owner)))

        world.player_status = PlayerState.IDLE
        player_enter = True


    #If it is the first step taken on an exploration, a message is shown informing the player of their familiarity with the location.
    elif world.first_step:
        world.first_step = False
        if not world.player_location.location_level == 3:
            console.rule(title="Exploring the {0}".format(world.player_location.name.title()), style=" white")

            console.print("I am {0} with the {1}, this will affect my ability to safely find my way around.\n".format(return_familiarity(world.player_location), world.player_location.name))
            console.print("This space will eventually present you with [yellow]Events and Encounters[/].\n")

        else:
            console.rule(title="Exploring the {0}".format(world.player_location.owner.name.title()), style=" white")

            console.print("I am {0} with the {1}, this will affect my ability to safely find my way around.\n".format(return_familiarity(world.player_location.owner), world.player_location.owner.name))
            console.print("This space will eventually present you with [yellow]Events and Encounters[/].\n")

        if not world.player_location.location_level == 3:

            console.print("{0}\n".format(world.return_time_and_light(world.player_location)))
        else:
            console.print("{0}\n".format(world.return_time_and_light(world.player_location.owner)))
        player_enter = True

    #If it is neither the first, not last step taken, nothing happens. The game loops still processes the steps in the background.
    else:
        pass
        #add exploration events here



    return player_enter


