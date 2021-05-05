from textgenerator import *
from objectdict import *
from object_tag_dict import *

#Function to add objects to a location. Looking at it now, it probably could be part of the location object. But then again that thing is already bloated as hell.....

def add_objects(object_template, location):
    #Sanity check to make sure there is a template.
    if object_template:
        #Looks up how many objects should be crated from the template
        number_of_objects = return_object_template(object_template).get("number")
        #Generates new objects while the counter is > 0
        while number_of_objects > 0:
            #Resets the generation_done var
            generation_done = False
            #Picks an object to generate with the pic_object function
            object_choice = pick_object(object_template, location)

            #If the object has the stack_on_creation flag set, it checks if the same object already exists.
            #If it does it will not create a new object but instead add tot he stack of the existing one.
            if object_choice.get("stack_on_creation") and location.objects:
                for existing_object in location.objects:
                    if existing_object.identifier == object_choice.get("identifier"):
                        existing_object.stack_size += 1
                        generation_done = True

            #If a new object must be created it does this now.
            if not generation_done:
                generated_object = Object(object_choice.get("name"), object_choice.get("plural"),
                                        object_choice.get("article"), object_choice.get("identifier"), object_choice.get("tags"))
                generated_object.owner = location
                location.objects.append(generated_object)

            #Very important ;)
            number_of_objects -= 1
    else:
        pass


#The class holding the object data
class Object:
    def __init__(self, base_name, plural, base_article, identifier, tags):
        self.base_name = base_name
        self.plural = plural
        self.base_article = base_article
        self.identifier = identifier
        self.stack_size = 1
        self.tags = tags
        self.resolve_tags()


    @property
    def article(self):
        if self.stack_size == 1:
            return self.base_article
        else:
            return return_numbers(self.stack_size)


    @property
    def pronoun(self):
        if self.stack_size == 1:
            return "it"
        else:
            return "they"

    @property
    def object_feature(self):
        if self.stack_size == 1:
            return "features"
        else:
            return "feature"

    @property
    def object_being(self):
        if self.stack_size == 1:
            return "is"
        else:
            return "are"

    @property
    def object_possession(self):
        if self.stack_size == 1:
            return "has"
        else:
            return "have"

    #Adds new tags if one of the objects tags wants to generate new tags. Same as with locations.
    def resolve_tags(self):

        for tag in self.tags:

            tag = return_object_tag(tag, self)
            additional_tags = tag.get("generate_tags")
            if additional_tags:
                for additional_tag in additional_tags:
                    if additional_tag not in self.tags:
                        self.tags.append(additional_tag)

    @property
    def description(self):
        return generate_object_description(self)

    @property
    def name(self):

        if self.stack_size == 1:
            return "{0} {1}".format(self.base_article, self.base_name)
        else:
            return "{0} {1}".format(return_numbers(self.stack_size), self.plural)

    @property
    def simple_name(self):

        if self.stack_size == 1:
            return "{0}".format(self.base_name)
        else:
            return "{0}".format(self.plural)






