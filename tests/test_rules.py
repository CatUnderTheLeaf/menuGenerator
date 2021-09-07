import pytest
from ..classRules import Rules

# test initializing Rules with empty db_path
def test_initRules():
    r = Rules()
    dics = r.rules['meal_tag'] and r.rules['class_nutrient']
    dics = dics and r.rules['meal_nutrient'] and r.rules['tag_ignore_nutrient']
    dics = dics and r.rules['day_time'] and r.rules['day_discard_meal']
    
    # all dics should be empty  
    assert bool(dics) == False


lines = [
    ("At Breakfast serve only breakfast", 'meal_tag', {'Breakfast': 'breakfast'}),
    ("short, medium prepareTime on Mon, Tue, Wed, Thu, Fri", 'day_time', {'Mon': ('short', 'medium'), 'Tue': 
('short', 'medium'), 'Wed': ('short', 'medium'), 'Thu': ('short', 'medium'), 'Fri': ('short', 'medium')}),
    ("For dough food ignore protein", 'tag_ignore_nutrient', {'dough food': ['protein']}),
    ("cereals_grains_pasta_bread_vegan is high_carb", 'class_nutrient', {'cereals_grains_pasta_bread_vegan': ['high_carb']}),
    ("dairy is low_carb, protein, fat", 'class_nutrient', {'dairy': ['low_carb', 'protein', 'fat']}),
    ("For Breakfast use low_carb, high_carb, fat, free", 'meal_nutrient', {'Breakfast': ['low_carb', 'high_carb', 'fat', 'free']}),
    ("On Sun discard Lunch", 'day_discard_meal', {'Sun': ['Lunch']}),
    pytest.param("On Sun discarding Lunch", 'day_discard_meal', {'Sun': ['Lunch']}, marks=pytest.mark.xfail)
]
@pytest.mark.parametrize("line,key,res", lines)
def test_readRules(line, key, res):
    r = Rules()
    r.readRules(line)
    assert r.rules[key] == res

meal_tags = [("At Breakfast serve only breakfast", 'Breakfast', 'breakfast'),
            ("At Breakfast serve only breakfast", 'Lunch', None)]
@pytest.mark.parametrize("line,key,res", meal_tags)
def test_filterByTag(line, key, res):
    r = Rules()
    r.readRules(line)
    assert r.filterByTag(key) == res

meal_nutrients = [("For Breakfast use low_carb, high_carb, fat, free", 'Breakfast', ['low_carb', 'high_carb', 'fat', 'free']),
                ("For Breakfast use low_carb, high_carb, fat, free", 'Lunch', None)]
@pytest.mark.parametrize("line,key,res", meal_nutrients)
def test_filterByNutrient(line, key, res):
    r = Rules()
    r.readRules(line)
    assert r.filterByNutrient(key) == res

days_times = [(["short, medium prepareTime on Mon, Tue, Wed, Thu, Fri"], {('short', 'medium')}),
            (["short, medium prepareTime on Mon, Tue, Wed, Thu, Fri", "medium, long prepareTime on Sat, Sun"], {('short', 'medium'), ('medium', 'long')})]
@pytest.mark.parametrize("lines,res", days_times)
def test_getDayTimes(lines, res):
    r = Rules()
    for line in lines:
        r.readRules(line)
    assert r.getDayTimes() == res

from datetime import date, timedelta

def getDates(n):
    days = [date.today() + timedelta(days=i) for i in range(n)]
    return days

dates_times = [(["short, medium prepareTime on Mon, Tue, Wed, Thu, Fri", "medium, long prepareTime on Sat, Sun"], 
            [(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], ('short', 'medium')), (['Sat', 'Sun'], ('medium', 'long'))]),
            (["short, medium prepareTime on Mon, Tue, Wed, Thu, Fri"], 
            [(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], ('short', 'medium')), (['Sat', 'Sun'], None)])]

@pytest.mark.parametrize("lines,ress", dates_times)
def test_getPrepTimes(lines, ress):
    r = Rules()
    for line in lines:
        r.readRules(line)

    result = {}
    dates = getDates(7)
    for date in dates:
        for res in ress:
            days, times = res
            day = date.strftime("%a")
            if day in days:
                result[date] = times
    
    assert r.getPrepTimes(dates) == result