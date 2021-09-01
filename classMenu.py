import random
import pickle
from pathlib import Path
from datetime import date, timedelta

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
HELPER_TIME = 'recipe_helpers/prepareTime'

class Menu:
    """ 
    recipeList: list of all recipes
    class_products: dictionary of food_class:[products]
    products_class: dictionary of product:food_class
    rules: object type Rules with all rules for generating menu
    mpd: meals per day
    menu: dict of recipes per meals
    subsets: dict of recipes grouped by prep time and meal
    n: number of days
    repeatDishes: if dishes can be eaten on more than one day
    
    """
    menu = {}
    subsets = {}
        
    def __init__(self):                 
        self.rules = Rules(DB_RULES)
        self.mpd = ['Breakfast', 'Lunch', 'Dinner']
        self.n = 1
        self.repeatDishes = True

        # if there are changes in product files reload them
        # self.reloadProducts()

        with open(DB_PRODUCTS, 'rb') as file:
            self.class_products = pickle.load(file)   
            print("load class_products dictionary")
            self.products_class = {}
            # make product dictionary for easy access
            for k, values in self.class_products.items():
                for v in values:
                    if v in self.products_class:
                        self.products_class[v].append(k)
                    else:
                        self.products_class[v] = [k]
        # if there are changes in recipe files reload them
        # self.reloadRecipes()        

        with open(DB_RECIPE, 'rb') as file:
            self.recipeList = pickle.load(file)            
            print("load recipes")

        # make subsets of recipes grouped by prep time and meal type
        times_list = [self.rules.day_time[key] for key in self.rules.day_time]
        times_groups = set(tuple(times) for times in times_list)
        for meal in self.mpd:
            self.subsets[meal] = {}
            for prep in times_groups:
                # Check if recipes should be filtered 
                # by tags for this type of meal
                tag, nutr = self.rules.filterByMeal(meal)
                if tag is not None or nutr is not None:
                    # print("filter with tags or nutrients")
                    sublist = self.filter(tag, nutr, prep)
                    self.subsets[meal][prep] = set(sublist)
        print(self.subsets)
                
    def __repr__(self):
       return repr(self.recipeList)

    def __str__(self):
        menu = []
        menu.append("!!!-----------------generated menu----------------!!!")
        for day in self.menu:
            menu.append("\n{}:".format(day))
            for meal in self.menu[day]:
                menu.append("{} - {}".format(meal, self.menu[day][meal]))
        return "\n".join(menu)
    
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

    :param sdate: start date
    :param edate: end date
    
     """
    def generateDailyMenu(self, sdate=date.today(), edate=date.today()):
        self.n = (edate - sdate).days + 1
        days = [sdate + timedelta(days=i) for i in range(self.n)]
        group_days = self.rules.filterByDay(days)
        menu = self.getMenuDraft(group_days)
        self.correctMenu(menu, days)
    
        return

    """ 
    generate a draft of menu
    without duplicates if possible
    should be edited later to apply "day" or "repeat" rules

    :param group_days: list of tuples (prepare times, number of days)
    :return: a draft menu
     """
    def getMenuDraft(self, group_days):
        menu = {}
        for meal in self.mpd:
            # Check if recipes should be filtered 
            # by tags for this type of meal
            tag, nutr = self.rules.filterByMeal(meal)
            for (prep, count) in group_days:
                recipes = self.choicesN(count, tag, nutr, prep)                
                if meal in menu:
                    menu[meal][0].extend(recipes)
                else:
                    menu[meal] = [recipes, tag, nutr]
        
        # print(menu)
        return menu
        

    """ 
    discard unused meals if there are such in Rules
    correct menu if option to repeat dishes is turned on

    :param draftMenu: generated draft of menu without duplicates, if possible
    :param days: list of days

     """
    def correctMenu(self, draftMenu, days):
        timeByDay = self.rules.getRulesByDay(days)
        days_meals = self.rules.filterDiscardedMeals(days)
        self.menu = {day.isoformat(): {meal:'' for meal in self.mpd} for day in days}
        
        # discard meals if there are rules
        for (day, meals) in days_meals:
            for meal in meals:
                self.menu[day][meal] = None
        if self.repeatDishes:
            for i, k in enumerate(self.menu.keys()):
                for meal in self.mpd:
                    # if meal for chosen day is still empty - fill it with the dish
                    if self.menu[k][meal] == '':
                        self.menu[k][meal] = draftMenu[meal][0][i]
                        # if the dish can be prepared for more than one time
                        # search for available next meal and fill it
                        if not draftMenu[meal][0][i].oneTime:
                            availableDay = self.findAvailableDay(draftMenu, timeByDay, draftMenu[meal][0][i], i)
                            if availableDay:
                                nextDay, nextMeal = availableDay
                                self.menu[nextDay][nextMeal] = draftMenu[meal][0][i]
        # if dishes are not repeated - just reorganize the draftmenu
        else:
            for i, k in enumerate(self.menu.keys()):
                for meal in self.mpd:
                    if self.menu[k][meal] is not None:
                        self.menu[k][meal] = draftMenu[meal][0][i]
        return

    """ 
    find next available slot in the menu for a dish
    which can be eaten more than one time

    :param draftMenu: generated draft of menu without duplicates, if possible
    :param timeByDay: list of prepareTimes
    :param recipe: a recipe of the dish
    :param i: index (day) of recipe in draftMenu
    :return: tuple (day, meal) if slot is available
    """
    def findAvailableDay(self, draftMenu, timeByDay, recipe, i):        
        days = list(self.menu.keys())
        for ind in range(i+1, len(days)):
            day = self.menu[days[ind]]
            for meal in day:
                if day[meal] == '':
                    check = self.checkRecipe(recipe, draftMenu[meal][1], draftMenu[meal][2], timeByDay[ind])
                    if check:
                        return (days[ind], meal)
        return

    # shuffle recipe list
    def shuffle(self):
        random.shuffle(self.recipeList)
        return self.recipeList

    """ 
    choose n recipes with or without duplicates

    :param n: number of recipes, can be bigger than amount of recipes
    :param tag: tags of recipe ('breakfast', etc)
    :param nutr: list of 'carb', 'protein' or 'fat'
    :param prep: list of preparation times
    :return: n recipes
    """
    def choicesN(self, n=1, tag=None, nutr=None, prep=None):
        sublist = self.recipeList
        if tag is not None or nutr is not None:
            # print("filter with tags or nutrients")
            sublist = self.filter(tag, nutr, prep)
        if len(sublist)<n:
            newList = random.choices(sublist, k=n)
        else:
            newList = random.sample(sublist, n)
        return newList

    """ 
    filter recipes by tags or nutrients

    :param tag: tags of recipe ('breakfast', etc)
    :param nutr: list of 'carb', 'protein' or 'fat'
    :param prep: list of preparation times
    :return: a subset of recipes
    """
    def filter(self, tag=None, nutr=None, prep=None):
        sublist = []
        for recipe in self.recipeList:
            if self.checkRecipe(recipe, tag, nutr, prep):
                sublist.append(recipe)
        return sublist

    def checkRecipe(self, recipe, tag=None, nutr=None, prep=None):
        good_time = (recipe.prepareTime in prep) if ((prep is not None) and prep!=[]) else True
        has_tags = (tag in recipe.tags) if (tag is not None) else True
        is_subset = (set(recipe.nutrients)<=set(nutr)) if (nutr is not None) else True

        return has_tags and is_subset and good_time

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
        with open(HELPER_TIME) as f:
            prepTime = [line.rstrip() for line in f]
        
        # add recipe objects to a list
        menu = []
        for (item, tag, ingr, prep) in zip(menuList, tags, ingridients, prepTime):
            new_recipe = Recipe(title=item, tags=tag, ingridients=ingr, prepareTime=prep)
            new_recipe.food_class = self.identifyFoodClass(new_recipe)
            new_recipe.nutrients = self.identifyNutrients(new_recipe)
            new_recipe.oneTime = True
            menu.append(new_recipe)
        # print(menu)
        # menu[5].oneTime = False
        # menu[6].oneTime = False
        # menu[11].oneTime = False
        # menu[13].oneTime = False
        # dump list in a file
        with open(DB_RECIPE, 'wb') as file:
            print("dump in db file")
            pickle.dump(menu, file)
        
        return