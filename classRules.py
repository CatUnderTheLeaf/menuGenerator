""" 
A class that represent rules for generating menu

rules can be written in such patterns:
    "At breakfast serve only breakfast"
    (meal time                  Tags)    
    "Vegetable is carb and fiber"
    (type           nutrients)
    "For Breakfast use carb"
    (meal time    nutrient category)

 """

class Rules:
    """ 
    meal_tag: list of tags per meal
    class_nutrient: list of correspondence of food class to nutrient type
    meal_nutrient: list of nutrients per meal
     """

    meal_tag = {}
    class_nutrient = {}
    meal_nutrient = {}
    tag_nutrient = {}

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
                print(rule)
        print(self.meal_tag)
        print(self.class_nutrient)
        print(self.meal_nutrient)
        print(self.tag_nutrient)

    """
     check and filter recipes if there are 
     rules for this meal type and tags,
     useful if user wants to eat for breakfast only 'breakfast' food

     :param meal_type: 'Breakfast', 'Lunch', 'Dinner', etc
     :return: None or tags of meals for this meal_type
    """
    def filterByTag(self, meal_type):
        if meal_type in self.meal_tag:
            print("apply rule from Rules")
            return self.meal_tag[meal_type]
        else:
            print("there is no such rule in Rules")
            return None


        # for (meal, tag) in self.meal_tag:
        #     if meal == meal_type:
        #         print("apply rule from Rules")
        #         return tag
        #     else:
        #         print("there is no such rule in Rules")
        #         return None
    
    """
     check and filter recipes if there are 
     rules for this meal and nutrient types,
     useful if user wants to eat for breakfast only 'carb' food

     :param meal_type: 'Breakfast', 'Lunch', 'Dinner', etc
     :return: None or tags of meals for this meal_type
    """
    def filterByNutrient(self, meal_type):
        if meal_type in self.meal_nutrient:
            print("Nutrients apply rule from Rules")
            return self.meal_nutrient[meal_type]
        else:
            print("there is no such rule in Rules")
            return None

        # nutrient_list = []
        # for (meal, nutrient) in self.meal_nutrient:
        #     if meal == meal_type:
        #         # print("apply rule from Rules")
        #         nutrient_list.append(nutrient)
        #     # else:
        #     #     print("there is no such rule in Rules")
                
        # if not nutrient_list:
        #     return None
        # else:
        #     print("Nutrients apply rule from Rules")
        #     return nutrient_list

    """ 
    from recipe food classes identify 
    to which nutrient type belongs recipe

    :param food_classes: list of food classes of ingridients in recipe
    :param tags: list of recipe tags
    :return: nutrient type
    """
    def identifyNutrient(self, food_classes, tags):
        nutrients = []
        for food in food_classes:
            nutrients.append(self.class_nutrient[food])
            # for (food_class, nutrient) in self.class_nutrient:
            #     if food_class==food:
            #         nutrients.append(nutrient)
        
        return list(set(nutrients))
        