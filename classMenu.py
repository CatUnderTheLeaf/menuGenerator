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
        with open('products.list', 'rb') as file:
            self.products = pickle.load(file)   
            print("load products")
        self.rules = Rules()
        self.mpd = ['Breakfast', 'Lunch', 'Dinner']

    def __repr__(self):
       return repr(self.recipeList)

    def __str__(self):
       return str(self.recipeList)
    
    def generateDailyMenu(self):
        print("!!!-----------------generating menu for one day----------------!!!")
        for meal in self.mpd:
            # Check if recipes should be filtered 
            # by category for this type of meal
            cat=self.rules.filterByCat(meal)            
            recipe = self.sampleN(1, cat)
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

        
