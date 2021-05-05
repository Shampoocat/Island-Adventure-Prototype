import random
from random import randint

def pick_object(template, location):
    template_buffer = return_object_template(template)
    object_options = template_buffer.get("object_options")
    forced = template_buffer.get("forced")
    singular = template_buffer.get("singular")
    existing_objects = []
    for existing_object in location.objects:
        existing_objects.append(existing_object.identifier)

    if singular:
        for singular_object in singular:
            if singular_object in existing_objects:
                object_options.remove(singular_object)

    needed_objects = []
    if forced:
        for forced_object in forced:
            if forced_object not in existing_objects:
                needed_objects.append(forced_object)
    if needed_objects:
        object_options = needed_objects

    object_choice = random.choice(object_options)
    object_pick = return_object_dict(object_choice)
    return object_pick



#This stores the data of the templates used to generate objects. Number is the number of objects to generate, options are the possible objects, forced makes sure that at least one of each
#object in there is generated and singular makes sure only one of this object is generated.
def return_object_template(key):
    templates = {
        "office": {"number": randint(3, 6), "object_options": ["simple_chair", "office_chair", "office_desk_wood", "plant_pot"], "forced": ["office_desk_wood"], "singular": ["office_desk_wood", "office_chair"]},
        "village": {"number": randint(3, 6), "object_options": ["cart", "box_wood", "rack_drying"]},
        "generic_hallways": {"number": randint(3, 6), "object_options": ["box_wood", "box_cardboard", "simple_chair", "locker", "table_wood"]},
        "outdoor_industrial": {"number": randint(3, 6), "object_options": ["abandoned_car", "abandoned_construction_equipment", "shipping_container", "barrel", "waste_container"], "singular": ["abandoned_car", "abandoned_construction_equipment"]},
        "observatory": {"number": randint(3, 6), "object_options": ["office_chair", "office_desk_wood", "computer"], "forced": ["large_telescope"],
                        "singular": ["large_telescope", "office_desk_wood", "office_chair"]},
        "storage_room": {"number": randint(3, 6), "object_options": ["box_wood", "box_cardboard", "simple_chair", "locker", "shelve"]},
        "utility_room": {"number": randint(3, 6), "object_options": ["box_wood", "box_cardboard", "simple_chair", "locker", "generator", "switch_box", "pipe", "shelve"], "singular": ["pipe"]},
        "shrine": {"number": randint(0, 2), "object_options": ["small_statue", "offering_box"], "singular": ["small_statue", "offering_box"], "forced": ["small_statue", "offering_box"]},
        "wreck_bridge": {"number": randint(3, 6), "object_options": ["box_wood", "box_cardboard", "simple_chair", "locker", "ship_controls"], "singular": ["ship_controls"], "forced": ["ship_controls"]},
        "wreck_cargo": {"number": randint(3, 6), "object_options": ["box_wood", "box_cardboard", "shipping_container", "barrel"]},
        "wreck_engine": {"number": randint(3, 6), "object_options": ["box_wood", "box_cardboard", "barrel", "locker", "ship_engine"],
                         "singular": ["ship_engine"], "forced": ["ship_engine"]},
        "wreck_quarters": {"number": randint(6, 10), "object_options": ["box_wood", "box_cardboard", "simple_chair", "locker", "kitchen_boat", "ship_cabin"], "singular": ["kitchen_boat"]},
        "boathouse": {"number": randint(3, 6), "object_options": ["box_wood", "box_cardboard", "simple_chair", "locker", "shelve", "small_boat_wreck"], "singular": ["small_boat_wreck"]},
        "wreck_cockpit": {"number": 3, "object_options": ["plane_controls", "plane_seat"], "singular": ["plane_controls"], "forced": ["plane_controls"]},
        "wreck_cabin": {"number": randint(3, 6), "object_options": ["box_wood", "box_cardboard", "plane_seat"]},
        "wreck_wing": {"number": 1, "object_options": ["plane_engine"]},
        "laboratory": {"number": randint(3, 6), "object_options": ["simple_chair", "office_chair", "office_desk_wood", "lab_equipment"], "forced": ["office_desk_wood", "lab_equipment"], "singular": ["office_desk_wood", "office_chair"]},
        "hut": {"number": randint(3, 6), "object_options": ["ornate_box", "simple_box", "bench", "cooking_spot"], "singular": ["cooking_spot"]},
        "hut_large": {"number": randint(6, 10), "object_options": ["ornate_box", "simple_box", "bench", "cooking_spot"], "singular": ["cooking_spot"]},

    }
    return templates.get(key)


#The data of objects, works pretty much the same as the one for locations. Apart from the obvious ones like name etc. there are tags associated with each object and the stack_on_creation flag that
#allows for objects to be stacked so they display as "five chairs" instead of "a chair, a chair, a char ...."
def return_object_dict(key):
    object_dict = {
        "simple_chair": {"name": "chair", "plural": "chairs", "article": "a", "identifier": "simple_chair", "tags": ["plastic", "cracked"], "stack_on_creation": True},
        "office_chair": {"name": "office chair", "plural": "office chairs", "article": "an", "identifier": "office_chair", "tags": ["plastic", "metal", "cushioning_artificial_leather", "moldy", "damaged"], "stack_on_creation": True},
        "office_desk_wood": {"name": "desk", "plural": "desks", "article": "a", "identifier": "office_desk_wood", "tags": ["wood", "moldy"], "stack_on_creation": True},
        "plant_pot": {"name": "plant pot", "plural": "plant pots", "article": "a", "identifier": "plant_pot", "tags": ["wood", "moldy"], "stack_on_creation": True},
        "cart": {"name": "cart", "plural": "carts", "article": "a", "identifier": "cart", "tags": ["wood", "damaged"], "stack_on_creation": True},
        "box_wood": {"name": "box", "plural": "boxes", "article": "a", "identifier": "box_wood", "tags": ["wood", "rotten"], "stack_on_creation": True},
        "box_cardboard": {"name": "box", "plural": "boxes", "article": "a", "identifier": "box_cardboard", "tags": ["cardboard", "rotten"], "stack_on_creation": True},
        "rack_drying": {"name": "rack", "plural": "racks", "article": "a", "identifier": "rack_drying", "tags": ["wood"], "stack_on_creation": True},
        "locker": {"name": "locker", "plural": "lockers", "article": "a", "identifier": "locker", "tags": ["metal"], "stack_on_creation": True},
        "table_wood": {"name": "table", "plural": "tables", "article": "a", "identifier": "table_wood", "tags": ["wood", "damaged"], "stack_on_creation": True},
        "abandoned_car": {"name": "abandoned car", "plural": "abandoned cars", "article": "an", "identifier": "abandoned_car", "tags": ["ruined"], "stack_on_creation": False},
        "abandoned_construction_equipment": {"name": "piece of abandoned construction equipment", "plural": "pieces of abandoned construction equipment", "article": "a", "identifier": "abandoned_construction_equipment",
                                             "tags": ["ruined"], "stack_on_creation": False},
        "shipping_container": {"name": "shipping container", "plural": "shipping containers", "article": "a", "identifier": "shipping_container", "tags": ["rust", "metal"], "stack_on_creation": True},
        "barrel": {"name": "barrel", "plural": "barrels", "article": "a", "identifier": "barrel", "tags": ["metal"], "stack_on_creation": True},
        "waste_container": {"name": "waste container", "plural": "waste containers", "article": "a", "identifier": "waste_container", "tags": ["plastic"], "stack_on_creation": True},
        "computer": {"name": "old computer", "plural": "old computers", "article": "a", "identifier": "computer", "tags": ["ruined"], "stack_on_creation": True},
        "large_telescope": {"name": "telescope", "plural": "telescopes", "article": "a", "identifier": "telescope", "tags": ["ruined", "massive"], "stack_on_creation": False},
        "generator": {"name": "small generator", "plural": "small generators", "article": "a", "identifier": "generator", "tags": ["rust", "metal", "damaged"], "stack_on_creation": True},
        "switch_box": {"name": "switch box", "plural": "switch boxes", "article": "a", "identifier": "switch_box", "tags": ["plastic", "metal", "concrete"], "stack_on_creation": True},
        "pipe": {"name": "pipework", "plural": "pipeworks", "article": "a", "identifier": "pipe", "tags": ["metal", "rust"], "stack_on_creation": False},
        "shelve": {"name": "shelve", "plural": "shelves", "article": "a", "identifier": "telescope", "tags": ["metal"], "stack_on_creation": True},
        "small_statue": {"name": "small statue", "plural": "small statues", "article": "a", "identifier": "small_statue", "tags": ["wood", "rotten"], "stack_on_creation": True},
        "offering_box": {"name": "offering box", "plural": "offering boxes", "article": "a", "identifier": "offering_box", "tags": ["wood", "rotten"], "stack_on_creation": False},
        "ship_controls": {"name": "nautical control panel", "plural": "nautical control panels", "article": "a", "identifier": "ship_controls", "tags": ["radar_equipment", "monitors", "helm", "ruined"], "stack_on_creation": False},
        "ship_engine": {"name": "engine", "plural": "engines", "article": "an", "identifier": "ship_engine", "tags": ["massive", "rust", "metal"], "stack_on_creation": False},
        "ship_cabin": {"name": "cabin", "plural": "cabins", "article": "a", "identifier": "ship_cabin", "tags": ["wood", "rotten", "old_mattress", "old_curtains"], "stack_on_creation": True},
        "kitchen_boat": {"name": "galley", "plural": "galley", "article": "a", "identifier": "kitchen_boat", "tags": ["ruined"], "stack_on_creation": False},
        "small_boat_wreck": {"name": "wrecked boat", "plural": "wrecked boat", "article": "a", "identifier": "small_boat_wreck", "tags": ["wood", "rotten"], "stack_on_creation": True},
        "plane_seat": {"name": "plane seat", "plural": "plane seats", "article": "a", "identifier": "plane_seat", "tags": ["cushioning_fabric", "rotten", "plastic"], "stack_on_creation": True},
        "plane_controls": {"name": "airplane control panel", "plural": "airplane control panels", "article": "an", "identifier": "plane_controls", "tags": ["monitors", "radar_equipment", "plane_controls"], "stack_on_creation": False},
        "plane_engine": {"name": "engine", "plural": "engines", "article": "an", "identifier": "plane_engine", "tags": ["ruined", "massive"], "stack_on_creation": False},
        "lab_equipment": {"name": "set of lab equipment", "plural": "sets of lab equipment", "article": "a", "identifier": "lab_equipment", "tags": ["glass", "metal", "plastic", "damaged"], "stack_on_creation": True},
        "simple_box": {"name": "simple box", "plural": "simple boxes", "article": "a", "identifier": "simple_box", "tags": ["wood"], "stack_on_creation": True},
        "ornate_box": {"name": "ornate box", "plural": "ornate boxes", "article": "an", "identifier": "ornate_box", "tags": ["wood"], "stack_on_creation": True},
        "bench": {"name": "bench", "plural": "benches", "article": "a", "identifier": "bench", "tags": ["wood"], "stack_on_creation": True},
        "cooking_spot": {"name": "cooking spot", "plural": "cooking spots", "article": "a", "identifier": "cooking_spot", "tags": ["stones"], "stack_on_creation": True},

    }

    return object_dict.get(key)
