from kivy.utils import platform
import os
""" 
a class that represent a single recipe
 """

class Recipe:
    """ 
    id: recipe id in db 
    title: name of the Recipe
    img: path to the image
    ingredients: list of products
    food_class: list of food classes, 'fat', 'fruit', 'cereal', etc
    nutrients: list of nutrients, 'carb', 'protein', etc
    prepareTime: short/middle/long
    description: recipe instructions
    tags: breakfast/dinner, dough food, etc
    repeat: True/False, if a dish can be prepared for more than one day
     """
    def __init__(self, id='', title="", img="no_image.png", ingredients=[], food_class=[], nutrients=[], prepareTime="short", text="", tags=[], repeat=False):        
        self.id = id
        self.title = title.capitalize()
        self.img = img
        if not os.path.dirname(img):
            if platform == "android":
                from android.storage import app_storage_path
                app_path = app_storage_path()
                self.img = os.path.join(app_path, 'app', 'img', img)
            else:
                self.img = os.path.join(os.path.dirname(os.path.dirname(__file__)), "img", img)
        
        self.ingredients = ingredients
        self.food_class = food_class
        self.nutrients = nutrients
        self.prepareTime = prepareTime
        self.description = text
        self.tags = tags
        self.repeat = repeat
        
    # def __repr__(self):
    #    return (f'{self.title!r}  -  {self.tags!r} - {self.ingredients!r} - {self.food_class!r} - {self.nutrients!r}')
    #    return (f'{self.title!r}')

    def __str__(self):
        # return f'{self.title}  -  {self.tags} - {self.prepareTime} - {self.repeat}'
        return self.title
        