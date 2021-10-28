from classes.classSqliteDB import SqliteDB
from classes.classUnqliteDB import UnqliteDB

class MenuDB:
    
    def __init__(self, type, path):
        if type=='sqlite':
            self.db = SqliteDB(path)
        if type=='unqlite':
            self.db = UnqliteDB(path)
    
    """ 
    get rules from the DB
    converted to the Rules object

    :return: Rules object 
  
     """
    def getRules(self):
        return self.db.getRules()

    """ 
    ret all recipes

    :return: list of Recipe objects 
  
     """
    def getRecipes(self):
        return self.db.getRecipes()

    """ 
    generate subsets of recipes
    grouped by meal and prepareTime    
     """  
    def generate_subsets(self, mpd):
        self.db.generate_subsets(mpd)

    """ 
    randomly choose recipe from the recipe subsets
    and delete it, so there will be no same dishes in one day

    :param meal: 'Breakfast', 'Lunch' or 'Dinner'
    :param prepTime: preparation time
    :return: recipe
    
     """
    def chooseRecipe(self, meal, prepTime):
        return self.db.chooseRecipe(meal, prepTime)

    """ 
    check if recipe suits criterias

    :param recipe: a recipe
    :param tag: tags of recipe ('breakfast', etc)
    :param nutr: list of 'carb', 'protein' or 'fat'
    :param prep: list of preparation times
    :return: True or False
    """
    def checkRecipe(self, recipe, tag, nutr, prep):
        return self.db.checkRecipe(recipe, tag, nutr, prep)

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
        nutrients = self.db.getRules().identifyNutrient(recipe.food_class, recipe.tags)
               
        return nutrients

    """ 
    close DB connection
 
    """
    def disconnect(self):
        self.db.disconnect()
