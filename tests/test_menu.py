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

lines = [
    (["On Sun discard Lunch"], 'day_discard_meal', {'Sun': {'Lunch'}}),
    (["On Sun, Mon discard Lunch, Breakfast", "On Sun discard Dinner"], 'day_discard_meal', {'Sun': {'Lunch', 'Breakfast', 'Dinner'}, 'Mon': {'Lunch', 'Breakfast'}})
]
@pytest.mark.parametrize("lines,key,res", lines)
def test_discardMeals(lines, key, res):
    for line in lines:
        sdate = date.today()
        days = [sdate + timedelta(days=i) for i in range(10)]
        m = Menu()
        m.rules = Rules()
    
        m.rules.readRules(line)
    m.getEmptyMenu(days)
    m.discardMeals()


# fillMenu(self):

# chooseRecipe(self, meal, prepTime):

# deleteRecipeFromSets(self, recipe):

# findAvailableDay(self, old_date, recipe):

# filter(self, tag=None, nutr=None, prep=None):

# checkRecipe(self, recipe, tag=None, nutr=None, prep=None):
