import random
import pickle

from classRules import Rules
""" 
a class that represent a list of recipes,
has a bunch of useful filtering and randomizing functions
 """

class Menu:
    """ 
    recipeList: list of all recipes
    class_products: dictionary of food_class:[products]
    products_class: dictionary of product:food_class
    rules: object type Rules with all rules for generating menu
    mpd: meals per day
    
    """    
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

    """ 
    generate Menu for n days

    :param n: number of days
    
     """
    def generateDailyMenu(self, n=1):
        print("!!!-----------------generating menu----------------!!!")
        for meal in self.mpd:
            # Check if recipes should be filtered 
            # by category for this type of meal
            cat=self.rules.filterByCat(meal)   
            nutr = self.rules.filterByNutrient(meal)         
            recipe = self.choicesN(n, cat, nutr)
            print(meal)
            print(nutr)
            print(recipe)

    # shuffle recipe list
    def shuffle(self):
        random.shuffle(self.recipeList)
        return self.recipeList

    """ 
    choose n recipes without duplicates

    :param n: number of recipes, cannot be bigger then amount of recipes
    :param cat: category of recipe ('breakfast', etc)
    :return: a subset of recipes
    """
    def sampleN(self, n=1, cat=None):
        sublist = self.recipeList
        if cat is not None:
            print("filter with category")
            sublist = self.filterCategory(cat)
        newList = random.sample(sublist, n)
        return newList

    """ 
    choose n recipes with duplicates

    :param n: number of recipes, can be bigger then amount of recipes
    :param cat: category of recipe ('breakfast', etc)
    :param nutr: list of 'carb', 'protein' or 'fat'
    :return: n recipes
    """
    def choicesN(self, n=1, cat=None, nutr=None):
        sublist = self.recipeList
        if cat is not None or nutr is not None:
            print("filter with category or nutrints")
            sublist = self.filterCategory(cat, nutr)
        newList = random.choices(sublist, k=n)
        return newList

    """ 
    filter recipes by category

    :param cat: category of recipe ('breakfast', etc)
    :param nutr: list of 'carb', 'protein' or 'fat'
    :return: a subset of recipes
    """
    def filterCategory(self, cat=None, nutr=None):
        sublist = []
        for recipe in self.recipeList:
            has_category = (recipe.category==cat) if (cat is not None) else True
            is_subset = (set(recipe.nutrients)<=set(nutr)) if (nutr is not None) else True
            if has_category and is_subset:
                sublist.append(recipe)
        # sublist = [x for x in self.recipeList if (cat is not None and x.category==cat)]
        return sublist

        
