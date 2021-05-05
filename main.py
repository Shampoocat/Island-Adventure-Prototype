from rich.console import Console
from worldbuilder import *
from worlddict import *
import pickle
from input import *
from gamestate_idle import *
from gamestate_exploring import *
from gamestate_enter import *
from gamestate_examine import *
from gamestate_exit import *

import os





#Extremely simple title screen, just prints out a few lines of text and waits for the player to press enter
def title_screen():
    console.rule(title="Island Adventure", style=" white")
    console.print("")
    console.print("A game by Shampoocat.", justify="center")
    console.print("")
    console.print("Please keep in mind, that this is a super early test build. There is not a lot of content and a lot of [yellow]placeholders[/]. I do appreciate you taking some time to check it "
                  "out. Any feedback is very welcome.", justify="center")
    console.print("")
    console.print("You can get a list of all possible commands by typing random garbage.", justify="center")
    console.print("")
    console.input("Press [cyan]Enter[/] to continue.")
    main_menu()

#The games main menu. Allows the player to pick between starting a new game, loading a game and exiting the program
def main_menu():
    #Prints out the menu displayed to the player
    console.rule(title="Main Menu", style=" white")
    console.print("Start a [cyan]new[/] game.\n", )
    console.print("[cyan]Load[/] a saved game.\n", )
    console.print("[cyan]Quit[/] the program.\n", )
    #Waits for player input
    player_input = input(">")

    #If the player selects new game it runs the new_game function
    if player_input == "new":
        new_game()

    #If the player selects to load a game, it unpickles the save file and runs the main game_loop function with the data from it
    elif player_input == "load":
        try:
            save_file = open('save', 'rb')
            load = pickle.load(save_file)
            save_file.close()
            game_loop(load)
        except FileNotFoundError:
            console.print("[red]WARNING!![/]", style="bold")
            console.print("No save file found!")
            console.input("Press [cyan]Enter[/] to continue.")
            main_menu()

    #Quits the program if the player selects quit
    elif player_input == "quit":
        console.print("Bye Bye.", )
        quit()

    #If the player input does not match any of the options above, it prints out a list of accepted commands. The function then calls itself again giving the player second chance.
    else:
        console.print("Possible options are:[cyan] new, load, quit.[/]", )
        main_menu()

#Function to run if new_game is selected on the main menu
def new_game():
    #Prints out some information to the player
    console.rule(title="New Game", style=" white")
    console.print("[red]WARNING!![/]", style="bold")
    console.print("Any previous Save Game Data will be erased!")
    console.print("Is this OK?\n")

    #Waits for player input
    player_input = input(">")

    #If the player confirms, they want to start, the initialize_world function is called
    if player_input == "yes" or player_input == "y":
        console.print("Alright then.\n", )
        initialize_world()

    #If the player does not want their savegame overwritten, the main_menu function is called bringing them back
    elif player_input == "no" or player_input == "n":
        console.print("No worries.\n", )
        main_menu()

    #If the player input does not match any of the options above, it prints out a list of accepted commands. The function then calls itself again giving the player second chance.
    else:
        console.print("Possible options are:[cyan] yes, y, no, n.[/]", )
        new_game()

#Function to generate the first location and create a world class to store the games data, called from either the main menu or the main function for debugging
def initialize_world():
    #Generates a location, should be a location of location_level 0 for normal gameplay, for debugging higher levels can be used, but the player will not be able to leave them.
    #Locations of the lowest level should never be used here, as they will crash the game quickly
    #In this demo the abandoned_island will be used

    #Loads the info from the world_dict in to a variable
    location_choice = return_world_dict('abandoned_island')

    #Generates a new instance of the Location class and feeds it the information from the variable
    location = Location([], location_choice[0], location_choice[1], location_choice[2], location_choice[3], location_choice[4], location_choice[5],
                               location_choice[6], location_choice[7], location_choice[8], location_choice[9],
                               location_choice[10], location_choice[12])

    #Generates objects for the starting location
    location.add_location_objects(location_choice[11])

    #Initialises a instance of the World class, it will hold pretty much all data of the game
    world = World()
    #Sets the player status to idle
    world.player_status = PlayerState.IDLE
    #Adds the starting location to the worlds location list
    world.locations.append(location)
    #Sets the players location to the starting location
    world.player_location = world.locations[0]
    #Runs the main game_loop function with the world that was just created
    world.player_location.owner = world.player_location

    game_loop(world)



#This is the main game function. right now it handles input, output and most game logic. This is suboptimal and these things should be given their own space eventually.
def game_loop(world):
    #Saves the world to the save file. Right now this is done every turn and I did not run in to any problems so far, but the game is still very small,
    #so it might need to be changed at some point
    save_file = open('save', 'wb')
    pickle.dump(world, save_file)
    save_file.close()
    #Prints out an empty spaceing line
    #Sets the current location to visited by the player
    world.player_location.visited = True
    #Updates the timescale to the current location
    world.set_timescale(world.player_location)
    #Calls the worlds process_step function. If the player is exploring or moving, a number of steps must be taken. This function will subtract one and advance time based on the timesclae.
    #It might be better to have it at the end of the function, but then it might immediately set the buffer to 0 when there is a 1 cost action being taken. I will have to rethink this.
    world.process_step()
    #resets player enter variable, if it is true, the player will be shown the "press enter to continue" message
    player_enter = False

    #This parts handles the player in their idle state
    if world.player_status == PlayerState.IDLE:
        player_enter = handle_game_state_idle(world, console, player_enter)

    #Handles everything happening when the player is exploring.
    elif world.player_status == PlayerState.EXPLORING:
        player_enter = handle_game_state_exploring(world, console, player_enter)

    #Handles everything happening when the player is moving from one location to another.
    elif world.player_status == PlayerState.GO:
        player_enter = handle_game_state_enter(world, console, player_enter)

    #Handles everything when the player is examining an object
    elif world.player_status == PlayerState.EXAMINE:
        player_enter = handle_game_state_examine(world, console, player_enter)

    #Handles everything when the player is exiting a location
    elif world.player_status == PlayerState.EXIT:
        player_enter = handle_game_state_exit(world, console, player_enter)


    #I am not 100% sure what the point of this is. I think it acts as a failsafe if the player_status somehow gets messed up or something.
    else:
        world.player_status = PlayerState.IDLE

    #If the player is not asked to just press enter and there are valid commands the player can enter, the input is taken
    if return_input_scope(world) and not player_enter:
        player_input = console.input(">")
        console.print("")

        # Creates a new "window" with the player input as a title and then prints out some sort of response to it
        console.rule(title="{0}\n".format(player_input), style="white")

        #Calls the input handler function and gets the choice and error from it
        player_input = input_handler(player_input, world)
        player_choice = player_input.get("player_choice")
        error = player_input.get("error")

        #Exacutes code based on the players input

        #If there is an error sent by the input handler, the error is shown
        if error:
            console.print(error)
            player_enter = True

        #Informs the player that traveling is not implemented
        elif player_choice == "travel":
            console.print("[yellow]Traveling[/] will be implemented later.\n")
            player_enter = True

        #Sets the object to examine in the world and changes the gamestate to examining
        elif player_choice == "examine":
            world.player_examine_object = player_input.get("examine_object")
            world.player_status = PlayerState.EXAMINE

        #Informs the player that searching is not implemented
        elif player_choice == "search":
            console.print("[yellow]Searching[/] will be implemented later.\n")
            player_enter = True

        #Adds the needed steps to the step buffer and changes the gamestate
        elif player_choice == "explore":
            steps = player_input.get("steps")
            world.step_buffer += steps
            world.first_step = True
            world.player_status = PlayerState.EXPLORING


        #Sets the destination for going to a new location, adds the steps to the buffer and changes the gamesate
        elif player_choice == "go":
            destination = player_input.get("destination")
            world.travel_target = destination
            world.step_buffer += return_steps(world.travel_target, 1)
            world.player_status = PlayerState.GO
            world.first_step = True


        # Handles the player wanting to leave a location, just switching the gamestate will do the trick
        elif player_choice == "exit":
            world.player_status = PlayerState.EXIT

        # Ends the game.
        elif player_choice == "quit":
            console.print("Bye Bye.", )
            quit()

        elif player_choice == "stop":
            world.player_examine_object = None
            world.player_status = PlayerState.IDLE


        #Shows the player the press enter message if needed
        else:
            pass
        if player_enter:
            console.input("Press [cyan]Enter[/] to continue.")


    elif player_enter:
        console.input("Press [cyan]Enter[/] to continue.")


    #Once everything is done, the game_loop calls it self again.
    game_loop(world)


#Main function to run on start of the program
if __name__ == '__main__':
    #Gets the width of the terminal. If it is too big it is set to 100
    size = os.get_terminal_size()
    size = size[0]
    if size > 100:
        size = 100
    #Initialises the real-text console with the given width
    console = Console(width=size, highlight=False)
    #Runs the title screen, with some commenting and uncommenting the initialize_world function can be run instead for debugging, skipping the menus
    #initialize_world()
    title_screen()
