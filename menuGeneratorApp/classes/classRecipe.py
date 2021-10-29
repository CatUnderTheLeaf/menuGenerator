""" 
a class that represent a single recipe
 """

class Recipe:
    """ 
    title: name of the Recipe
    ingridients: list of products
    food_class: list of food classes, 'fat', 'fruit', 'cereal', etc
    nutrients: list of nutrients, 'carb', 'protein', etc
    prepareTime: short/middle/long
    description: recipe instructions
    tags: breakfast/dinner, dough food, etc
    oneTime: True/False, if a dish can be prepared for more than one day
     """
    def __init__(self, id=0, title="", ingridients=[], food_class=[], nutrients=[], prepareTime="short", text="", tags=[], oneTime=True):        
        self.id = id
        self.title = title
        # TODO later implement, now it is not so important
        # self.img = img
        self.ingridients = ingridients
        self.food_class = food_class
        self.nutrients = nutrients
        self.prepareTime = prepareTime
        self.description = text
        self.tags = tags
        self.oneTime = oneTime
        
    def __repr__(self):
    #    return (f'{self.title!r}  -  {self.tags!r} - {self.ingridients!r} - {self.food_class!r} - {self.nutrients!r}')
       return (f'{self.title!r}')

    def __str__(self):
        # return f'{self.title}  -  {self.tags} - {self.prepareTime} - {self.oneTime}'
        return self.title
        