import pytest
import yaml
import os

with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "app_settings.yml"), 'r') as stream:
    data_loaded = yaml.safe_load(stream)

db = data_loaded['DB_TYPE']
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), data_loaded['MENU_DB'])

from ..classes.classRecipe import Recipe


from ..classes.classMenu import Menu
from ..classes.classRules import Rules

from datetime import date, timedelta

# test initializing Menu
def test_initMenu():
    m = Menu()
    
    # all dics should be not empty  
    assert bool(m.n) == 1
    assert (m.timePeriod) == "day"
    assert bool(m.repeatDishes) == True

# menu length is n-days and each day has all meals
def test_generateDailyMenu():
    sdate = date.today()
    for n in range(10):
        edate = sdate + timedelta(days=n)
        m = Menu()
        m.connectDB(db, db_path)
        m.generateDailyMenu(sdate, edate)
        assert len(m.menu) == n + 1
        for day in m.menu:
            for meal in m.mpd:
                assert meal in m.menu[day]
        m.disconnectDB()


# for each day in menu there is only one dict key, which equals 'prepTime'
def test_getEmptyMenu():
    sdate = date.today()
    for n in range(10):
        days = [sdate + timedelta(days=i) for i in range(n)]
        m = Menu()
        m.connectDB(db, db_path)
        m.getEmptyMenu(days)
        assert len(m.menu) == n
        for day in m.menu:
            assert 'prepTime' in m.menu[day]
            assert len(m.menu[day]) == 1
        m.disconnectDB()

# for each discarded meal there is None in menu on corresponding day
lines = [
    ([("On Sun discard Lunch", "1")], {'Sun': {'Lunch'}}),
    ([("On Sun, Mon discard Lunch, Breakfast", "1"), ("On Sun discard Dinner", "2")], {'Sun': {'Lunch', 'Breakfast', 'Dinner'}, 'Mon': {'Lunch', 'Breakfast'}})
]
@pytest.mark.parametrize("lines,ress", lines)
def test_discardMeals(lines, ress):
    sdate = date.today()
    # for 2 weeks and menu will have each day twice
    days = [sdate + timedelta(days=i) for i in range(14)]
    m = Menu()
    m.connectDB(db, db_path)
    m.rules = Rules() 
    for line in lines:           
        m.rules.readRules(line)
    m.getEmptyMenu(days)
    m.discardMeals()
    for day_key in m.menu:
        if day_key in ress:
            meal_keys = ress[day_key]
            for meal_key in meal_keys:
                assert m.menu[day][meal_key] == None
    m.disconnectDB()

# if there is smth to choose it is a Recipe object else None
lines = [
    ('Lunch', {'medium', 'long'}),
    ('Breakfast', {'medium'})
]
@pytest.mark.parametrize("meal, prepTimes", lines)
def test_chooseRecipe(meal, prepTimes):
    m = Menu()
    m.connectDB(db, db_path)
    meals = {"0": "Breakfast", "2": "Lunch", "4": "Dinner"}
    m.update_mpd(meals)
    m.db.generate_subsets(m.mpd)
    recipe = m.db.chooseRecipe(meal, prepTimes)
    sub = m.db.subsets[meal]['recipes']
    if tuple(prepTimes) not in sub:
        assert recipe == None
    else:
        assert recipe.__class__.__name__ == 'Recipe'
    m.disconnectDB()

# deleteRecipeFromSets(self, recipe):
def test_deleteRecipeFromSetsOne():
    m = Menu()
    m.connectDB(db, db_path)
    meals = {"0": "Breakfast", "2": "Lunch", "4": "Dinner"}
    m.update_mpd(meals)
    m.db.generate_subsets(m.mpd)
    a = None
    recipe = None
    newsubsets = {}
    # for cases with subsets that have more than one recipes
    for meal in m.db.subsets:
        newsubsets[meal] = {}
        newsubsets[meal]['recipes'] = {}
        for prepTime in m.db.subsets[meal]['recipes']:
            # add to a new dict all subsets with len > 1
            # first recipe from the first such subset is added to others
            if len(m.db.subsets[meal]['recipes'][prepTime])>1:
                newsubsets[meal]['recipes'][prepTime] = m.db.subsets[meal]['recipes'][prepTime]
                if a is None:
                    a = m.db.subsets[meal]['recipes'][prepTime]
                    recipe = list(a)[0]
                else:
                    newsubsets[meal]['recipes'][prepTime].add(recipe)
                
    m.db.subsets = newsubsets
    if a is not None:
        # delete our recipe from all subsets and check it
        m.db.deleteRecipeFromSets(recipe)
        for meal in m.db.subsets:
            for prepTime in m.db.subsets[meal]['recipes']:
                assert recipe not in m.db.subsets[meal]['recipes'][prepTime]

    m.disconnectDB()

# for cases with subsets with one element
def test_deleteRecipeFromSetsTwo():
    m = Menu()
    m.connectDB(db, db_path)
    meals = {"0": "Breakfast", "2": "Lunch", "4": "Dinner"}
    m.update_mpd(meals)
    m.db.generate_subsets(m.mpd)
    
    a = None
    del_len = None
    newsubsets = {}
    # take one subset and delete all elements except one
    # save original length of this subset
    for meal in m.db.subsets:        
        for prepTime in m.db.subsets[meal]['recipes']:
            if del_len is None:
                newsubsets[meal] = m.db.subsets[meal]
                a = list(m.db.subsets[meal]['recipes'][prepTime])
                del_len = len(a)
                newsubsets[meal]['recipes'] = {}
                newsubsets[meal]['recipes'][prepTime] = set([a[0]])
    m.db.subsets = newsubsets
    
    # delete recipe and check if the subset returned to its original length
    if del_len is not None:
        m.db.deleteRecipeFromSets(a[0])
        for meal in m.db.subsets:
            for prepTime in m.db.subsets[meal]['recipes']:
                assert len(m.db.subsets[meal]['recipes'][prepTime])==del_len

    m.disconnectDB()

lines = [
    (['breakfast'], ['free', 'high_carb'], 'short', 1), # all is the same
    (['breakfast'], ['free', 'protein', 'high_carb'], 'short', 1), # nutrients are not all the same
    (['breakfast'], ['free', 'protein'], 'short', 0), # nutrients are different
    (['breakfast'], ['free', 'high_carb'], 'medium', 0), # prepareTime is different
    (['breakfast'], ['free', 'high_carb'], ['short', 'medium'], 1), # multiple prepareTimes
    (['dinner'], ['free', 'protein'], 'short', 1), # tags are different
    (['dinner'], ['free', 'high_carb', 'protein', 'fat'], 'short', 2) # prepTime is empty 
]
@pytest.mark.parametrize("tag, nutr, prep, res", lines)
def test_filter(tag, nutr, prep, res):
    m = Menu()
    m.connectDB(db, db_path)
    # meals = {"0": "Breakfast", "2": "Lunch", "4": "Dinner"}
    # m.update_mpd(meals)
    # m.db.generate_subsets(m.mpd)
    newCollection = m.db.db.db.collection('testCollection')
    newCollection.create()
    newCollection.store({'title': '', 'img': '', 'ingredients': [], 'prepareTime': 'short', 'tags': ['breakfast'], 'repeat': False, 'description': '', 'food_class': [], 'nutrients': ['high_carb', 'free'], '__id': 27})
    newCollection.store({'title': '', 'img': '', 'ingredients': [], 'prepareTime': 'long', 'tags': ['breakfast'], 'repeat': False, 'description': '', 'food_class': [], 'nutrients': ['high_carb', 'free'], '__id': 28})
    newCollection.store({'title': '', 'img': '', 'ingredients': [], 'prepareTime': 'short', 'tags': ['dinner'], 'repeat': False, 'description': '', 'food_class': [], 'nutrients': ['protein', 'free'], '__id': 29})
    newCollection.store({'title': '', 'img': '', 'ingredients': [], 'prepareTime': 'medium', 'tags': ['dinner'], 'repeat': False, 'description': '', 'food_class': [], 'nutrients': ['free', 'protein', 'high_carb'], '__id': 30})
    newCollection.store({'title': '', 'img': '', 'ingredients': [], 'prepareTime': 'short', 'tags': ['dinner'], 'repeat': False, 'description': '', 'food_class': [], 'nutrients': ['fat', 'free'], '__id': 31})
    m.db.db.recipesCollection = newCollection

    test_res = m.db.filter(tag, nutr, prep)
    newCollection.drop()

    assert len(test_res) == res

    m.disconnectDB()

lines = [
    (['breakfast'], ['free', 'high_carb'], 'short', True), # all is the same
    (['breakfast'], ['free', 'protein', 'high_carb'], 'short', True), # nutrients are not all the same
    (['breakfast'], ['free', 'protein'], 'short', False), # nutrients are different
    (['breakfast'], ['free', 'high_carb'], 'medium', False), # prepareTime is different
    (['breakfast'], ['free', 'high_carb'], ['short', 'medium'], True), # multiple prepareTimes
    (['dinner'], ['free', 'high_carb'], 'short', False), # tags are different
    (['breakfast', 'dough food'], ['free', 'high_carb'], 'short', True) # more than one tag 
]
@pytest.mark.parametrize("tag, nutr, prep, res", lines)
def test_checkRecipe(tag, nutr, prep, res):
    m = Menu()
    m.connectDB(db, db_path)
    recipe = Recipe()
    recipe.tags = ['breakfast']
    recipe.prepareTime = 'short'
    recipe.nutrients = ['free', 'high_carb']
    assert m.db.checkRecipe(recipe, tag, nutr, prep) == res

    m.disconnectDB()

# without discardMeals()
def test_fillMenu():
    sdate = date.today()
    for n in range(10):
        days = [sdate + timedelta(days=i) for i in range(n)]
        m = Menu()
        m.connectDB(db, db_path)
        meals = {"0": "Breakfast", "2": "Lunch", "4": "Dinner"}
        m.update_mpd(meals)
        m.db.generate_subsets(m.mpd)
        m.getEmptyMenu(days)
        m.fillMenu()
        for day in m.menu:
            for meal in m.mpd:
                assert m.menu[day][meal] is not None
    
    m.disconnectDB()

lines = [
    # 1: Today I have a breakfast, when can I eat the same dish? - Tomorrow at breakfast 
    ({'Breakfast': {'tag': ['breakfast'], 'nutr': ['low_carb', 'high_carb', 'fat', 'free']}, 
    'Lunch': {'tag': None, 'nutr': ['low_carb', 'high_carb', 'protein', 'fat', 'free']}, 
    'Dinner': {'tag': None, 'nutr': ['protein', 'fat', 'free', 'low_carb']}}, 
    {'meal': 'Breakfast', 'tags': ['breakfast'], 'prepareTime': 'short', 'nutrients': ['free', 'high_carb']}, 
    {},
    (1, 'Breakfast')),
    # 2 Today I have a breakfast, tomorrow I have a breakfast, when can I eat the same dish? - Tomorrow at lunch
    ({'Breakfast': {'tag': ['breakfast'], 'nutr': ['low_carb', 'high_carb', 'fat', 'free']}, 
    'Lunch': {'tag': None, 'nutr': ['low_carb', 'high_carb', 'protein', 'fat', 'free']}, 
    'Dinner': {'tag': None, 'nutr': ['protein', 'fat', 'free', 'low_carb']}}, 
    {'meal': 'Breakfast', 'tags': ['breakfast'], 'prepareTime': 'short', 'nutrients': ['free', 'high_carb']}, 
    {'meal': 'Breakfast', 'tags': ['breakfast'], 'prepareTime': 'short', 'nutrients': ['free', 'high_carb']},
    (1, 'Lunch')),
    # 3 Today I have a lunch, tomorrow I have a lunch, when can I eat the same dish? - A day after tomorrow at lunch
    ({'Breakfast': {'tag': ['breakfast'], 'nutr': ['low_carb', 'high_carb', 'fat', 'free']}, 
    'Lunch': {'tag': None, 'nutr': ['low_carb', 'high_carb', 'protein', 'fat', 'free']}, 
    'Dinner': {'tag': None, 'nutr': ['protein', 'fat', 'free', 'low_carb']}}, 
    {'meal': 'Lunch', 'tags': ['dinner'], 'prepareTime': 'short', 'nutrients': ['free', 'high_carb']},
    {'meal': 'Lunch', 'tags': ['dinner'], 'prepareTime': 'short', 'nutrients': ['free', 'high_carb']},  (2, 'Lunch'))
]
@pytest.mark.parametrize("subset, fakeRecipe1, fakeRecipe2, res", lines)
def test_findAvailableDay(subset, fakeRecipe1, fakeRecipe2, res):
    sdate = date.today()
    days = [sdate + timedelta(days=i) for i in range(3)]
    m = Menu()
    m.connectDB(db, db_path)
    meals = {"0": "Breakfast", "2": "Lunch", "4": "Dinner"}
    m.update_mpd(meals)
    # m.db.generate_subsets(m.mpd)
    m.getEmptyMenu(days)
    m.db.subsets = subset
    recipe = Recipe(tags=fakeRecipe1['tags'], nutrients=fakeRecipe1['nutrients'],prepareTime=fakeRecipe1['prepareTime'])
    m.menu[sdate.isoformat()][fakeRecipe1['meal']] = recipe
    if fakeRecipe2:
        recipe2 = Recipe(tags=fakeRecipe2['tags'], nutrients=fakeRecipe2['nutrients'],prepareTime=fakeRecipe2['prepareTime'])
        m.menu[(sdate + timedelta(days=1)).isoformat()][fakeRecipe2['meal']] = recipe2
    
    ind_day, meal = res
    new_res = ((sdate + timedelta(days=ind_day)).isoformat(), meal)
    assert m.findAvailableDay(sdate.isoformat(), recipe)==new_res

    m.disconnectDB()