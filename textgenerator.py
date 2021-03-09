
from materialdict import *

#Note: since these are in large parts just copy pastes of one another, I will only comment some of them. Look at: return_description, return_being and return_construction_material.




#Function to return the description of a location, to be shown to the player.
def return_description(location):
    results = []

    #The return_being function is always used. Everything else is optional and only called if needed.
    results.append(return_being(location))
    if location.situated:
        results.append(return_situated(location))
    if location.flavor_text:
        results.append(return_flavor_text(location))
    if location.topography:
        results.append(return_topography_objects(location))
    if location.construction_material:
        results.append(return_construction_material(location))
    if location.natural_material:
        results.append(return_natural_material(location))
    if location.surrounded:
        results.append(return_surrounded(location))
    if location.scattered_objects:
        results.append(return_scattered_objects(location))
    if location.environmental_effects:
        results.append(return_environment(location))
    if location.fauna:
        results.append(return_fauna(location))
    if location.flora:
        results.append(return_flora(location))


    results = " ".join(results)
    return results


def return_discovery(location):
    results = []
    results.append(discovery_base(location))
    if location.situated:
        results.append(return_situated(location))
    if location.topography:
        results.append(return_topography_objects(location))
    if location.surrounded:
        results.append(return_surrounded(location))
    if location.access:
        results.append(return_access(location))
    results = " ".join(results)

    return results


def return_enter(location):
    results = []
    if location.situated:
        results.append(return_situated_enter(location))
    if location.surrounded:
        results.append(return_surrounded_enter(location))
    if location.access:
        results.append(return_access_enter(location))
    results.append("{0}".format(return_access_being(location)))
    results = " ".join(results)
    return results



def return_exit(location):
    results = []
    if location.access:
        results.append(return_access_exit(location))
    if location.surrounded:
        results.append(return_surrounded_exit(location))
    if location.situated:
        results.append(return_situated_exit(location))
    results = " ".join(results)
    return results





def return_being_exit(location):
    results = []
    name = location.name
    if location.size:
        name = "{0} {1}".format(location.size, name)
    if not location.water:
        if location.being:
            results.append("I am once again {0} {1} the {2}.".format(location.being, location.preposition, name))
        else:
            results.append("I am once again {0} the {1}.".format(location.preposition, name))
    else:
        if location.water[0] == 0:
            if location.being:
                results.append("I am once again {0} {1} the {2}. There is a thin film of {3} water here.".format(location.being, location.preposition, name, location.water[1]))
            else:
                results.append("I am once again {0} the {1}. There is a thin film of {2} water here.".format(location.preposition, name, location.water[1]))
        elif location.water[0] == 1:
            results.append("I am once again wading through the {0} water of the {1}. It reaches to my ankles.".format(location.water[1], name))
        elif location.water[0] == 2:
            results.append("I am once again wading through the {0} water of the {1}. It reaches to my knees.".format(location.water[1], name))
        elif location.water[0] == 3:
            results.append("I am once again wading through the {0} water of the {1}. It reaches to my chest.".format(location.water[1], name))
        elif location.water[0] == 4:
            results.append("I am once again swimming in the {0} water of the {1}. I can barely stand here.".format(location.water[1], name))
        elif location.water[0] == 5:
            results.append("I am once again swimming in the {0} water of the {1}. It is barely too deep for me to stand.".format(location.water[1], name))
        elif location.water[0] == 6:
            results.append("I am once again swimming in the {0} water of the {1}. It is way too deep for me to stand.".format(location.water[1], name))
        elif location.water[0] == 7:
            results.append("I am once again swimming in the {0} water of the {1}. I can't even guess how deep it might be.".format(location.water[1], name))

    results = " ".join(results)
    return results



def return_situated_exit(location):
    results = []
    situation = location.situated
    if situation:
        if location.surrounded or location.access:
            material_results = "Then I {0} in order to leave the {1}.".format(random.sample(SituatedObjects.objects[situation[0]]['exit_message'], k=1)[0], location.alias)
        elif location.surrounded and location.access:
            material_results = "Finally I {0} in order to leave the {1}.".format(random.sample(SituatedObjects.objects[situation[0]]['exit_message'], k=1)[0], location.alias)
        else:
            material_results = "I {0} in order to leave the {1}.".format(random.sample(SituatedObjects.objects[situation[0]]['exit_message'], k=1)[0], location.alias)
        results.append(material_results)
    results = "".join(results)
    return results


def return_surrounded_exit(location):
    results = []
    surrounding_objects = location.surrounded
    if surrounding_objects:
        if len(surrounding_objects) == 1:
            if location.access:
                material_results = "Then my path is blocked again by {0}{1}. After a while {2}.".format(Surrounded.objects[surrounding_objects[0]]['preposition'], Surrounded.objects[surrounding_objects[0]]['name'], random.sample(SituatedObjects.objects[surrounding_objects[0]]['exit_message'], k=1)[0])
            else:
                material_results = "My path is blocked again by {0}{1}. After a while {2}.".format(Surrounded.objects[surrounding_objects[0]]['preposition'], Surrounded.objects[surrounding_objects[0]]['name'], random.sample(SituatedObjects.objects[surrounding_objects[0]]['exit_message'], k=1)[0])

            results.append(material_results)
        else:
            material_results = []
            for surrounding_object in surrounding_objects:
                index = surrounding_objects.index(surrounding_object)
                if index == 0:
                    material_results.append("{1}{0}".format(Surrounded.objects[surrounding_object]['name'], Surrounded.objects[surrounding_object]['preposition']))
                elif index == len(surrounding_objects) -1:
                    material_results.append(" and {1}{0}".format(Surrounded.objects[surrounding_object]['name'], Surrounded.objects[surrounding_object]['preposition']))
                else:
                    material_results.append(", {1}{0}".format(Surrounded.objects[surrounding_object]['name'], Surrounded.objects[surrounding_object]['preposition']))
            material_results = "".join(material_results)
            if location.access:
                material_results = "Then my path is blocked again by {0}. It takes some effort, but I eventually make my way past them.".format(material_results, location.alias)

            else:
                material_results = "My path is blocked again by {0}. It takes some effort, but I eventually make my way past them.".format(material_results, location.alias)
            results.append(material_results)


    results = "".join(results)
    return results


def return_access_exit(location):
    results = []
    situation = location.access
    if situation:
        if location.surrounded or location.situated:
            material_results = "First I {0} from the {1}.".format(random.sample(AccessMethods.methods[situation[0]]['exit_message'], k=1)[0], location.name)
        else:
            material_results = "I {0} from the {1}.".format(random.sample(AccessMethods.methods[situation[0]]['exit_message'], k=1)[0], location.name)
        results.append(material_results)
    results = "".join(results)
    return results



def return_situated_enter(location):
    results = []
    situation = location.situated
    if situation:
        if location.surrounded or location.access:
            material_results = "First I {0} in order to reach the {1}.".format(random.sample(SituatedObjects.objects[situation[0]]['enter_message'], k=1)[0], location.alias)
        else:
            material_results = "I {0} in order to reach the {1}.".format(random.sample(SituatedObjects.objects[situation[0]]['enter_message'], k=1)[0], location.alias)
        results.append(material_results)
    results = "".join(results)
    return results


def return_surrounded_enter(location):
    results = []
    surrounding_objects = location.surrounded
    if surrounding_objects:
        if len(surrounding_objects) == 1:
            if location.situated:
                material_results = "Then my path is blocked by {0}{1}. After a while {2}.".format(Surrounded.objects[surrounding_objects[0]]['preposition'], Surrounded.objects[surrounding_objects[0]]['name'], random.sample(SituatedObjects.objects[surrounding_objects[0]]['enter_message'], k=1)[0])
            else:
                material_results = "My path is blocked by {0}{1}. After a while {2}.".format(Surrounded.objects[surrounding_objects[0]]['preposition'], Surrounded.objects[surrounding_objects[0]]['name'], random.sample(SituatedObjects.objects[surrounding_objects[0]]['enter_message'], k=1)[0])

            results.append(material_results)
        else:
            material_results = []
            for surrounding_object in surrounding_objects:
                index = surrounding_objects.index(surrounding_object)
                if index == 0:
                    material_results.append("{1}{0}".format(Surrounded.objects[surrounding_object]['name'], Surrounded.objects[surrounding_object]['preposition']))
                elif index == len(surrounding_objects) -1:
                    material_results.append(" and {1}{0}".format(Surrounded.objects[surrounding_object]['name'], Surrounded.objects[surrounding_object]['preposition']))
                else:
                    material_results.append(", {1}{0}".format(Surrounded.objects[surrounding_object]['name'], Surrounded.objects[surrounding_object]['preposition']))
            material_results = "".join(material_results)
            if location.situated:
                material_results = "Then my path is blocked by {0}. It takes some effort, but I eventually make my way past them.".format(material_results, location.alias)

            else:
                material_results = "My path is blocked by {0}. It takes some effort, but I eventually make my way past them.".format(material_results, location.alias)
            results.append(material_results)


    results = "".join(results)
    return results


def return_access_enter(location):
    results = []
    situation = location.access
    if situation:
        if location.surrounded and location.situated:
            material_results = "Finally I can {0} {1} to the {2}.".format(random.sample(AccessMethods.methods[situation[0]]['enter_message'], k=1)[0], location.preposition, location.name)
        elif location.surrounded or location.situated:
            material_results = "Then I {0} {1} to the {2}.".format(random.sample(AccessMethods.methods[situation[0]]['enter_message'], k=1)[0], location.preposition, location.name)
        else:
            material_results = "I {0} {1} to the {2}.".format(random.sample(AccessMethods.methods[situation[0]]['enter_message'], k=1)[0], location.preposition, location.name)
        results.append(material_results)
    results = "".join(results)
    return results


def return_access_being(location):
    results = []
    name = location.name
    if location.size:
        name = "{0} {1}".format(location.size, name)
    if not location.water:
        if location.being:
            results.append("I am now {0} {1} the {2}.".format(location.being, location.preposition, name))
        else:
            results.append("I am now {0} the {1}.".format(location.preposition, name))
    else:
        if location.water[0] == 0:
            if location.being:
                results.append("I am now {0} {1} the {2}. There is a thin film of {3} water here.".format(location.being, location.preposition, name, location.water[1]))
            else:
                results.append("I am now {0} the {1}. There is a thin film of {2} water here.".format(location.preposition, name, location.water[1]))
        elif location.water[0] == 1:
            results.append("I am now wading through the {0} water of the {1}. It reaches to my ankles.".format(location.water[1], name))
        elif location.water[0] == 2:
            results.append("I am now wading through the {0} water of the {1}. It reaches to my knees.".format(location.water[1], name))
        elif location.water[0] == 3:
            results.append("I am now wading through the {0} water of the {1}. It reaches to my chest.".format(location.water[1], name))
        elif location.water[0] == 4:
            results.append("I am now swimming in the {0} water of the {1}. I can barely stand here.".format(location.water[1], name))
        elif location.water[0] == 5:
            results.append("I am now swimming in the {0} water of the {1}. It is barely too deep for me to stand.".format(location.water[1], name))
        elif location.water[0] == 6:
            results.append("I am now swimming in the {0} water of the {1}. It is way too deep for me to stand.".format(location.water[1], name))
        elif location.water[0] == 7:
            results.append("I am now swimming in the {0} water of the {1}. I can't even guess how deep it might be.".format(location.water[1], name))

    results = " ".join(results)
    return results







def discovery_base(location):
    results = []
    name = location.name
    if location.size:
        name = "{0} {1}".format(location.size, name)
    else:
        name = location.name

    results.append("My exploration has revealed {1}{0}.".format(name, location.article))
    if location.water and not location.indoors:
        if location.water[0] == 0:
            results.append("There seems to be a thin film of {0} water there.".format(location.water[1]))
        elif location.water[0] == 1:
            results.append("There seems to be shallow {0} water there.".format(location.water[1]))
        elif location.water[0] == 2:
            results.append("There seems to be shallow {0} water there.".format(location.water[1]))
        elif location.water[0] == 3:
            results.append("There seems to be shallow {0} water there.".format(location.water[1]))
        elif location.water[0] == 4:
            results.append("There seems to be deep {0} water there.".format(location.water[1]))
        elif location.water[0] == 5:
            results.append("There seems to be deep {0} water there.".format(location.water[1]))
        elif location.water[0] == 6:
            results.append("There seems to be deep {0} water there.".format(location.water[1]))
        elif location.water[0] == 7:
            results.append("There seems to be deep {0} water there.".format(location.water[1]))


    results = " ".join(results)

    return results



#Function to generate the initial "I am standing around in a soandso" sentence at the beginning of each description.
def return_being(location):
    results = []
    name = location.name
    #If a size is given, the size is added to the location name
    if location.size:
        name = "{0} {1}".format(location.size, name)
    #If there is no water at the location, we generate the message.
    if not location.water:
        #If the location.being value is set, this value is used in the message, otherwise a generic message is used.
        if location.being:
            results.append("I am {0} {1} the {2}.".format(location.being, location.preposition, name))
        else:
            results.append("I am {0} the {1}.".format(location.preposition, name))
    #If the location has water, this is accounted for in the message. If the water level is high enough, a special message is generated about the player wading or swimming in the water.
    else:
        #The lowest water level does not generate a special message and just informs the player of the water being there.
        if location.water[0] == 0:
            if location.being:
                results.append("I am {0} {1} the {2}. There is a thin film of {3} water here.".format(location.being, location.preposition, name, location.water[1]))
            else:
                results.append("I am {0} the {1}. There is a thin film of {2} water here.".format(location.preposition, name, location.water[1]))
        #If the water level is high enough, a special message is generated.
        elif location.water[0] == 1:
            results.append("I am wading through the {0} water of the {1}. It reaches to my ankles.".format(location.water[1], name))
        elif location.water[0] == 2:
            results.append("I am wading through the {0} water of the {1}. It reaches to my knees.".format(location.water[1], name))
        elif location.water[0] == 3:
            results.append("I am wading through the {0} water of the {1}. It reaches to my chest.".format(location.water[1], name))
        elif location.water[0] == 4:
            results.append("I am swimming in the {0} water of the {1}. I can barely stand here.".format(location.water[1], name))
        elif location.water[0] == 5:
            results.append("I am swimming in the {0} water of the {1}. It is barely too deep for me to stand.".format(location.water[1], name))
        elif location.water[0] == 6:
            results.append("I am swimming in the {0} water of the {1}. It is way too deep for me to stand.".format(location.water[1], name))
        elif location.water[0] == 7:
            results.append("I am swimming in the {0} water of the {1}. I can't even guess how deep it might be.".format(location.water[1], name))

    results = " ".join(results)
    return results

#Generates a message describing the construction materials.
def return_construction_material(location):
    results = []
    #First we must check to see what material groups have been used.
    base_material = location.construction_material.get("base_material")
    secondary_material = location.construction_material.get("secondary_material")
    repair_material = location.construction_material.get("repair_material")

    if base_material:
        #We check if there is more than one material.
        if len(base_material) == 1:
            #If there is just one material, the message is generated. If the material appears in singular/plural needs to be taken in to account as well.
            if not ConstructionMaterials.materials[base_material[0]]['plural']:
                material_results = "{0} seems to be the primary construction material used.".format(ConstructionMaterials.materials[base_material[0]]['name'])
            else:
                material_results = "{0} seem to be the primary construction material used.".format(ConstructionMaterials.materials[base_material[0]]['name'])
            results.append(material_results)
            #If there is more than one material, we go over them and generate one of three messages, one for the first, one for the last and one for anything in between.
        else:
            material_results = []
            for material in base_material:
                index = base_material.index(material)
                if index == 0:
                    material_results.append(ConstructionMaterials.materials[material]['name'])
                elif index == len(base_material) -1:
                    material_results.append(" and {0}".format(ConstructionMaterials.materials[material]['name']))
                else:
                    material_results.append(", {0}".format(ConstructionMaterials.materials[material]['name']))
            #These messages are then combined in to one sentence.
            material_results = "".join(material_results)
            material_results = "{0} seem to be the primary construction materials used.".format(material_results)
            results.append(material_results)

        #If there are damages done to the material, we generate a message for each material that has been damaged, describing the damage.
        base_damage = location.construction_material.get("primary_damage")
        if base_damage:
            for material in base_material:
                if material in base_damage:
                    material_results = " The {0} {1} {2}.".format(ConstructionMaterials.materials[material]['name'], return_damage_prefixes(ConstructionMaterials.damages.get(base_damage[material])['prefix'], ConstructionMaterials.materials[material]['plural']),
                                                                  ConstructionMaterials.damages.get(base_damage[material])['name'])
                    results.append(material_results)


    #The same process is then repeated for any other material group.
    if secondary_material:
        if len(secondary_material) == 1:
            if not ConstructionMaterials.materials[secondary_material[0]]['plural']:
                material_results = " It appears some {0} was also used in the construction of the {1}.".format(ConstructionMaterials.materials[secondary_material[0]]['name'], location.alias)
            else:
                material_results = " It appears some {0} were also used in the construction of the {1}.".format(ConstructionMaterials.materials[secondary_material[0]]['name'], location.alias)
            results.append(material_results)
        else:
            material_results = []
            for material in secondary_material:
                index = secondary_material.index(material)
                if index == 0:
                    material_results.append(ConstructionMaterials.materials[material]['name'])
                elif index == len(secondary_material) - 1:
                    material_results.append(" and {0}".format(ConstructionMaterials.materials[material]['name']))
                else:
                    material_results.append(", {0}".format(ConstructionMaterials.materials[material]['name']))
            material_results = "".join(material_results)
            material_results = " It appears some {0} were also used in the construction of the {1}.".format(material_results, location.alias)
            results.append(material_results)
        secondary_damage = location.construction_material.get("secondary_damage")
        if secondary_damage:
            for material in secondary_material:
                if material in secondary_damage:

                    material_results = " The {0} {1} {2}.".format(ConstructionMaterials.materials[material]['name'], return_damage_prefixes(ConstructionMaterials.damages.get(secondary_damage[material])['prefix'], ConstructionMaterials.materials[material]['plural']),
                                                                  ConstructionMaterials.damages.get(secondary_damage[material])['name'])
                    results.append(material_results)





    if repair_material:
        if len(repair_material) == 1:
            if not ConstructionMaterials.materials[repair_material[0]]['plural']:
                material_results = " By the looks of it some one attempted to do some repairs to the structure using {0}.".format(ConstructionMaterials.materials[repair_material[0]]['name'])
            else:
                material_results = " By the looks of it some one attempted to do some repairs to the structure using {0}.".format(ConstructionMaterials.materials[repair_material[0]]['name'])
            results.append(material_results)
        else:
            material_results = []
            for material in repair_material:
                index = repair_material.index(material)
                if index == 0:
                    material_results.append(ConstructionMaterials.materials[material]['name'])
                elif index == len(repair_material) - 1:
                    material_results.append(" and {0}".format(ConstructionMaterials.materials[material]['name']))
                else:
                    material_results.append(", {0}".format(ConstructionMaterials.materials[material]['name']))
            material_results = "".join(material_results)
            material_results = " By the looks of it some one attempted to do some repairs to the structure using {0}.".format(material_results)
            results.append(material_results)
        repair_damage = location.construction_material.get("repair_damage")
        if repair_damage:
            for material in repair_material:
                if material in repair_damage:

                    material_results = " The {0} {1} {2}.".format(ConstructionMaterials.materials[material]['name'], return_damage_prefixes(ConstructionMaterials.damages.get(repair_damage[material])['prefix'], ConstructionMaterials.materials[material]['plural']),
                                                                  ConstructionMaterials.damages.get(repair_damage[material])['name'])
                    results.append(material_results)





    results = "".join(results)
    return results


def return_natural_material(location):
    results = []
    base_material = location.natural_material.get("base_material")
    secondary_material = location.natural_material.get("secondary_material")
    anthropogenic_material = location.natural_material.get("anthropogenic_material")

    if base_material:
        if len(base_material) == 1:
            if not NaturalMaterials.materials[base_material[0]]['plural']:
                material_results = "{0} seems to be the preeminent material found {2} the {1}.".format(NaturalMaterials.materials[base_material[0]]['name'], location.alias, location.preposition)
            else:
                material_results = "{0} seem to be the preeminent material found {2} the {1}.".format(NaturalMaterials.materials[base_material[0]]['name'], location.alias, location.preposition)
            results.append(material_results)
        else:
            material_results = []
            for material in base_material:
                index = base_material.index(material)
                if index == 0:
                    material_results.append(NaturalMaterials.materials[material]['name'])
                elif index == len(base_material) -1:
                    material_results.append(" and {0}".format(NaturalMaterials.materials[material]['name']))
                else:
                    material_results.append(", {0}".format(NaturalMaterials.materials[material]['name']))
            material_results = "".join(material_results)
            material_results = "{0} seem to be the preeminent materials found {2} the {1}.".format(material_results, location.alias, location.preposition)
            results.append(material_results)
        base_damage = location.natural_material.get("primary_damage")
        if base_damage:
            for material in base_material:
                if material in base_damage:

                    material_results = " The {0} {1} {2}.".format(NaturalMaterials.materials[material]['name'], return_damage_prefixes(NaturalMaterials.damages.get(base_damage[material])['prefix'], NaturalMaterials.materials[material]['plural']),
                                                                  NaturalMaterials.damages.get(base_damage[material])['name'])
                    results.append(material_results)



    if secondary_material:
        if len(secondary_material) == 1:
            if not NaturalMaterials.materials[secondary_material[0]]['plural']:
                material_results = " Some {0} can be found here as well.".format(NaturalMaterials.materials[secondary_material[0]]['name'])
            else:
                material_results = " Some {0} can be found here as well.".format(NaturalMaterials.materials[secondary_material[0]]['name'])
            results.append(material_results)
        else:
            material_results = []
            for material in secondary_material:
                index = secondary_material.index(material)
                if index == 0:
                    material_results.append(NaturalMaterials.materials[material]['name'])
                elif index == len(secondary_material) - 1:
                    material_results.append(" and {0}".format(NaturalMaterials.materials[material]['name']))
                else:
                    material_results.append(", {0}".format(NaturalMaterials.materials[material]['name']))
            material_results = "".join(material_results)
            material_results = " Some {0} can be found here as well.".format(material_results)
            results.append(material_results)
        secondary_damage = location.natural_material.get("secondary_damage")
        if secondary_damage:
            for material in secondary_material:
                if material in secondary_damage:

                    material_results = " The {0} {1} {2}.".format(NaturalMaterials.materials[material]['name'], return_damage_prefixes(NaturalMaterials.damages.get(secondary_damage[material])['prefix'], NaturalMaterials.materials[material]['plural']),
                                                                  NaturalMaterials.damages.get(secondary_damage[material])['name'])
                    results.append(material_results)





    if anthropogenic_material:
        if len(anthropogenic_material) == 1:
            if not NaturalMaterials.materials[anthropogenic_material[0]]['plural']:
                material_results = " I can also see some {0} that someone has left here.".format(NaturalMaterials.materials[anthropogenic_material[0]]['name'])
            else:
                material_results = " I can also see some {0} that someone has left here.".format(NaturalMaterials.materials[anthropogenic_material[0]]['name'])
            results.append(material_results)
        else:
            material_results = []
            for material in anthropogenic_material:
                index = anthropogenic_material.index(material)
                if index == 0:
                    material_results.append(NaturalMaterials.materials[material]['name'])
                elif index == len(anthropogenic_material) - 1:
                    material_results.append(" and {0}".format(NaturalMaterials.materials[material]['name']))
                else:
                    material_results.append(", {0}".format(NaturalMaterials.materials[material]['name']))
            material_results = "".join(material_results)
            material_results = " I can also see some {0} that someone has left here.".format(material_results)
            results.append(material_results)
        repair_damage = location.natural_material.get("repair_damage")
        if repair_damage:
            for material in anthropogenic_material:
                if material in repair_damage:

                    material_results = " The {0} {1} {2}.".format(NaturalMaterials.materials[material]['name'], return_damage_prefixes(NaturalMaterials.damages.get(repair_damage[material])['prefix'], NaturalMaterials.materials[material]['plural']),
                                                                  NaturalMaterials.damages.get(repair_damage[material])['name'])
                    results.append(material_results)





    results = "".join(results)
    return results




def return_fauna(location):
    results = []
    fauna = location.fauna


    if fauna:
        if len(fauna) == 1:
            material_results = "Plenty of {0} call this place their home.".format(Fauna.animals[fauna[0]]['name'])
            results.append(material_results)
        else:
            material_results = []
            for animal in fauna:
                index = fauna.index(animal)
                if index == 0:
                    material_results.append(Fauna.animals[animal]['name'])
                elif index == len(fauna) -1:
                    material_results.append(" and {0}".format(Fauna.animals[animal]['name']))
                else:
                    material_results.append(", {0}".format(Fauna.animals[animal]['name']))
            material_results = "".join(material_results)
            material_results = "Plenty of {0} call this place their home.".format(material_results)
            results.append(material_results)


    results = "".join(results)
    return results


def return_flora(location):
    results = []
    flora = location.flora


    if flora:
        if len(flora) == 1:
            if not Flora.plants[flora[0]]['plural']:
                material_results = "{0} is growing all over the {1}.".format(Flora.plants[flora[0]]['name'], location.alias)
            else:
                material_results = "{0} are growing all over the {1}.".format(Flora.plants[flora[0]]['name'], location.alias)

            results.append(material_results)
        else:
            material_results = []
            for plant in flora:
                index = flora.index(plant)
                if index == 0:
                    material_results.append(Flora.plants[plant]['name'])
                elif index == len(flora) -1:
                    material_results.append(" and {0}".format(Flora.plants[plant]['name']))
                else:
                    material_results.append(", {0}".format(Flora.plants[plant]['name']))
            material_results = "".join(material_results)
            material_results = "{0} are growing all over the {1}.".format(material_results, location.alias)
            results.append(material_results)


    results = "".join(results)
    return results

def return_surrounded(location):
    results = []
    surrounding_objects = location.surrounded
    if surrounding_objects:
        if len(surrounding_objects) == 1:
            material_results = "The {1} is surrounded by {2}{0}.".format(Surrounded.objects[surrounding_objects[0]]['name'], location.alias, Surrounded.objects[surrounding_objects[0]]['preposition'])
            results.append(material_results)
        else:
            material_results = []
            for surrounding_object in surrounding_objects:
                index = surrounding_objects.index(surrounding_object)
                if index == 0:
                    material_results.append("{1}{0}".format(Surrounded.objects[surrounding_object]['name'], Surrounded.objects[surrounding_object]['preposition']))
                elif index == len(surrounding_objects) -1:
                    material_results.append(" and {1}{0}".format(Surrounded.objects[surrounding_object]['name'], Surrounded.objects[surrounding_object]['preposition']))
                else:
                    material_results.append(", {1}{0}".format(Surrounded.objects[surrounding_object]['name'], Surrounded.objects[surrounding_object]['preposition']))
            material_results = "".join(material_results)
            material_results = "The {1} is surrounded by {0}.".format(material_results, location.alias)
            results.append(material_results)


    results = "".join(results)
    return results


def return_scattered_objects(location):
    results = []
    scattered_objects = location.scattered_objects


    if scattered_objects:
        if len(scattered_objects) == 1:
            material_results = "{0} can be found all over the place.".format(ScatteredObjects.objects[scattered_objects[0]]['name'])

            results.append(material_results)
        else:
            material_results = []
            for scattered_object in scattered_objects:
                index = scattered_objects.index(scattered_object)
                if index == 0:
                    material_results.append(ScatteredObjects.objects[scattered_object]['name'])
                elif index == len(scattered_objects) -1:
                    material_results.append(" and {0}".format(ScatteredObjects.objects[scattered_object]['name']))
                else:
                    material_results.append(", {0}".format(ScatteredObjects.objects[scattered_object]['name']))
            material_results = "".join(material_results)
            material_results = "{0} can be found all over the place.".format(material_results)
            results.append(material_results)


    results = "".join(results)
    return results


def return_environment(location):
    results = []
    wind = location.environmental_effects.get("wind")
    sounds = location.environmental_effects.get("sounds")
    smells = location.environmental_effects.get("smells")

    if wind:
            wind_results = "There is a {0} Wind blowing here.".format(EnvironmentalEffects.wind[wind]['name'])
            results.append(wind_results)
    if smells:
        if len(smells) == 1:
            material_results = "There is a {0} Smell in the air.".format(EnvironmentalEffects.smells[smells[0]]['name'])
            results.append(material_results)
        else:
            material_results = []
            for smell in smells:
                index = smells.index(smell)

                if index == 0:
                    material_results.append(EnvironmentalEffects.smells[smell]['name'])
                elif index == len(smells) -1:
                    material_results.append(" and {0}".format(EnvironmentalEffects.smells[smell]['name']))
                else:
                    material_results.append(", {0}".format(EnvironmentalEffects.smells[smell]['name']))
            material_results = "".join(material_results)
            material_results = "There is a {0} Smell in th air.".format(material_results)
            results.append(material_results)
    if sounds:
        if len(sounds) == 1:
            sound_results = "I can hear the {0} of {1}.".format(EnvironmentalEffects.sounds[sounds[0]]['verb'], EnvironmentalEffects.sounds[sounds[0]]['name'])
            results.append(sound_results)
        else:
            sound_results = []
            for sound in sounds:
                index = sounds.index(sound)
                if index == 0:
                    sound_results.append("I can hear the {0} of {1}".format(EnvironmentalEffects.sounds[sound]['verb'], EnvironmentalEffects.sounds[sound]['name']))
                elif index == len(sounds) -1:
                    sound_results.append(" and the {0} of {1}".format(EnvironmentalEffects.sounds[sound]['verb'], EnvironmentalEffects.sounds[sound]['name']))
                else:
                    sound_results.append(", the {0} of {1}".format(EnvironmentalEffects.sounds[sound]['verb'], EnvironmentalEffects.sounds[sound]['name']))
            sound_results = "".join(sound_results)
            sound_results = "{0}.".format(sound_results)
            results.append(sound_results)

    results = " ".join(results)
    return results

def return_topography_objects(location):
    results = []
    topography = location.topography

    if topography:
        if len(topography) == 1:
            if not TopographyObjects.objects[topography[0]]['plural']:
                material_results = "The {1} features {2}{0}.".format(TopographyObjects.objects[topography[0]]['name'], location.alias, TopographyObjects.objects[topography[0]]['preposition'])
            else:
                material_results = "The {1} features {0}.".format(TopographyObjects.objects[topography[0]]['name'], location.alias)

            results.append(material_results)
        else:
            material_results = []
            for topography_object in topography:
                index = topography.index(topography_object)
                if index == 0:
                    material_results.append("{1}{0}".format(TopographyObjects.objects[topography_object]['name'], TopographyObjects.objects[topography_object]['preposition']))
                elif index == len(topography) - 1:
                    material_results.append(" and {1}{0}".format(TopographyObjects.objects[topography_object]['name'], TopographyObjects.objects[topography_object]['preposition']))
                else:
                    material_results.append(", {1}{0}".format(TopographyObjects.objects[topography_object]['name'], TopographyObjects.objects[topography_object]['preposition']))
            material_results = "".join(material_results)
            material_results = "The {1} features {0}.".format(material_results, location.alias)
            results.append(material_results)

    results = "".join(results)
    return results



def return_situated(location):
    results = []
    situation = location.situated
    if situation:
        material_results = "It is located {0}.".format(SituatedObjects.objects[situation[0]]['name'])
        results.append(material_results)



    results = "".join(results)
    return results



def return_flavor_text(location):
    results = []
    flavor_text = location.flavor_text
    if flavor_text:
        material_results = "{0}".format(flavor_text)
        results.append(material_results)

    results = "".join(results)
    return results


def return_access(location):
    results = []
    situation = location.access
    if situation:
        if not AccessMethods.methods[situation[0]]['plural']:
            material_results = "It can be accessed via {0}{1}.".format(AccessMethods.methods[situation[0]]['preposition'], AccessMethods.methods[situation[0]]['name'])
        else:
            material_results = "It can be accessed via {0}.".format(AccessMethods.methods[situation[0]]['name'])

        results.append(material_results)



    results = "".join(results)
    return results




def return_window_lighting(windows):
    results = []



    if windows:
        if len(windows) == 1:
            material_results = "{0}".format(Windows.windows[windows[0]]['name'])
            results.append(material_results)
        else:
            material_results = []
            for window in windows:
                index = windows.index(window)
                if index == 0:
                    material_results.append(Windows.windows[window]['name'])
                elif index == len(windows) -1:
                    material_results.append(" and {0}".format(Windows.windows[window]['name']))
                else:
                    material_results.append(", {0}".format(Windows.windows[window]['name']))
            material_results = "".join(material_results)
            material_results = "{0}".format(material_results)
            results.append(material_results)


    results = "".join(results)
    return results