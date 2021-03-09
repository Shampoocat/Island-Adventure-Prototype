from rich.console import Console
from worldbuilder import *
from worlddict import *
import pickle
from textgenerator import *
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
                        location_choice[6], location_choice[7], location_choice[8], location_choice[9], location_choice[10], location_choice[11], location_choice[12])
    location.set_location_parameters(location_choice[13])

    #Runs the Locations function to generate damages to its materials
    location.set_material_damage()

    #Initialises a instance of the World class, it will hold pretty much all data of the game
    world = World()
    #Sets the player status to idle
    world.player_status = PlayerState.IDLE
    #Adds the starting location to the worlds location list
    world.locations.append(location)
    #Sets the players location to the starting location
    world.player_location = world.locations[0]
    #Runs the main game_loop function with the world that was just created
    game_loop(world)



#This is the main game function. right now it handles input, output and most game logic. This is suboptimal and these things should be given their own space eventually.
def game_loop(world):
    #Saves the world to the save file. Right now this is done every turn and I did not run in to any problems so far, but the game is still very small,
    #so it might need to be changed at some point
    save_file = open('save', 'wb')
    pickle.dump(world, save_file)
    save_file.close()
    #Prints out an empty spaceing line
    console.print("")
    #Sets the current location to visited by the player
    world.player_location.visited = True
    #Updates the timescale to the current location
    world.set_timescale(world.player_location)
    #Calls the worlds process_step function. If the player is exploring or moving, a number of steps must be taken. This function will subtract one and advance time based on the timesclae.
    #It might be better to have it at the end of the function, but then it might immediately set the buffer to 0 when there is a 1 cost action being taken. I will have to rethink this.
    world.process_step()

    #This parts handles the player in their idle state
    if world.player_status == PlayerState.IDLE:
        #Sanity check to make sure there is no exit location stored by accident
        world.exiting = None

        #Prints out the description of the players location as well as the time of day and the light conditions
        console.rule(title="{0}".format(world.player_location.name), style=" white")
        console.print("{0}\n".format(world.player_location.description))
        console.print("{0}\n".format(world.return_time_and_light(world.player_location)))


        #Prints out options to let the player travel to sublocations of their current location
        #There is a special case here for locations of location level 3, as they do not have sublocations. Here the game uses their parent location instead. This allows the player
        #to go from one room to another room in the same building, without first going back to the building
        location_names = []
        if not world.player_location.location_level == 3:
            #If there are sublocations discovered, they are listed and printed out to the player
            if world.player_location.sublocations:
                console.print("I can [cyan]go[/] to:", )

                #The number of the location is added before printing. It needs the +1 since lists start at 0 because why not -.-
                for location in world.player_location.sublocations:
                    location_names.append(location.name)
                    location_names.append("[cyan]({0})[/]".format(str(world.player_location.sublocations.index(location) + 1)))
            #If no sublocations are known, the player is told to go and explore
            else:
                location_names.append("I do not know of any locations I could go to. I should [cyan]explore[/] this location.")

        #Same as above, but using the locations parent location instead
        else:
            if world.player_location.owner.sublocations:
                console.print("I can [cyan]go[/] to:", )

                for location in world.player_location.owner.sublocations:
                    location_names.append(location.name)
                    location_names.append("[cyan]({0})[/]".format(str(world.player_location.owner.sublocations.index(location) + 1)))

            else:
                location_names.append("I do not know of any locations I could go to. I should [cyan]explore[/] this location.")

        #Prints the entire thing to screen
        console.print(' '.join(location_names), )
        console.print("", )

        #Same as above, but with entities in the players location. there is no need to use the parent location for lv3 locations so this is gone.
        #Currently a placeholder! It does nothing.
        entities_names = []
        if world.player_location.entities:
            console.print("I can try to [cyan]examine[/],[cyan] use[/] or [cyan]pick up[/] the following objects:")

            for entity in world.player_location.entities:
                entities_names.append(entity.name)
                entities_names.append("[cyan]({0})[/]".format(str(world.player_location.sublocations.index(entity) + 1)))
        else:
            entities_names.append("I do not know of any objects around here. I should [yellow]search[/] this location.")

        console.print(' '.join(entities_names))

        console.print("")


        #Waits for player input and stores it in a variable for further use
        player_input = console.input(">")
        console.print("")

        #If the player just presses enter we end up without a proper string, this ensures there is always a string with at least one "word" in the player_input variable.
        if not player_input:
            player_input = "..."

        #Creates a new "window" with the player input as a title and then prints out some sort of response to it
        console.rule(title="{0}\n".format(player_input.capitalize()), style="white")

        #If the player wants to travel they are informed about it not being in the game yet
        if player_input.split()[0] == "travel":
                console.print("[yellow]Traveling[/] will be implemented later.\n")
                console.input("Press [cyan]Enter[/] to continue.")

        #If the player wants to search they are informed about it not being in the game yet
        if player_input.split()[0] == "search":
            console.print("[yellow]Searching for Objects[/] will be implemented later.\n")
            console.input("Press [cyan]Enter[/] to continue.")


        #If the player chooses to explore this is handled here
        elif player_input.split()[0] == "explore":
            #Once again we needs to distinguish between level 3 locations and the rest.
            if not world.player_location.location_level == 3:
                #This checks if the players current location has not yet reached its maximum number of sublocations. If it does not, the player_status is set to exploring and the number of
                #steps it take sto explore the location is saved in the world.step_buffer variable.
                if len(world.player_location.sublocations) <= world.player_location.max_sublocations:
                        world.step_buffer += return_steps(world.player_location.explore_steps)
                        world.player_status = PlayerState.EXPLORING
                else:
                    #Tells the player there is nothing left to explore.
                    console.print("There is nothing left to explore.\n")
                    console.input("Press [cyan]Enter[/] to continue.")
            #Same as above, but for locations of level 3.
            else:
                if len(world.player_location.owner.sublocations) <= world.player_location.owner.max_sublocations:
                    world.step_buffer += return_steps(world.player_location.owner.explore_steps)
                    world.player_status = PlayerState.EXPLORING
                else:
                    console.print("There is nothing left to explore.\n")
                    console.input("Press [cyan]Enter[/] to continue.")



        #Handles the player going to or entering a location.
        elif player_input.split()[0] == "go" or player_input.split()[0] == "enter":
            #Same deal with the location level again.
            if not world.player_location.location_level == 3:
                #Checks if the player did enter something besides "go" or "enter"
                if len(player_input.split()) > 1:
                    #Cheks if the second "word" of the player input is a number
                    if player_input.split()[1].isnumeric():
                        #Reduces the number by one, since, contrary to popular belief amongst programmers, people usually do not start counting at zero. -.-
                        player_input = int(player_input.split()[1])
                        player_input -= 1
                        #Cheks if the desired location exists.
                        if player_input in range(len(world.player_location.sublocations)):
                            #Once all the checks have been passed, the travel target is set to the desired sublocation,
                            #the steps_buffer variable is filled with the number of steps needed to get there and the player_status is set to traveling
                            world.travel_target = world.player_location.sublocations[player_input]
                            world.step_buffer += return_steps(world.travel_target.travel_steps)
                            world.player_status = PlayerState.TRAVELING
                        else:
                            console.print("Please choose a valid destination.\n")
                            console.input("Press [cyan]Enter[/] to continue.")

                    else:
                        console.print("Please choose a destination by inputting the appropriate number after the go/enter command.\n")
                        console.input("Press [cyan]Enter[/] to continue.")

                else:
                    console.print("Please choose a destination by inputting the appropriate number after the go/enter command.\n")
                    console.input("Press [cyan]Enter[/] to continue.")
            #Copy paste of the above, for sublocation level 3.
            else:
                if len(player_input.split()) > 1:
                    if player_input.split()[1].isnumeric():
                        player_input = int(player_input.split()[1])
                        player_input -= 1
                        if player_input in range(len(world.player_location.owner.sublocations)):
                            world.travel_target = world.player_location.owner.sublocations[player_input]
                            world.step_buffer += return_steps(world.travel_target.travel_steps)
                            world.player_status = PlayerState.TRAVELING



                        else:
                            console.print("Please choose a valid destination.\n")
                            console.input("Press [cyan]Enter[/] to continue.")


                    else:
                        console.print("Please choose a destination by inputting the appropriate number after the go command.\n")
                        console.input("Press [cyan]Enter[/] to continue.")

                else:
                    console.print("Please choose a destination by inputting the appropriate number after the go command.\n")
                    console.input("Press [cyan]Enter[/] to continue.")



        #Handles the player wanting to leave a location
        elif player_input.split()[0] == "leave" or player_input.split()[0] == "exit":
            #If the players location level is 0, they are told to travel instead, as these locations have no parent.
            if world.player_location.location_level == 0:
                console.print("I will have to [cyan]travel[/] if I want to leave the {0}.\n".format(world.player_location.name))
                console.input("Press [cyan]Enter[/] to continue.")

            #If the location can be exited, the exiting location is set to the current location, the target location is set to the current locations parent location.
            #The player_status and step_buffer are once again updated. The exit_first_step bool is set to true, it will be used later.
            else:
                world.exiting = world.player_location
                world.travel_target = world.player_location.owner
                world.step_buffer += return_steps(world.exiting.travel_steps)
                world.player_status = PlayerState.TRAVELING
                world.exit_first_step = True

        #Ends the game.
        elif player_input.split()[0] == "quit":
            console.print("Bye Bye.", )
            quit()

        #If the player enters an invalid command, the possible commands are shown to them.
        else:
            console.print("Possible options are:[cyan] go, enter, leave, exit, explore, search, travel, quit.[/]", )
            console.input("Press [cyan]Enter[/] to continue.")

    #Handles everything happening when the player is exploring.
    elif world.player_status == PlayerState.EXPLORING:
        #Once again the location_level is checked. This is handles much less gracefully here than above, as it checks over an dover again and it only gets worse down the line.
        #This should be refactored, but since I want to move most of this stuff in to its own files, I won't waste my time on it now.
        if not world.player_location.location_level == 3:

            console.rule(title="Exploring the {0}".format(world.player_location.name), style=" white")
        else:
            console.rule(title="Exploring the {0}".format(world.player_location.owner.name), style=" white")

        #If there are no steps left in thr steps_buffer, a new sublocation is generated and the player_status is set to idle.
        if not world.step_buffer:
            if not world.player_location.location_level == 3:

                world.player_location.add_sublocation()
                console.print("{0}\n".format(world.player_location.sublocations[-1].description_on_discovery))
            else:
                world.player_location.owner.add_sublocation()
                console.print("{0}\n".format(world.player_location.owner.sublocations[-1].description_on_discovery))

            world.player_status = PlayerState.IDLE

        #If there are still steps to take, the player is told that they are still exploring. This will at some point allow random events and stuff to fire.
        #There is no player input being processed here for now. But once events are a thing, the player will need to be able to react to them. There should at some point also
        #be a way for the player to access their inventory or maybe even set up camp on longer explorations. This is why I really need a dedicated function to handle player input.
        #Otherwise I would have to have the entire input logic in here again.
        else:
            if not world.player_location.location_level == 3:
                console.print("I am exploring the {0}\n".format(world.player_location.name))
                console.print("This space will eventually present you with [yellow]Events and Encounters[/].\n")

            else:
                console.print("I am exploring the {0}\n".format(world.player_location.owner.name))
                console.print("This space will eventually present you with [yellow]Events and Encounters[/].\n")

        if not world.player_location.location_level == 3:

            console.print("{0}\n".format(world.return_time_and_light(world.player_location)))
        else:
            console.print("{0}\n".format(world.return_time_and_light(world.player_location.owner)))


        console.input("Press [cyan]Enter[/] to continue.")

    #Handles everything happening when the player is moving from one location to another.
    elif world.player_status == PlayerState.TRAVELING:
        console.rule(title="Going to the {0}".format(world.travel_target.name), style=" white")

        #If there is nothing left in the step_buffer, the player will arrive at their target.
        if not world.step_buffer:
            #The players location is set to the target location.
            world.player_location = world.travel_target


            #If the player was entering a location the description_on_enter is shown to the player. Otherwise a fairly generic message from the text generator is shown.
            #This prevents strange cases where the player, leaving a room inside a house surrounded by a fence, would be shown a message about them climbing over the fence to get to the house.
            #There would still be a message when the player takes the first step out of the room, this is handled a bit further down.
            if not world.exiting:
                console.print("{0}\n".format(world.player_location.description_on_enter))
            else:
                console.print("{0}\n".format(return_being(world.player_location)))
            console.print("This space will eventually present you with [yellow]Events and Encounters[/].\n")

            #Cleares some variables to prevent any nonsense from happening. Player_status is set to idle.
            world.travel_target = None
            world.exiting = None
            world.player_status = PlayerState.IDLE
            world.exit_first_step = False


        #If there are still steps to take before the player arrives, this is handled here.
        else:
            #If the player is exiting a location and it is the first message shown to the player regarding their movement, the description_on_exit text is shown to them.
            if world.exit_first_step:
                world.exit_first_step = False

                console.print("{0}\n".format(world.exiting.description_on_exit))
                console.print("I am now headed for the {0}.\n".format(world.travel_target.name))
                console.print("This space will eventually present you with [yellow]Events and Encounters[/].\n")

            #If the exit_first_step is false, a generic message is shown instead. It does not matter if the player is exiting or entering in this case.
            else:

                console.print("I am going to the {0}.\n".format(world.travel_target.name))
                console.print("This space will eventually present you with [yellow]Events and Encounters[/].\n")

        #This is just a hot mess, don't pay any attention to it as it is guaranteed to change sooner rather than later.
        #It deals with showing the time and light message under different circumstances when moving from one lv3 sublocaion to another.
        if world.exiting:
            console.print("{0}\n".format(world.return_time_and_light(world.travel_target)))
        else:
            if not world.player_location.location_level == 3:
                console.print("{0}\n".format(world.return_time_and_light(world.player_location)))
            else:
                if not world.step_buffer:
                    console.print("{0}\n".format(world.return_time_and_light(world.player_location)))
                else:
                    console.print("{0}\n".format(world.return_time_and_light(world.player_location.owner)))

        console.input("Press [cyan]Enter[/] to continue.")

    #I am not 100% sure what the point of this is. I think it acts as a failsafe if the player_status somehow gets messed up or something.
    else:
        world.player_status = PlayerState.IDLE

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
