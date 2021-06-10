""" 
a class that represent a single recipe

title - name of the Recipe
ingridients - list of products
prepareTime - short/middle/long
text - recipe instructions
category - breakfast/dinner
 """

class Recipe:

    def __init__(self, title="", ingridients=[], food_class=[], nutrients=[], prepareTime="short", text="", category="breakfast"):        
        self.title = title
        # TODO later implement, now it is not so important
        # self.img = img
        self.ingridients = ingridients
        self.food_class = food_class
        self.nutrients = nutrients
        self.prepareTime = prepareTime
        self.description = text
        self.category = category
        
    def __repr__(self):
       return (f'{self.title!r}  -  {self.category!r} - {self.ingridients!r}')

    def __str__(self):
        return f'{self.title}  -  {self.category}'
        