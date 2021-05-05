



#simple function to transform the daytime variable from an number in to a description to be shown to the player
def return_daytime(time):
    if 0 <= time < 180:
        return 'night'
    elif 180 <= time < 360:
        return 'dawn'
    elif 360 <= time < 510:
        return 'early morning'
    elif 510 <= time <= 720:
        return 'late morning'
    elif 720 <= time < 900:
        return 'early afternoon'
    elif 900 <= time < 1200:
        return 'late afternoon'
    elif 1200 <= time <= 1380:
        return 'dusk'
    else:
        return 'night'


#simple function that sets the base light level of the world based on the tine of day
def return_light_daytime(time):
    if 0 <= time < 180:
        return 2
    elif 180 <= time < 360:
        return 2
    elif 360 <= time < 510:
        return 3
    elif 510 <= time <= 720:
        return 4
    elif 720 <= time < 900:
        return 4
    elif 900 <= time < 1200:
        return 3
    elif 1200 <= time <= 1380:
        return 2
    elif 1380 <= time <= 1440:
        return 2
