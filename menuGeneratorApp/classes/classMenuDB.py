import random
from classes.classSqliteDB import SqliteDB
from classes.classUnqliteDB import UnqliteDB

class MenuDB:
        
    def __init__(self, type, path):
        if type=='sqlite':
            self.db = SqliteDB(path)
        if type=='unqlite':
            self.db = UnqliteDB(path)
        # subsets of recipes for each mealtype
        self.subsets = {}
    
    """ 
    get all products from the DB

    :return: dict of products 
  
     """   
    def getProducts(self):
        return self.db.getProducts()

    """ 
    get rules from the DB
    converted to the Rules object

    :return: Rules object 
  
     """
    def getRules(self):
        return self.db.getRules()

    """ 
    get tags from the DB

    :return: list of tags
  
     """
    def getTags(self):
        return self.db.getTags()

    """ 
    ret all recipes

    :return: list of Recipe objects 
  
     """
    def getRecipes(self):
        return self.db.getRecipes()

    """ 
    update recipe in the collection

    :param recipeObj: Recipe object to update  
     """
    def updateRecipe(self, recipeObj):
        recipeObj.food_class = self.identifyFoodClass(recipeObj.ingredients)
        recipeObj.nutrients = self.identifyNutrients(recipeObj.food_class, recipeObj.tags)
        if recipeObj.id=='':
            self.db.insertRecipe(recipeObj)
        else:
            self.db.updateRecipe(recipeObj.id, recipeObj)
        self.updateTags(recipeObj)

    """ 
    update recipe image paths in the collection
    it depends on device primary_external_storage_path

    :param dstpath: image dir in primary_external_storage_path
  
     """
    def updateRecipeImgPath(self, dstpath):
        self.db.updateRecipe(dstpath)
    """ 
    update rules in the collection

    :param rules: rules to update  
     """
    def updateRules(self, rules):
        self.db.updateRules(rules)

    """ 
    update tags in the db

    :param recipeObj: Recipe object
     """
    def updateTags(self, recipeObj):        
        self.db.updateTags(recipeObj)

    """ 
    delete recipe from the collection

    :param recipeIds: list of recipe ids
  
     """
    def deleteRecipes(self, recipeIds):
        self.db.deleteRecipes(recipeIds)


    """ 
    generate subsets of recipes
    grouped by meal and prepareTime    
     """  
    def generate_subsets(self, mpd):
        mpd_exist = True if len(mpd) else False
        if mpd_exist:
            need_to_generate = True if not(len(self.subsets)) else set(self.subsets.keys())!=set(mpd)
            if need_to_generate:
                times_groups = self.getRules().getDayTimes()
                for meal in mpd:
                    self.subsets[meal] = {}
                    self.subsets[meal]['recipes'] = {}
                    for prep in times_groups:
                        # Check if recipes should be filtered 
                        # by tags for this type of meal
                        tag, nutr = self.getRules().filterByMeal(meal)
                        if tag is not None or nutr is not None:
                            sublist = self.filter(tag, nutr, prep)
                            self.subsets[meal]['recipes'][tuple(prep)] = set(sublist)
                            self.subsets[meal]['tag'] = tag
                            self.subsets[meal]['nutr'] = nutr

    """ 
    filter recipes by tags, nutrients and preparation time

    :param tag: tags of recipe ('breakfast', etc)
    :param nutr: list of 'carb', 'protein' or 'fat'
    :param prep: list of preparation times
    :return: a subset of recipes
    """
    def filter(self, tag=None, nutr=None, prep=None):
        return self.db.filter(tag, nutr, prep)

    """ 
    randomly choose recipe from the recipe subsets
    and delete it, so there will be no same dishes in one day

    :param meal: 'Breakfast', 'Lunch' or 'Dinner'
    :param prepTime: preparation time
    :return: recipe
    
     """
    def chooseRecipe(self, meal, prepTime):
        sub = self.subsets[meal]['recipes']
        prepTime = tuple(prepTime)
        if prepTime not in sub or len(sub[prepTime]) < 1:
            return None
        else:
            recipe = random.sample(sub[prepTime], 1)[0]
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
                if recipe in self.subsets[meal]['recipes'][prepTime]:
                    self.subsets[meal]['recipes'][prepTime].discard(recipe)
                    # if subset is empty get it anew
                    if len(self.subsets[meal]['recipes'][prepTime]) < 1:
                        sublist = self.filter(self.subsets[meal]['tag'], self.subsets[meal]['nutr'], prepTime)
                        self.subsets[meal]['recipes'][prepTime] = set(sublist)
        return


    """ 
    check if recipe suits criterias

    :param recipe: a recipe
    :param tag: tags of recipe ('breakfast', etc)
    :param nutr: list of 'carb', 'protein' or 'fat'
    :param prep: list of preparation times
    :return: True or False
    """
    def checkRecipe(self, recipe, tag, nutr, prep):
        return self.db.checkRecipe(recipe.prepareTime, recipe.tags, recipe.nutrients, tag, nutr, prep)

    """ 
    identify to which food class 
    belong ingredients

    :param recipe: a single recipe
    :return: list of unique food classes    
     """
    def identifyFoodClass(self, ingredients):        
        return self.db.identifyFoodClass(ingredients)

    """ 
    identify to which nutrient type 
    belongs recipe

    :param recipe: a single recipe
    :return: list of unique nutrient types (carb, protein, fat or free)    
     """
    def identifyNutrients(self, food_class, tags):            
        nutrients = self.db.getRules().identifyNutrient(food_class, tags)
               
        return nutrients

    """ 
    close DB connection
 
    """
    def disconnect(self):
        self.db.disconnect()
