from itertools import groupby
""" 
A class that represent rules for generating menu

rules can be written in such patterns:
    "At breakfast serve only breakfast"
    (meal time                  Tags)    
    "Vegetable is carb and fiber"
    (type           nutrients)
    "For Breakfast use carb"
    (meal time    nutrient category)
    "For dough food ignore protein"
    (Tag                 nutrient)
    "medium, long prepareTime on Sat, Sun"
    (preparation time          day of week)

 """

class Rules:
    """ 
    meal_tag: list of tags per meal
    class_nutrient: list of correspondence of food class to nutrient type
    meal_nutrient: list of nutrients per meal
    tag_nutrient: list of ignored nutrients for tags
    day_time: list of preparation times for weekdays
     """

    meal_tag = {}
    class_nutrient = {}
    meal_nutrient = {}
    tag_nutrient = {}
    day_time = {}

    """ 
    :param db_rules: path to db file
     """
    def __init__(self, db_rules):
        print("load rules")
        with open(db_rules, 'r') as file:
            for line in file:
                rule = line.strip()
                if ' serve only ' in rule:
                    meal, tag = rule.split(' serve only ')
                    self.meal_tag[meal[len('At '):]] = tag
                elif ' is ' in rule:
                    product_class, nutrients = rule.split(' is ')
                    self.class_nutrient[product_class] = nutrients.split(', ')
                elif ' use ' in rule:
                    product_class, nutrients = rule.split(' use ')
                    self.meal_nutrient[product_class[len('For '):]] = nutrients.split(', ')                    
                elif ' ignore ' in rule:
                    tag, nutrients = rule.split(' ignore ')
                    self.tag_nutrient[tag[len('For '):]] = nutrients.split(', ')
                elif ' prepareTime on ' in rule:
                    times, days = rule.split(' prepareTime on ')
                    for day in days.split(', '):
                        self.day_time[day] = times.split(', ')
        #         print(rule)
        # print(self.meal_tag)
        # print(self.class_nutrient)
        # print(self.meal_nutrient)
        # print(self.tag_nutrient)
        # print(self.day_time)

    """
     check and filter recipes if there are 
     rules for this meal type

     :param meal_type: 'Breakfast', 'Lunch', 'Dinner', etc
     :return: tuple of tags and nutrients
    """
    def filterByMeal(self, meal_type):
        tag = self.filterByTag(meal_type)
        nutr = self.filterByNutrient(meal_type)

        return tag, nutr
    """
     check and filter recipes if there are 
     rules for this meal type and tags,
     useful if user wants to eat for breakfast only 'breakfast' food

     :param meal_type: 'Breakfast', 'Lunch', 'Dinner', etc
     :return: None or tags of meals for this meal_type
    """
    def filterByTag(self, meal_type):
        if meal_type in self.meal_tag:
            # print("apply filter by tag from Rules")
            return self.meal_tag[meal_type]
        else:
            # print("there is no such rule in Rules to filter by tag")
            return None
    
    """
     check and filter recipes if there are 
     rules for this meal and nutrient types,
     useful if user wants to eat for breakfast only 'carb' food

     :param meal_type: 'Breakfast', 'Lunch', 'Dinner', etc
     :return: None or tags of meals for this meal_type
    """
    def filterByNutrient(self, meal_type):
        if meal_type in self.meal_nutrient:
            # print("Nutrients apply rule from Rules")
            return self.meal_nutrient[meal_type]
        else:
            # print("there is no such rule in Rules")
            return None

    """ 
    filter by day of week and its prepare time

    :param days: list of days
    :return: list of tuples (prepareTime, n concequent days)
     """
    def filterByDay(self, days):
        prepForDay = [self.day_time[k] if k in self.day_time else [] for k in days]
        groups = [(k, len(list(g))) for k, g in groupby(prepForDay)]
        return groups
    
    """ 
    from recipe food classes identify 
    to which nutrient type belongs recipe

    :param food_classes: list of food classes of ingridients in recipe
    :param tags: list of recipe tags
    :return: nutrient type
    """
    def identifyNutrient(self, food_classes, tags):
        nutrients = set()
        for food in food_classes:
            nutrients.update(self.class_nutrient[food])
        common_tags = set(tags).intersection(set(self.tag_nutrient))
        if common_tags:
            for tags in list(common_tags):
                for tag in self.tag_nutrient[tags]:
                    nutrients.discard(tag)
        return list(nutrients)
        