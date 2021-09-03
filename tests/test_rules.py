from ..classRules import Rules

# test initializing Rules with empty db_path
def test_initRules():
    r = Rules()
    dics = r.meal_tag and r.class_nutrient
    dics = dics and r.meal_nutrient and r.tag_ignore_nutrient
    dics = dics and r.day_time and r.day_discard_meal
    
    # all dics should be empty  
    assert bool(dics) == False