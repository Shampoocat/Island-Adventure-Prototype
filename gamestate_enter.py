
from worldbuilder import PlayerState

from textgenerator import *





def handle_game_state_enter(world, console, player_enter):

    #If the step buffer is empty, the player arrives at the target location. the players location is changed to the new one, some variables are reset and the gamestate is set to idle.
    if not world.step_buffer:
        console.rule(title="Going to the {0}".format(world.travel_target.name.title()), style=" white")

        world.player_location = world.travel_target

        #
        console.print("I have arrived {0} the {1}.\n".format(world.travel_target.preposition, world.travel_target.name))

        console.print("This space will eventually present you with [yellow]Events and Encounters[/].\n")

        world.travel_target = None
        world.exiting = None
        world.player_status = PlayerState.IDLE
        world.first_step = False
        player_enter = True

    #If it is the first step on the way to a location a message is shown informing the player of their familiarity with the current location.
    else:

        if world.first_step:
            console.rule(title="Going to the {0}".format(world.travel_target.name.title()), style=" white")

            world.first_step = False

            console.print("I am now headed for the {0}.\n".format(world.travel_target.name))

            if not world.player_location.location_level == 3:

                console.print("I am {0} with the {1}, this will affect my ability to safely find my way around.\n".format(return_familiarity(world.player_location), world.player_location.name))

            else:
                console.print("I am {0} with the {1}, this will affect my ability to safely find my way around.\n".format(return_familiarity(world.player_location.owner), world.player_location.owner.name))

            console.print("This space will eventually present you with [yellow]Events and Encounters[/].\n")
            player_enter = True

        # If it is neither the first, not last step taken, nothing happens. The game loops still processes the steps in the background.
        else:

            pass
            # add travel events here




    return player_enter