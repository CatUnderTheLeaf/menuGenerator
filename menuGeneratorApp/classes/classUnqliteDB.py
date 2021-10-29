from unqlite import UnQLite
from classes.classRecipe import Recipe
from classes.classRules import Rules

class UnqliteDB:
    
    def __init__(self, path):
        self.db = UnQLite(path)
        # create products collection
        self.products = self.db.collection('products')
        self.products.create() 
        # create recipes collection
        self.recipesCollection = self.db.collection('recipes')
        self.recipesCollection.create()
        # create rules collection
        self.rulesCollection = self.db.collection('rules')
        self.rulesCollection.create()
        
        self._rules = None
        self._recipes = None

    """ 
    fetch all rules from the collection
    and convert to the Rules object

    :return: Rules object 
  
     """   
    def getRules(self):
        if (self._rules is None):            
            all = self.rulesCollection.all()
            self._rules = Rules([x['rule'] for x in all])
        return self._rules

    """ 
    fetch all recipes from the collection
    and convert to the Recipe objects

    :return: list of Recipe objects 
  
     """
    def getRecipes(self):
        print("get all recipes")
        if (self._recipes is None):        
            all = self.recipesCollection.all()
            self._recipes = [self.makeRecipeFromRecord(x) for x in all]
        return self._recipes

    """ 
    make a Recipe object from collections record

    :param record: record in the recipe collection
    :return: Recipe object
  
     """
    def makeRecipeFromRecord(self, record):
        return Recipe(id = record['__id'],
                        title=record['title'], 
                        ingridients=record['ingridients'], 
                        food_class=record['food_class'], 
                        nutrients=record['nutrients'], 
                        prepareTime=record['prepareTime'], 
                        text=record['description'], 
                        tags=record['tags'], 
                        oneTime=record['oneTime']) 

    """ 
    update recipe in the collection
  
     """
    def updateRecipe(self, id, recipe):
        self.recipesCollection.update(id, recipe)

    """ 
    filter recipes by tags, nutrients and preparation time

    :param tag: tags of recipe ('breakfast', etc)
    :param nutr: list of 'carb', 'protein' or 'fat'
    :param prep: list of preparation times
    :return: a sublist of recipes
    """
    def filter(self, tag=None, nutr=None, prep=None):
        sublist = self.recipesCollection.filter(lambda recipe: self.checkRecipe(recipe['prepareTime'],
                                                                    recipe['tags'],
                                                                    recipe['nutrients'],
                                                                    tag, nutr, prep) == True)
        return [self.makeRecipeFromRecord(x) for x in sublist]


    """ 
    check if recipe suits criterias

    :param recipe: a recipe
    :param tag: tags of recipe ('breakfast', etc)
    :param nutr: list of 'carb', 'protein' or 'fat'
    :param prep: list of preparation times
    :return: True or False
    """
    def checkRecipe(self, recipePrepareTime, recipeTags, recipeNutrients, tag=None, nutr=None, prep=None):
        good_time = (recipePrepareTime in prep) if ((prep is not None) and prep!=[]) else True
        has_tags = (not set(tag).isdisjoint(set(recipeTags))) if (tag is not None) else True
        is_subset = (set(recipeNutrients)<=set(nutr)) if (nutr is not None) else True

        return has_tags and is_subset and good_time

    """ 
    close DB connection
 
    """
    def disconnect(self):
        self.db.close()
