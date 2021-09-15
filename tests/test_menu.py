from classRecipe import Recipe
import pytest
from classMenu import Menu
from classRules import Rules

from datetime import date, timedelta

# test initializing Menu
def test_initMenu():
    m = Menu()
    dics = m.rules and m.products_class
    dics = dics and m.recipeList
    dics = dics and m.subsets
    
    # all dics should be not empty  
    assert bool(dics) == True

# menu length is n-days and each day has all meals
def test_generateDailyMenu():
    sdate = date.today()
    for n in range(10):
        edate = sdate + timedelta(days=n)
        m = Menu()
        m.generateDailyMenu(sdate, edate)
        assert len(m.menu) == n + 1
        for day in m.menu:
            for meal in m.mpd:
                assert meal in m.menu[day]


# for each day in menu there is only one dict key, which equals 'prepTime'
def test_getEmptyMenu():
    sdate = date.today()
    for n in range(10):
        days = [sdate + timedelta(days=i) for i in range(n)]
        m = Menu()
        m.getEmptyMenu(days)
        assert len(m.menu) == n
        for day in m.menu:
            assert 'prepTime' in m.menu[day]
            assert len(m.menu[day]) == 1

# for each discarded meal there is None in menu on corresponding day
lines = [
    (["On Sun discard Lunch"], {'Sun': {'Lunch'}}),
    (["On Sun, Mon discard Lunch, Breakfast", "On Sun discard Dinner"], {'Sun': {'Lunch', 'Breakfast', 'Dinner'}, 'Mon': {'Lunch', 'Breakfast'}})
]
@pytest.mark.parametrize("lines,ress", lines)
def test_discardMeals(lines, ress):
    sdate = date.today()
    # for 2 weeks and menu will have each day twice
    days = [sdate + timedelta(days=i) for i in range(14)]
    m = Menu()
    m.rules = Rules() 
    for line in lines:           
        m.rules.readRules(line)
    m.getEmptyMenu(days)
    m.discardMeals()
    for day in m.menu:
        day_key = day.strftime("%a")
        if day_key in ress:
            meal_keys = ress[day_key]
            for meal_key in meal_keys:
                assert m.menu[day][meal_key] == None

# if there is smth to choose it is a Recipe object else None
lines = [
    ('Lunch', ('medium', 'long')),
    ('Breakfast', ('medium'))
]
@pytest.mark.parametrize("meal, prepTimes", lines)
def test_chooseRecipe(meal, prepTimes):
    m = Menu()
    recipe = m.chooseRecipe(meal, prepTimes)
    sub = m.subsets[meal]['recipes']
    if prepTimes not in sub or len([prepTimes]) < 1:
        assert recipe == None
    else:
        assert isinstance(recipe, Recipe)

# deleteRecipeFromSets(self, recipe):
def test_deleteRecipeFromSetsOne():
    m = Menu()
    a = None
    recipe = None
    newsubsets = {}
    # for cases with subsets that have more than one recipes
    for meal in m.subsets:
        newsubsets[meal] = {}
        newsubsets[meal]['recipes'] = {}
        for prepTime in m.subsets[meal]['recipes']:
            # add to a new dict all subsets with len > 1
            # first recipe from the first such subset is added to others
            if len(m.subsets[meal]['recipes'][prepTime])>1:
                newsubsets[meal]['recipes'][prepTime] = m.subsets[meal]['recipes'][prepTime]
                if a is None:
                    a = m.subsets[meal]['recipes'][prepTime]
                    recipe = list(a)[0]
                else:
                    newsubsets[meal]['recipes'][prepTime].add(recipe)
                
    m.subsets = newsubsets
    if a is not None:
        # delete our recipe from all subsets and check it
        m.deleteRecipeFromSets(recipe)
        for meal in m.subsets:
            for prepTime in m.subsets[meal]['recipes']:
                assert recipe not in m.subsets[meal]['recipes'][prepTime]

# for cases with subsets with one element
def test_deleteRecipeFromSetsTwo():
    m = Menu()
    
    a = None
    del_len = None
    newsubsets = {}
    # take one subset and delete all elements except one
    # save original length of this subset
    for meal in m.subsets:        
        for prepTime in m.subsets[meal]['recipes']:
            if del_len is None:
                newsubsets[meal] = m.subsets[meal]
                a = list(m.subsets[meal]['recipes'][prepTime])
                del_len = len(a)
                newsubsets[meal]['recipes'] = {}
                newsubsets[meal]['recipes'][prepTime] = set([a[0]])
    m.subsets = newsubsets
    
    # delete recipe and check if the subset returned to its original length
    if del_len is not None:
        m.deleteRecipeFromSets(a[0])
        for meal in m.subsets:
            for prepTime in m.subsets[meal]['recipes']:
                assert len(m.subsets[meal]['recipes'][prepTime])==del_len





# findAvailableDay(self, old_date, recipe):

# filter(self, tag=None, nutr=None, prep=None):

# checkRecipe(self, recipe, tag=None, nutr=None, prep=None):


# fillMenu(self):