
from worldbuilder import PlayerState





#function to handle the player exiting, very simple as it always lasts just one step. It displays a message and will eventually house a check for some events to happen on exiting a location.
def handle_game_state_exit(world, console, player_enter):

    console.rule(title="Leaving the {0}".format(world.player_location.name.title()), style=" white")
    console.print("I am leaving the {0}.\n".format(world.player_location.name))

    world.player_location = world.player_location.owner

    console.print("This space will eventually present you with [yellow]Events and Encounters[/].\n")

    world.player_status = PlayerState.IDLE
    player_enter = True


    return player_enter