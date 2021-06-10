""" 
A class that represent rules for generating menu

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
    # list of correspondence of food class to nutrient type
    class_nutrient = []

    def __init__(self):
        print("load rules")
        with open('rules', 'r') as file:
            for line in file:
                rule = line.strip()
                if ' serve only ' in rule:
                    meal, cat = rule.split(' serve only ')
                    # remove prefix 'At'
                    self.meal_cat.append((meal[len('At '):], cat))                
                elif ' is ' in rule:
                    product_class, nutrient = rule.split(' is ')
                    if ' and ' in nutrient:
                        nutrient1, nutrient2 = nutrient.split(' and ')
                        self.class_nutrient.append((product_class, nutrient1))
                        self.class_nutrient.append((product_class, nutrient2))
                    else:
                        self.class_nutrient.append((product_class, nutrient))
                print(rule)
        print(self.meal_cat)
        print(self.class_nutrient)

    """
     check if there are rules for this meal type,
     useful if user wants to eat for breakfast only 'breakfast' food

     :param meal_type: 'Breakfast', 'Lunch', 'Dinner', etc
     :return: None or category of meals for this meal_type
    """
    def filterByCat(self, meal_type):
        for (meal, cat) in self.meal_cat:
            if meal == meal_type:
                print("apply rule from Rules")
                return cat
            else:
                print("there is no such rule in Rules")
                return None
    
    """ 
    from recipe food classes identify 
    to which nutrient type belongs recipe

    :param food_classes: list of food classes of ingridients in recipe
    :return: nutrient type
    """
    def identifyNutrient(self, food_classes):
        nutrients = []
        for food in food_classes:
            for (food_class, nutrient) in self.class_nutrient:
                if food_class==food:
                    nutrients.append(nutrient)
        return list(set(nutrients))
        