from unqlite import UnQLite
from sortedcontainers import SortedList
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
        self._tags = None
        self._products = None

    """ 
    fetch all products from the collection

    :return: dict of products 
  
     """   
    def getProducts(self):
        if (self._products is None):            
            all = {}
            it = self.products.iterator()
            for row in it:                
                if row['food_class'] in all:
                        all[row['food_class']].add(row['name'])
                else:
                    all[row['food_class']] = SortedList([row['name']])
            self._products = all
        return self._products

    """ 
    identify to which food class 
    belong ingridients

    :param recipe: a single recipe
    :return: list of unique food classes    
     """
    def identifyFoodClass(self, ingridients):            
        food = self.products.filter(lambda ingridient: (ingridient['name'] in ingridients)==True)
        foodClass = set(x['food_class'] for x in food)
        
        return list(foodClass)

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
    get tags from the DB

    :return: list of tags
  
     """
    def getTags(self):
        if (self._tags is None):   
            allTags = set()                
            for recipe in self._recipes:
                allTags.update(recipe.tags)
            self._tags = allTags
        return self._tags

    """ 
    update tags in the db

    :param recipeObj: Recipe object
     """
    def updateTags(self, recipeObj):        
        self.getTags()
        self._tags.update(recipeObj.tags)

    """ 
    get tags from the DB that are not in the recipe

    :param tags: set of recipe tags
    :return: list of tags
  
     """
    def getUnusedTags(self, tags):
        allTags = self.getTags()
        return list(allTags - set(tags))

    """ 
    fetch all recipes from the collection
    and convert to the Recipe objects

    :return: list of Recipe objects 
  
     """
    def getRecipes(self):
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
                        repeat=record['repeat']) 

    """ 
    update recipe in the collection

    :param id: recipe id
    :param recipeObj: Recipe object to update
  
     """
    def updateRecipe(self, id, recipeObj):

        recipe = {}
        recipe['title'] = recipeObj.title
        recipe['ingridients'] = recipeObj.ingridients
        recipe['prepareTime'] = recipeObj.prepareTime
        recipe['tags'] = recipeObj.tags
        recipe['repeat'] = recipeObj.repeat
        recipe['description'] = recipeObj.description
        recipe['food_class'] = recipeObj.food_class
        recipe['nutrients'] = recipeObj.nutrients

        self.recipesCollection.update(id, recipe)
        

    """ 
    delete recipes from the collection

    :param ids: list of recipe ids
  
     """
    def deleteRecipes(self, ids):
        for id in ids:
            self.recipesCollection.delete(id)

    """ 
    insert recipe in the collection

    :param recipeObj: Recipe object to insert  
     """
    def insertRecipe(self, recipeObj):

        recipe = {}
        recipe['title'] = recipeObj.title
        recipe['ingridients'] = recipeObj.ingridients
        recipe['prepareTime'] = recipeObj.prepareTime
        recipe['tags'] = recipeObj.tags
        recipe['repeat'] = recipeObj.repeat
        recipe['description'] = recipeObj.description
        recipe['food_class'] = recipeObj.food_class
        recipe['nutrients'] = recipeObj.nutrients

        self.recipesCollection.store(recipe)

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
