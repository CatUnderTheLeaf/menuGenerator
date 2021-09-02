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
            self.subsets[meal]['recipes'] = {}
            for prep in times_groups:
                # Check if recipes should be filtered 
                # by tags for this type of meal
                tag, nutr = self.rules.filterByMeal(meal)
                if tag is not None or nutr is not None:
                    # print("filter with tags or nutrients")
                    sublist = self.filter(tag, nutr, prep)
                    self.subsets[meal]['recipes'][prep] = set(sublist)
                    self.subsets[meal]['tag'] = tag
                    self.subsets[meal]['nutr'] = nutr
                
    def __repr__(self):
       return repr(self.recipeList)

    def __str__(self):
        menu = []
        menu.append("!!!-----------------generated menu----------------!!!")
        for day in self.menu:
            menu.append("\n{}, {}:".format(day, day.strftime("%a")))
            for meal in self.mpd:
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

        self.getEmptyMenu(days)
        self.discardMeals()
        self.fillMenu()
        
        return

    """ 
    generate empty menu with corresponding prep times

    :param days: calendar dates
    
     """
    def getEmptyMenu(self, days):
        prepTimes = self.rules.getPrepTimes(days)
        self.menu = {day: {'prepTime': prepTimes[day]} for day in days}   
        return

    """ 
    fill in the menu with discarded meals
    
     """
    def discardMeals(self):
        days = self.menu.keys()
        days_meals = self.rules.filterDiscardedMeals(days)
        
        # discard meals if there are rules
        for (day, meals) in days_meals:
            for meal in meals:
                self.menu[day][meal] = None
        return

    """ 
    fill in the menu
    
     """
    def fillMenu(self):        
        # for each meal/day get recipe from the corresponding subset
        for date in self.menu:
            for meal in self.mpd:
                if meal not in self.menu[date]:                    
                    cur_recipe = self.chooseRecipe(meal, self.menu[date]['prepTime'])
                    self.menu[date][meal] = cur_recipe
                    # if dishes can be repeated search for next available day and meal
                    if self.repeatDishes and not cur_recipe.oneTime:
                        availableDay = self.findAvailableDay(date, cur_recipe)
                        if availableDay:
                            nextDate, nextMeal = availableDay
                            self.menu[nextDate][nextMeal] = cur_recipe
        return

    """ 
    randomly choose recipe from the recipe subsets
    and delete it, so there will be no same dishes in one day

    :param meal: 'Breakfast', 'Lunch' or 'Dinner'
    :param prepTime: preparation time
    :return: recipe
    
     """
    def chooseRecipe(self, meal, prepTime):
        recipe = random.sample(self.subsets[meal]['recipes'][prepTime], 1)[0]
        # delete this recipe from all sets
        self.deleteRecipeFromSets(recipe)
        return recipe

    """ 
    delete recipe from subsets, so there will be no same dishes in one day

    :param recipe: recipe to delete from subsets
    
     """
    def deleteRecipeFromSets(self, recipe):        
        for meal in self.subsets:
            for prepTime in self.subsets[meal]['recipes']:
                self.subsets[meal]['recipes'][prepTime].discard(recipe)
                # if subset is empty get it anew
                if len(self.subsets[meal]['recipes'][prepTime]) < 1:
                    sublist = self.filter(self.subsets[meal]['tag'], self.subsets[meal]['nutr'], prepTime)
                    self.subsets[meal]['recipes'][prepTime] = set(sublist)
        return

    """ 
    find next available slot in the menu for a dish
    which can be eaten more than one time

    :param old_date: day of recipe in Menu
    :param recipe: a recipe of the dish
    :return: tuple (day, meal) if slot is available
    """
    def findAvailableDay(self, old_date, recipe):
        dates = sorted(self.menu.keys())
        s_ind = dates.index(old_date)
        new_dates = dates[s_ind+1:]
        for date in new_dates:
            for meal in self.mpd:
                if meal not in self.menu[date]:                    
                    check = self.checkRecipe(recipe, self.subsets[meal]['tag'], self.subsets[meal]['nutr'], self.menu[date]['prepTime'])
                    if check:
                        return (date, meal)       
        return

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

    """ 
    check if recipe suits criterias

    :param recipe: a recipe
    :param tag: tags of recipe ('breakfast', etc)
    :param nutr: list of 'carb', 'protein' or 'fat'
    :param prep: list of preparation times
    :return: True or False
    """
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