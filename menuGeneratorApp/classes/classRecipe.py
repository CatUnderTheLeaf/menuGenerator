""" 
a class that represent a single recipe
 """

class Recipe:
    """ 
    id: recipe id in db 
    title: name of the Recipe
    img: path to the image
    ingridients: list of products
    food_class: list of food classes, 'fat', 'fruit', 'cereal', etc
    nutrients: list of nutrients, 'carb', 'protein', etc
    prepareTime: short/middle/long
    description: recipe instructions
    tags: breakfast/dinner, dough food, etc
    repeat: True/False, if a dish can be prepared for more than one day
     """
    def __init__(self, id='', title="", img="menuGeneratorApp\img\\no_image.png", ingridients=[], food_class=[], nutrients=[], prepareTime="short", text="", tags=[], repeat=False):        
        self.id = id
        self.title = title
        self.img = img
        self.ingridients = ingridients
        self.food_class = food_class
        self.nutrients = nutrients
        self.prepareTime = prepareTime
        self.description = text
        self.tags = tags
        self.repeat = repeat
        
    def __repr__(self):
    #    return (f'{self.title!r}  -  {self.tags!r} - {self.ingridients!r} - {self.food_class!r} - {self.nutrients!r}')
       return (f'{self.title!r}')

    def __str__(self):
        # return f'{self.title}  -  {self.tags} - {self.prepareTime} - {self.repeat}'
        return self.title
        