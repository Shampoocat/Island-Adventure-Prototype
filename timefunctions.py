



#simple function to transform the daytime variable from an number in to a description to be shown tot he player
def return_daytime(time):
    if 0 <= time < 180:
        return 'Night'
    elif 180 <= time < 360:
        return 'Dawn'
    elif 360 <= time < 510:
        return 'Early Morning'
    elif 510 <= time <= 720:
        return 'Late Morning'
    elif 720 <= time < 900:
        return 'Early Afternoon'
    elif 900 <= time < 1200:
        return 'Late Afternoon'
    elif 1200 <= time <= 1380:
        return 'Dusk'
    else:
        return 'Night'


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
