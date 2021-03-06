import calendar
import itertools
from datetime import date

""" 
A class that represent rules for generating menu

rules can be written in such patterns:
    "At Breakfast serve only breakfast"
    (meal time                  Tags)    
    "Vegetable is carb and fiber"
    (type           nutrients)
    "For Breakfast use carb"
    (meal time    nutrient category)
    "For dough food ignore protein"
    (Tag                 nutrient)
    "medium, long prepareTime on Sat, Sun"
    (preparation time          day of week)
    "On Sun discard Lunch"
    (day of week      meal time)

 """

class Rules:
    """ 
    :param db_rules: path to db file
     """
    def __init__(self, db_rules=''):
        # rules['meal_tag']: dict of tags per meal
        # rules['class_nutrient']: dict of correspondence of food class to nutrient type
        # rules['meal_nutrient']: dict of nutrients per meal
        # rules['tag_ignore_nutrient']: dict of ignored nutrients for tags
        # rules['day_time']: dict of preparation times for weekdays
        # rules['time_days']: dict of weekdays for preparation time
        # rules['day_discard_meal']: dict of discarded meals for specified weekdays
        # rules['meal_discard_day']: dict of days per discarded meal
          
        self.rules = {}
        self.rules['meal_tag'] = {}
        self.rules['class_nutrient'] = {}
        self.rules['meal_nutrient'] = {}
        self.rules['tag_ignore_nutrient'] = {}
        self.rules['day_time'] = {}
        self.rules['time_days'] = {}
        self.rules['day_discard_meal'] = {}
        self.rules['meal_discard_day'] = {}
        print("load rules")
        

        if not db_rules=='':            
            for line in db_rules:
                self.readRules(line)
        else:
            print('path to DB is empty')


    """ 
    Read a line and add it to rules dictionary

    :param line: string line from file
     """
    def readRules(self, line):
        rule, id = line
        # print(rule)
        if ' serve only ' in rule:
            meals, tags = rule.split(' serve only ')
            meals = meals[len('At '):].split(', ')
            serve_tags = set()
            if len(tags):
                serve_tags = set(tags.split(', '))
            for meal in meals:
                self.rules['meal_tag'][meal] = (serve_tags, id)
        elif ' is ' in rule:
            product_class, nutrients = rule.split(' is ')
            self.rules['class_nutrient'][product_class] = nutrients.split(', ')
        elif ' use ' in rule:
            product_class, nutrients = rule.split(' use ')
            meal_nutr = set()
            if len(nutrients):
                meal_nutr = set(nutrients.split(', '))
            self.rules['meal_nutrient'][product_class[len('For '):]] = (meal_nutr, id)
            
        elif ' ignore ' in rule:
            tag, nutrients = rule.split(' ignore ')
            self.rules['tag_ignore_nutrient'][tag[len('For '):]] = nutrients.split(', ')
        elif ' prepareTime on ' in rule:
            times, days = rule.split(' prepareTime on ')
            for day in days.split(', '):
                if day in self.rules['day_time']:
                    self.rules['day_time'][day].update(times.split(', '))
                else:
                    self.rules['day_time'][day] = set(times.split(', '))
            for time in times.split(', '):
                if time in self.rules['time_days']:
                    days, id = self.rules['time_days'][time]
                    days.update(days.split(', '))
                else:
                    self.rules['time_days'][time] = (set(days.split(', ')), id)
        elif ' discard ' in rule:
            days, meals = rule.split(' discard ')
            for day in days[len('On '):].split(', '):
                if day in self.rules['day_discard_meal']:
                    self.rules['day_discard_meal'][day].update(meals.split(', '))
                else:
                    self.rules['day_discard_meal'][day] = set(meals.split(', '))
            for meal in meals.split(', '):
                if meal in self.rules['meal_discard_day']:
                    days, id = self.rules['meal_discard_day'][meal]
                    days.update(days[len('On '):].split(', '))
                else:
                    disc_days = set()
                    if len(days[len('On '):]):
                        disc_days = set(days[len('On '):].split(', '))
                    self.rules['meal_discard_day'][meal] = (disc_days, id)
    
    """ 
    form rules to update in db

    :param rules: rules to update 

    :return: Dict of string rules for db 
     """
    def formRules(self, rules):
        updateRules = {}
        for cat in rules:
            if (cat == 'meal_nutrient'):
                for meal_rule in rules[cat]:
                    nutrients, id = rules[cat][meal_rule]
                    rule = 'For '+ meal_rule + ' use ' + ', '.join(nutrients)
                    updateRules[id] = rule
            if (cat == 'time_days'):
                for period in rules[cat]:
                    days, id = rules[cat][period]
                    rule = period + ' prepareTime on ' + ', '.join(days)
                    updateRules[id] = rule
            if (cat == 'meal_discard_day'):
                for meal in rules[cat]:
                    days, id = rules[cat][meal]
                    rule = 'On ' + ', '.join(days) + ' discard ' + meal
                    updateRules[id] = rule
            if (cat == 'meal_tag'):
                for meal in rules[cat]:
                    tags, id = rules[cat][meal]
                    rule = 'At ' + meal + ' serve only ' + ', '.join(tags)
                    updateRules[id] = rule
        return updateRules



    """
     check if there are 
     rules for this meal type

     :param meal_type: 'Breakfast', 'Lunch', 'Dinner', etc
     :return: tuple of tags and nutrients
    """
    def filterByMeal(self, meal_type):
        tag = self.filterByTag(meal_type)
        nutr = self.filterByNutrient(meal_type)

        return tag, nutr
    """
     check if there are 
     rules for these tags,
     useful if user wants to eat for breakfast only 'breakfast' food

     :param meal_type: 'Breakfast', 'Lunch', 'Dinner', etc
     :return: None or tags of meals for this meal_type
    """
    def filterByTag(self, meal_type):
        if meal_type in self.rules['meal_tag']:
            # print("apply filter by tag from Rules")
            tags, id = self.rules['meal_tag'][meal_type]
            return tags
        else:
            # print("there is no such rule in Rules to filter by tag")
            return None
    
    """
     check if there are 
     rules for this meal and nutrient types,
     useful if user wants to eat for breakfast only 'carb' food

     :param meal_type: 'Breakfast', 'Lunch', 'Dinner', etc
     :return: None or tags of meals for this meal_type
    """
    def filterByNutrient(self, meal_type):
        if meal_type in self.rules['meal_nutrient']:
            # print("Nutrients apply rule from Rules")
            nutrients, id = self.rules['meal_nutrient'][meal_type]
            return nutrients
        else:
            # print("there is no such rule in Rules")
            return None
    
    """ 
    get prepare time for days of week if there are such rules

    :return: array of all possible prepareTimes grouped by day of week
     """
    def getDayTimes(self):
        times_list = [self.rules['day_time'][key] if key in self.rules['day_time'] else None for key in calendar.day_name]
        times_groups = [k for k, g in itertools.groupby(times_list)]
        
        return times_groups

    """ 
    get prepare time for all dates

    :param days: list of dates
    :return: dict of prepareTimes per date
     """
    def getPrepTimes(self, dates):
        days = [day.strftime("%A") for day in dates]
        prepForDay = {date: self.rules['day_time'][day] if day in self.rules['day_time'] else None for (day,date) in zip(days, dates)}
        return prepForDay

    """ 
    check if there are 
    rules for this day of week and meal type

    :param days: list of days
    :return: tuples (date, meals)
    """
    def filterDiscardedMeals(self, days):
        indices = []
        for day in days:
            x = date.fromisoformat(day)
            if x.strftime("%A") in self.rules['day_discard_meal']:
                meals = self.rules['day_discard_meal'][x.strftime("%A")]
                indices.append((day, meals))
        return indices

    """ 
    from recipe food classes identify 
    to which nutrient type belongs recipe

    :param food_classes: list of food classes of ingredients in recipe
    :param tags: list of recipe tags
    :return: nutrient type
    """
    def identifyNutrient(self, food_classes, tags):
        nutrients = set()
        for food in food_classes:
            nutrients.update(self.rules['class_nutrient'][food])
        common_tags = set(tags).intersection(set(self.rules['tag_ignore_nutrient']))
        if common_tags:
            for tags in list(common_tags):
                for tag in self.rules['tag_ignore_nutrient'][tags]:
                    nutrients.discard(tag)
        return list(nutrients)
        