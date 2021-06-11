""" 
A class that represent rules for generating menu

rules can be written in such patterns:
    "At breakfast serve only breakfast"
    (meal time                  Category)    
    "Vegetable is carb and fiber"
    (type           nutrients)
    "For Breakfast use carb"
    (meal time    nutrient category)

 """

class Rules:
    """ 
    meal_cat: list of categories per meal
    class_nutrient: list of correspondence of food class to nutrient type
    meal_nutrient: list of nutrients per meal
     """

    meal_cat = []
    class_nutrient = []
    meal_nutrient = []

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
                    product_class, nutrients = rule.split(' is ')
                    if ' and ' in nutrients:
                        nutrients_list = nutrients.split(' and ')
                        for nutrient in nutrients_list:
                            self.class_nutrient.append((product_class, nutrient))  
                    else:
                        self.class_nutrient.append((product_class, nutrients))
                elif ' use ' in rule:
                    product_class, nutrients = rule.split(' use ')
                    product_class = product_class[len('For '):]
                    if ' and ' in nutrients:
                        nutrients_list = nutrients.split(' and ')
                        for nutrient in nutrients_list:
                            self.meal_nutrient.append((product_class, nutrient))                       
                    else:
                        self.meal_nutrient.append((product_class, nutrients))
                print(rule)
        print(self.meal_cat)
        print(self.class_nutrient)
        print(self.meal_nutrient)

    """
     check and filter recipes if there are 
     rules for this meal type and category,
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
     check and filter recipes if there are 
     rules for this meal and nutrient types,
     useful if user wants to eat for breakfast only 'carb' food

     :param meal_type: 'Breakfast', 'Lunch', 'Dinner', etc
     :return: None or category of meals for this meal_type
    """
    def filterByNutrient(self, meal_type):
        nutrient_list = []
        for (meal, nutrient) in self.meal_nutrient:
            if meal == meal_type:
                # print("apply rule from Rules")
                nutrient_list.append(nutrient)
            # else:
            #     print("there is no such rule in Rules")
                
        if not nutrient_list:
            return None
        else:
            print("Nutrients apply rule from Rules")
            return nutrient_list

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
        