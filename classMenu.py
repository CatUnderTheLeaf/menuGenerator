import random
import pickle
from pathlib import Path

from classRules import Rules
from classRecipe import Recipe
""" 
a class that represent a list of recipes,
has a bunch of useful filtering and randomizing functions
 """

DB_RECIPE = 'db/recipe.list'
DB_PRODUCTS = 'db/class_products.list'
DB_RULES = 'db/rules'
PRODUCT_DIR = 'products'
HELPER_ITEM = 'recipe_helpers/menuItems'
HELPER_TAGS = 'recipe_helpers/tags'
HELPER_INGRIDIENTS = 'recipe_helpers/ingridients'

class Menu:
    """ 
    recipeList: list of all recipes
    class_products: dictionary of food_class:[products]
    products_class: dictionary of product:food_class
    rules: object type Rules with all rules for generating menu
    mpd: meals per day
    
    """    
    def __init__(self):                 
        self.rules = Rules(DB_RULES)
        self.mpd = ['Breakfast', 'Lunch', 'Dinner']

        # if there are changes in product files reload them
        # self.reloadProducts()

        with open(DB_PRODUCTS, 'rb') as file:
            self.class_products = pickle.load(file)   
            print("load class_products dictionary")
            self.products_class = {}
            for k, values in self.class_products.items():
                for v in values:
                    if v in self.products_class:
                        self.products_class[v].append(k)
                    else:
                        self.products_class[v] = [k]
        # print(self.products_class)
        # if there are changes in recipe files reload them
        # self.reloadRecipes()        

        with open(DB_RECIPE, 'rb') as file:
            self.recipeList = pickle.load(file)            
            print("load recipes")
                
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
        foodClass = set()
        for ingridient in recipe.ingridients:
            foodClass.update(self.products_class[ingridient])
        foodClass = list(foodClass)
               
        return foodClass

    """ 
    identify to which nutrient type 
    belongs recipe

    :param recipe: a single recipe
    :return: list of unique nutrient types (carb, protein, fat or free)    
     """
    def identifyNutrients(self, recipe):            
        nutrients = self.rules.identifyNutrient(recipe.food_class, recipe.tags)
               
        return nutrients

    """ 
    generate Menu for n days

    :param n: number of days
    
     """
    def generateDailyMenu(self, n=1):
        print("!!!-----------------generating menu----------------!!!")
        for meal in self.mpd:
            # Check if recipes should be filtered 
            # by tags for this type of meal
            tag=self.rules.filterByTag(meal)   
            nutr = self.rules.filterByNutrient(meal)         
            recipe = self.choicesN(n, tag, nutr)
            print(meal)
            print(nutr)
            print(recipe)
        return

    # shuffle recipe list
    def shuffle(self):
        random.shuffle(self.recipeList)
        return self.recipeList

    """ 
    choose n recipes without duplicates

    :param n: number of recipes, cannot be bigger then amount of recipes
    :param tag: tags of recipe ('breakfast', etc)
    :return: a subset of recipes
    """
    def sampleN(self, n=1, tag=None):
        sublist = self.recipeList
        if tag is not None:
            print("filter with tags")
            sublist = self.filter(tag)
        newList = random.sample(sublist, n)
        return newList

    """ 
    choose n recipes with duplicates

    :param n: number of recipes, can be bigger then amount of recipes
    :param tag: tags of recipe ('breakfast', etc)
    :param nutr: list of 'carb', 'protein' or 'fat'
    :return: n recipes
    """
    def choicesN(self, n=1, tag=None, nutr=None):
        sublist = self.recipeList
        if tag is not None or nutr is not None:
            print("filter with tags or nutrients")
            sublist = self.filter(tag, nutr)
        newList = random.choices(sublist, k=n)
        return newList

    """ 
    filter recipes by tags or nutrients

    :param tag: tags of recipe ('breakfast', etc)
    :param nutr: list of 'carb', 'protein' or 'fat'
    :return: a subset of recipes
    """
    def filter(self, tag=None, nutr=None):
        sublist = []
        for recipe in self.recipeList:
            has_tags = (tag in recipe.tags) if (tag is not None) else True
            is_subset = (set(recipe.nutrients)<=set(nutr)) if (nutr is not None) else True
            if has_tags and is_subset:
                sublist.append(recipe)
        # sublist = [x for x in self.recipeList if (tag is not None and x.tags==tag)]
        return sublist

    """ 
    Reload product list if there are changes in files
     """
    def reloadProducts(self):
        products = {}
        for p in Path(PRODUCT_DIR).iterdir():
            with p.open() as f:
                menuList = [line.rsplit(' - ')[0].rstrip() for line in f]
                products[p.name] = menuList
        print(products)
        # dump products dict in a file
        with open(DB_PRODUCTS, 'wb') as file:
            pickle.dump(products, file)

        return

    """ 
    Reload recipes from helper files
    in future will not be needed
     """
    def reloadRecipes(self):
        with open(HELPER_ITEM) as f:
            menuList = [line.rstrip() for line in f]
        with open(HELPER_TAGS) as f:
            tags = [line.rstrip().split(', ') for line in f]
        with open(HELPER_INGRIDIENTS) as f:
            ingridients = [line.rstrip().split(', ') for line in f]
        
        # add recipe objects to a list
        menu = []
        for (item, tag, ingr) in zip(menuList, tags, ingridients):
            new_recipe = Recipe(title=item, tags=tag, ingridients=ingr)
            new_recipe.food_class = self.identifyFoodClass(new_recipe)
            new_recipe.nutrients = self.identifyNutrients(new_recipe)
            menu.append(new_recipe)
        print(menu)
        # dump list in a file
        with open(DB_RECIPE, 'wb') as file:
            pickle.dump(menu, file)
        
        return