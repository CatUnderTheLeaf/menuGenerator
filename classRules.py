""" 
a class that represent rules for generating menu

rules - list of Rules

rules can be written in such patterns:
    "0 is breakfast"
    (meal number     meal time)
    "At breakfast serve only breakfast"
    (meal time                  Category)
    "Onion is vegetable"
    (product    type)
    "Vegetable is carb and fiber"
    (type           nutrients)
    "At breakfast serve only carbs"
    (meal time                nutrient category)

 """

class Rules:
    def __init__(self, rules):        
        self.rules = rules