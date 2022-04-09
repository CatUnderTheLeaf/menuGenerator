from datetime import date, timedelta
import os

from classes.classMenu import Menu
from classes.classRecipe import Recipe

from kivy.storage.jsonstore import JsonStore
# Create Menu object


db_path = os.path.join(os.path.dirname(__file__), 'db/menuUnqliteDB.db')

menu = Menu()

menu.connectDB(db_path)

# generate menu for n+1 days applying rules
n = 10
sdate = date.today()
edate = sdate + timedelta(days=n)
# meals = {"0": "Breakfast", "2": "Lunch", "4": "Dinner"}
meals = {'4': 'Dinner', '2': 'Lunch', '0': 'Breakfast', '1': 'Brunch', '3': 'Supper'}
# meals = {'0': 'Breakfast'}
menu.update_mpd(meals)

# from pathlib import Path
# products_table = menu.db.db.products
# products = {}
# for p in Path(os.path.join(os.path.dirname(__file__), 'products')).iterdir():
#     with p.open(encoding='cp1251') as f:
#         for line in f:
#             prod = {
#                 'food_class': p.name,
#                 'name': line.rsplit(' - ')[0].rstrip()
#             }
#             print(prod)
            # products_table.store(prod)
        




# menu.generateDailyMenu(sdate, edate)
# print(menu)
# genMenu = menu.toJson()
# menu.menu = {}
# menu.loadFromJson(genMenu)
# print(menu)
# rules = menu.db.db.rulesCollection
# arr = ['short prepareTime on Wednesday, Friday, Monday, Tuesday, Thursday', 'long prepareTime on Saturday, Sunday', 'At Breakfast serve only breakfast', 'For dough food ignore protein', 'cereals,grains,pasta,bread,vegan is high_carb', 'dried_beans is high_carb', 'fat,nuts is fat', 'fruits is high_carb', 'high_carb_veggies is high_carb', 'low_carb_veggies is low_carb', 'meat,fish,cheese,eggs is protein', 'dairy is low_carb, protein, fat', 'other_seasoning is free', 'For Breakfast use low_carb, high_carb, fat, free', 'For Lunch use low_carb, high_carb, protein, fat, free', 'For Dinner use protein, fat, free, low_carb', 'On Sunday discard Lunch', 'medium prepareTime on Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday', 'On discard Breakfast', 'On discard Brunch', 'On discard Supper', 'At Lunch serve only ', 'At Brunch serve only ', 'At Supper serve only ', 'At Dinner serve only ', 'For Brunch use low_carb, protein, high_carb, fat, free', 'For Supper use low_carb, protein, high_carb, fat, free', 'On discard Dinner']
# for a in rules:
    # newRule = {
    #     'rule': a
    # }
    # print(a)
    # rules.store(newRule)
    # arr.append(rule['rule'])
# print(arr)
# print(rules[2])
# rules[2] = {'rule': 'At Breakfast serve only завтрак'}
# rules[25] = {'rule': 'For Brunch use low_carb, protein, high_carb, fat, free'}
# rules.store({'rule': 'For ignoreProtein ignore protein'})
# rules.store({'rule': 'For ignoreHighCarb ignore high_carb'})
# rules.store({'rule': 'For ignoreLowCarb ignore low_carb'})
# rules.store({'rule': 'For ignoreFat ignore fat'})
# tags = menu.db.getTags()
# print(tags)
products = menu.db.db.products
# print(products[8])
# products[198] = {'food_class': 'cereals,grains,pasta,bread,vegan', 'name': 'Lavash'}
# products[168] = {'food_class': 'other_seasoning', 'name': 'Ketchup'}
# products[200] = {'food_class': 'meat,fish,cheese,eggs', 'name': 'Feta'}
# products[201] = {'food_class': 'low_carb_veggies', 'name': 'Algae'}


# products.store({'food_class': 'cereals,grains,pasta,bread,vegan', 'name': 'Coconut milk'})
# products.store({'food_class': 'other_seasoning', 'name': 'Turmeric'})
# products.store({'food_class': 'low_carb_veggies', 'name': 'Pickled cucumber'})
# products.store({'food_class': 'meat,fish,cheese,eggs', 'name': 'Salted herring'})
# products.store({'food_class': 'other_seasoning', 'name': 'Curry paste'})

    
# for rule in products:
    # if rule['name']=='Заправка для салата':
    #     products[rule['__id']] = {'food_class': rule['food_class'], 'name': 'Салатная заправка'}
    # if ' ' in rule['name']:
    #     st = rule['name'].split(' – ')
        # print(st)
    #     products[rule['__id']] = {'food_class': rule['food_class'], 'name': st[0]}
    # print(rule)
# dstpath = 'c:\my_projects\menuGenerator\menuGeneratorApp\img'
# dstpath = '/storage/img'
# dstpath = ''
# menu.db.db.updateRecipeImgPath(dstpath)







# import shutil
# srcpath = "C:/Users/stacy/Pictures/src"
# dstpath = "C:/Users/stacy/Pictures/dst"
# os.makedirs(dstpath, exist_ok=True)
# #tag each file to the source path to create the file path
# for file in os.listdir(srcpath):
#     srcfile = os.path.join(srcpath, file)
#     dstfile = os.path.join(dstpath, file)
#     shutil.move(srcfile, dstfile)
# os.rmdir(srcpath)


# !!!!!!!!!!! recipes from .yml to .db !!!!!!!!!!!!!!!!!!!!!!!!!!!
# import jsons
# settings_path = os.path.join(os.path.dirname(__file__), 'test2.json')
# store = JsonStore(settings_path)
# import yaml

# with open(os.path.join(os.path.dirname(__file__), "recipe_helpers", "test_english.yml"), 'r', encoding='cp1251') as stream:
#     data_loaded = yaml.safe_load(stream)
#     # print(data_loaded)
#     store.put('recipes', recipes=data_loaded)

# data_get = store.get('recipes')
# # print(data_get['recipes'])
# for r in data_get['recipes']:
#     h = jsons.load(r, Recipe)
#     menu.db.updateRecipe(h)
#     # print(h.food_class)

recipes = menu.db.db.recipesCollection
# recipes.drop()
for recipe in recipes:
#     print(recipe['__id'])
    print(recipe['title'])
    print(recipe['img'])
#     print(recipe['nutrients'])
#     print(recipe['food_class'])
#     print(recipe['tags'])
# menu.disconnectDB()



# -
#   title: 
#   description: >
    
#   img: no_image.png
#   prepareTime: short
#   repeat: false
#   tags: 
#   - завтрак
#   ingredients: