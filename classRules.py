""" 
a class that represent rules for generating menu

rules - list of Rules

rules can be written in such patterns:
    "At breakfast serve only breakfast"
    (meal time                  Category)    
    "Vegetable is carb and fiber"
    (type           nutrients)
    "At breakfast serve only carbs"
    (meal time                nutrient category)

 """

class Rules:
    # list of categories per meal
    meal_cat = []

    def __init__(self):
        print("load rules")
        with open('rules', 'r') as file:
            # rules = [line.strip() for line in file]
            for line in file:
                rule = line.strip()
                if ' serve only ' in rule:
                    meal, cat = rule.split(' serve only ')
                    # remove prefix 'At'
                    self.meal_cat.append((meal[len('At '):], cat))
                print(rule)
        print(self.meal_cat)

    def filterByCat(self, meal_type):
        for (meal, cat) in self.meal_cat:
            if meal == meal_type:
                print("apply rule from Rules")
                return cat
            else:
                print("there is no such rule in Rules")
                return None
        