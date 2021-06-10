import random
import pickle

from classRules import Rules
""" 
a class that represent a list of recipes,
has a bunch of useful filtering and randomizing functions

list - list of Recipe objects
mpd - meals per day, default value is 3
 """

class Menu:
    def __init__(self):  
        with open('recipe.list', 'rb') as file:
            self.recipeList = pickle.load(file)            
            print("load recipes")
        with open('class_products.list', 'rb') as file:
            self.class_products = pickle.load(file)   
            print("load class_products dictionary")
            self.products_class = {v: k for k, values in self.class_products.items() for v in values}            
        
        
        self.rules = Rules()
        self.mpd = ['Breakfast', 'Lunch', 'Dinner']
        
    def __repr__(self):
       return repr(self.recipeList)

    def __str__(self):
       return str(self.recipeList)
    
    """ 
    identify to which food class 
    belong ingridients

    :param recipe: a single recipe
    :return: list of unique food classes    
     """
    def identifyFoodClass(self, recipe):            
        foodClass = []
        for ingridient in recipe.ingridients:
            foodClass.append(self.products_class[ingridient])
        foodClass = list(set(foodClass))
               
        return foodClass

    """ 
    identify to which nutrient type 
    belongs recipe

    :param recipe: a single recipe
    :return: list of unique nutrient types (carb, protein, fat or free)    
     """
    def identifyNutrients(self, recipe):            
        nutrients = self.rules.identifyNutrient(recipe.food_class)
               
        return nutrients

    def generateDailyMenu(self, n=1):
        print("!!!-----------------generating menu----------------!!!")
        for meal in self.mpd:
            # Check if recipes should be filtered 
            # by category for this type of meal
            cat=self.rules.filterByCat(meal)            
            recipe = self.choicesN(n, cat)
            print(meal)
            print(recipe)

    # shuffle recipe list
    def shuffle(self):
        random.shuffle(self.recipeList)
        return self.recipeList

    # when you can't afford to have duplicates while sampling your data.
    def sampleN(self, n=1, cat=None):
        sublist = self.recipeList
        if cat is not None:
            print("filter with category")
            sublist = self.filterCategory(cat)
        newList = random.sample(sublist, n)
        return newList

    # when you can afford to have duplicates in your sampling
    def choicesN(self, n=1, cat=None):
        sublist = self.recipeList
        if cat is not None:
            print("filter with category")
            sublist = self.filterCategory(cat)
        newList = random.choices(sublist, k=n)
        return newList

    def filterCategory(self, cat):
        sublist = [x for x in self.recipeList if x.category==cat]
        return sublist

        
