


#This stores all the data associated with object tags. This needs to be a function so the format function can work its magic properly.
#It also allows for random to be used in the future if so desired.
#More data will be stored here eventually.

def return_object_tag(tag, game_object):

    location_tags = {
        "none_tag": {},
        "concrete": {"material": "concrete"},
        "metal": {"material": "metal"},
        "bricks": {"material": "bricks"},
        "stones": {"material": "stones"},
        "wood": {"material": "wood"},
        "glass": {"material": "glass"},
        "cardboard": {"material": "cardboard"},
        "plastic": {"material": "plastic"},
        "cushioning_fabric": {"feature": "a cushioning made out of a synthetic foam, covered with fabric"},
        "cushioning_artificial_leather": {"feature": "a cushioning made out of a synthetic foam, covered with artificial leather"},
        "radar_equipment": {"feature": "some sort of radar equipment"},
        "monitors": {"feature": "several monitors"},
        "old_mattress": {"feature": "a very old mattress"},
        "old_curtains": {"feature": "the remains of some old curtains"},
        "helm": {"feature": "a helm"},
        "torn": {"message": [5, "{0} {1} torn.".format(game_object.pronoun, game_object.object_being)]},
        "ragged": {"message": [5, "{0} {1} ragged.".format(game_object.pronoun, game_object.object_being)]},
        "mangled": {"message": [5, "{0} {1} mangled.".format(game_object.pronoun, game_object.object_being)]},
        "cracked": {"message": [5, "{0} {1} cracked.".format(game_object.pronoun, game_object.object_being)]},
        "damaged": {"message": [5, "{0} {1} damaged.".format(game_object.pronoun, game_object.object_being)]},
        "rotten": {"message": [5, "{0} {1} rotten.".format(game_object.pronoun, game_object.object_being)]},
        "moldy": {"message": [5, "{0} {1} covered in mold.".format(game_object.pronoun, game_object.object_being)]},
        "rust": {"message": [5, "{0} {1} covered in rust.".format(game_object.pronoun, game_object.object_being)]},
        "ruined": {"message": [5, "{0} {1} in an utter state of ruin.".format(game_object.pronoun, game_object.object_being)]},
        "massive": {"message": [5, "The {0} {1} absolutely massive.".format(game_object.simple_name, game_object.object_being)]},
        "plane_controls": {"feature": "airplane controls"},

    }
    return location_tags.get(tag)


