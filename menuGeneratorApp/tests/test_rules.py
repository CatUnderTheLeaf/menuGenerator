import pytest
from ..classes.classRules import Rules

# test initializing Rules with empty db_path
def test_initRules():
    r = Rules()
    dics = r.rules['meal_tag'] and r.rules['class_nutrient']
    dics = dics and r.rules['meal_nutrient'] and r.rules['tag_ignore_nutrient']
    dics = dics and r.rules['day_time'] and r.rules['day_discard_meal']
    
    # all dics should be empty  
    assert bool(dics) == False


lines = [
    ([("At Breakfast serve only breakfast", "1")], 'meal_tag', {'Breakfast': ({'breakfast'}, '1')}),
    ([("At Breakfast, Lunch serve only breakfast", "1")], 'meal_tag', {'Breakfast': ({'breakfast'}, '1'), 'Lunch': ({'breakfast'}, '1')}),
    ([("At Breakfast serve only breakfast, dough food", "1")], 'meal_tag', {'Breakfast': ({'breakfast', 'dough food'}, '1')}),
    ([("short, medium prepareTime on Mon, Tue, Wed, Thu, Fri", "1")], 'day_time', {'Mon': {'medium', 'short'}, 'Tue': 
        {'medium', 'short'}, 'Wed': {'medium', 'short'}, 'Thu': {'medium', 'short'}, 'Fri': {'medium', 'short'}}),
    ([("short prepareTime on Mon, Tue, Fri", "1")], 'day_time', {'Mon': {'short'}, 'Tue': 
        {'short'}, 'Fri': {'short'}}),
    ([("For dough food ignore protein", "1")], 'tag_ignore_nutrient', {'dough food': ['protein']}),
    ([("cereals_grains_pasta_bread_vegan is high_carb", "1")], 'class_nutrient', {'cereals_grains_pasta_bread_vegan': ['high_carb']}),
    ([("dairy is low_carb, protein, fat", "1")], 'class_nutrient', {'dairy': ['low_carb', 'protein', 'fat']}),
    ([("For Breakfast use low_carb, high_carb, fat, free", "1")], 'meal_nutrient', {'Breakfast': ({'fat', 'free', 'high_carb', 'low_carb'}, '1')}),
    ([("On Sun discard Lunch", "1")], 'day_discard_meal', {'Sun': {'Lunch'}}),
    ([("On Sun, Mon discard Lunch, Breakfast", "1"), ("On Sun discard Dinner", "2")], 'day_discard_meal', {'Sun': {'Lunch', 'Breakfast', 'Dinner'}, 'Mon': {'Lunch', 'Breakfast'}}),
    pytest.param([("On Sun discarding Lunch", "1")], 'day_discard_meal', {'Sun': ['Lunch']}, marks=pytest.mark.xfail)
]
@pytest.mark.parametrize("rules,key,res", lines)
def test_readRules(rules, key, res):
    r = Rules()
    for line in rules:
        r.readRules(line)
    assert r.rules[key] == res

meal_tags = [(("At Breakfast serve only breakfast", "1"), 'Breakfast', {'breakfast'}),
            (("At Breakfast serve only breakfast", "1"), 'Lunch', None)]
@pytest.mark.parametrize("line,key,res", meal_tags)
def test_filterByTag(line, key, res):
    r = Rules()
    r.readRules(line)
    assert r.filterByTag(key) == res

meal_nutrients = [(("For Breakfast use low_carb, high_carb, fat, free", "1"), 'Breakfast', {'low_carb', 'high_carb', 'fat', 'free'}),
                (("For Breakfast use low_carb, high_carb, fat, free", "1"), 'Lunch', None)]
@pytest.mark.parametrize("line,key,res", meal_nutrients)
def test_filterByNutrient(line, key, res):
    r = Rules()
    r.readRules(line)
    assert r.filterByNutrient(key) == res

days_times = [([('short prepareTime on Wednesday, Friday, Monday, Tuesday, Thursday', "1")], [{'short'}, None]),
            ([('short prepareTime on Wednesday, Friday, Monday, Tuesday, Thursday', "1"), ('medium prepareTime on Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday', "2")], [{'medium', 'short'}, {'medium'}])]
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

dates_times = [#1
    ([('short prepareTime on Wednesday, Friday, Monday, Tuesday, Thursday', "1"), ('medium prepareTime on Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday', "2")], 
        [(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], {'short', 'medium'}), (['Sat', 'Sun'], {'medium'})]),
    #2
    ([('short prepareTime on Wednesday, Friday, Monday, Tuesday, Thursday', "1")], 
    [(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], {'short'}), (['Sat', 'Sun'], None)]),
    #3
    ([('short prepareTime on Friday, Monday, Tuesday, Thursday', "1"), ('medium prepareTime on Saturday, Sunday', "2")], 
    [(['Mon', 'Tue', 'Thu', 'Fri'], {'short'}), (['Sat', 'Sun'], {'medium'}), (['Wed'], None)])
        ]

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

discarded_meals = [([("On Sun discard Lunch", "1")], [(['Sun'], {'Lunch'})]),
                    ([("On Sun discard Lunch, Breakfast", "1")], [(['Sun'], {'Lunch', 'Breakfast'})]),
                    ([("On Sun, Mon discard Lunch, Breakfast", "1")], [(['Sun', 'Mon'], {'Lunch', 'Breakfast'})]),
                    ([("On Sun, Mon discard Lunch", "1")], [(['Sun', 'Mon'], {'Lunch'})]),
                    ([("On Sun, Mon discard Lunch, Breakfast", "1"), ("On Sun discard Dinner", "2")], [(['Sun'], {'Lunch', 'Breakfast', 'Dinner'}), (['Mon'], {'Lunch', 'Breakfast'})]),
                    ([("On Sun, Mon discard Lunch", "1"), ("On Sun discard Dinner, Breakfast", "2")], [(['Sun'], {'Lunch', 'Breakfast', 'Dinner'}), (['Mon'], {'Lunch'})])]

@pytest.mark.parametrize("lines, ress", discarded_meals)
def test_filterDiscardedMeals(lines, ress):
    r = Rules()
    for line in lines:
        r.readRules(line)

    result = []
    dates = getDates(7)
    dates = [day.isoformat() for day in dates]
    for date in dates:
        for res in ress:
            days, meals = res
            if date in days:
                result.append((date, meals))
    
    assert r.filterDiscardedMeals(dates) == result