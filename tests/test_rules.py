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
    ("On Sun discard Lunch", 'day_discard_meal', {'Sun': ['Lunch']})
]
@pytest.mark.parametrize("line,key,res", lines)
def test_atRules(line, key, res):
    r = Rules()
    r.readRules(line)
    assert r.rules[key] == res