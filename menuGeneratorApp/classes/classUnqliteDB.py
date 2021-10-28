import random
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
        self.recipes = self.db.collection('recipes')
        self.recipes.create()
        # create rules collection
        self.rules = self.db.collection('rules')
        self.rules.create()
        self.subsets = {}

    """ 
    fetch all rules from the collection
    and convert to the Rules object

    :return: Rules object 
  
     """   
    def getRules(self):
        all = self.rules.all()
        return Rules([x['rule'] for x in all])

    """ 
    fetch all recipes from the collection
    and convert to the Rucipe objects

    :return: list of Recipe objects 
  
     """
    def getRecipes(self):
        all = self.recipes.all()
        return [Recipe(title=x['title'], 
                        ingridients=x['ingridients'], 
                        food_class=x['food_class'], 
                        nutrients=x['nutrients'], 
                        prepareTime=x['prepareTime'], 
                        text=x['description'], 
                        tags=x['tags'], 
                        oneTime=x['oneTime']) 
                for x in all]

    """ 
    generate subsets of recipes
    grouped by meal and prepareTime    
     """  
    def generate_subsets(self, mpd):
        mpd_exist = True if len(mpd) else False
        if mpd_exist:
            need_to_generate = True if not(len(self.subsets)) else set(self.subsets.keys())!=set(self.mpd)
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
                            # print("filter with tags or nutrients")
                            sublist = self.filter(tag, nutr, prep)
                            self.subsets[meal]['recipes'][prep] = set(sublist)
                            self.subsets[meal]['tag'] = tag
                            self.subsets[meal]['nutr'] = nutr

    """ 
    filter recipes by tags or nutrients

    :param tag: tags of recipe ('breakfast', etc)
    :param nutr: list of 'carb', 'protein' or 'fat'
    :param prep: list of preparation times
    :return: a subset of recipes
    """
    def filter(self, tag=None, nutr=None, prep=None):
        sublist = []
        for recipe in self.getRecipes():
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
        has_tags = (not set(tag).isdisjoint(set(recipe.tags))) if (tag is not None) else True
        is_subset = (set(recipe.nutrients)<=set(nutr)) if (nutr is not None) else True

        return has_tags and is_subset and good_time

    """ 
    randomly choose recipe from the recipe subsets
    and delete it, so there will be no same dishes in one day

    :param meal: 'Breakfast', 'Lunch' or 'Dinner'
    :param prepTime: preparation time
    :return: recipe
    
     """
    def chooseRecipe(self, meal, prepTime):
        sub = self.subsets[meal]['recipes']
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
    close DB connection
 
    """
    def disconnect(self):
        self.db.close()
