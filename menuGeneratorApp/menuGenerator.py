from datetime import date, timedelta
import os

from classes.classMenu import Menu
from classes.classRecipe import Recipe

from kivy.storage.jsonstore import JsonStore
# Create Menu object

import yaml
with open(os.path.join(os.path.dirname(__file__), "app_settings.yml"), 'r') as stream:
    data_loaded = yaml.safe_load(stream)

db = data_loaded['DB_TYPE']
db_path = os.path.join(os.path.dirname(__file__), data_loaded['MENU_DB_RU'])

menu = Menu()

menu.connectDB(db, db_path)

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
rules = menu.db.db.rulesCollection
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
# rules.store({'rule': 'On discard Dinner'})
# tags = menu.db.getTags()
# print(tags)
products = menu.db.db.products
# products[0] = {'food_class': 'cereals,grains,pasta,bread,vegan', 'name': 'Cereals'}
    
for rule in products:
    # if rule['name']=='Заправка для салата':
    #     products[rule['__id']] = {'food_class': rule['food_class'], 'name': 'Салатная заправка'}
    # if ' ' in rule['name']:
    #     st = rule['name'].split(' – ')
        # print(st)
    #     products[rule['__id']] = {'food_class': rule['food_class'], 'name': st[0]}
    print(rule)
# dstpath = 'c:\my_projects\menuGenerator\menuGeneratorApp\img'
# dstpath = '/storage/img'
# dstpath = ''
# menu.db.db.updateRecipeImgPath(dstpath)

# import json
# # recipes = menu.db.getRecipes()


# # rec = store.get('recipes')
# rec = None
# with open(os.path.join(os.path.dirname(__file__), 'test.json'), encoding='cp1251') as f:
#     rec = json.load(f)
#     # print(rec)
# print(rec)
# for r in rec['recipes']:
#     h = jsons.load(r, Recipe)
#     print(h.title)

# jsonMenu = jsons.dump(rec)
# store.put('recipes', recipes=rec['recipes'])




# print(jsonMenu)
# recipes = menu.db.db.recipesCollection
# for recipe in recipes:
    # menu.db.updateRecipe(recipe)
    # print(recipe.ingredients)
    # print(recipe.img)
    # print(recipe['__id'])
    # print(recipe['description'])
# recipe = recipes[1]
# print("00000000000000")
# print(recipe['description'])
# newRecipe = recipe
# newRecipe['description'] = "\u0421\u043c\u0435\u0448\u0430\u0442\u044c \u0442\u0432\u043e\u0440\u043e\u0433 \u0441 \u044f\u0439\u0446\u043e\u043c, \u0441\u0430\u0445\u0430\u0440\u043e\u043c \u0438 \u0441\u043e\u043b\u044c\u044e.\n\u0412\u043c\u0435\u0448\u0430\u0442\u044c \u0442\u0443\u0434\u0430 \u043c\u0443\u043a\u0443 \u0434\u043e \u0441\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u044f \u043a\u0440\u0443\u0442\u043e\u0433\u043e \u0442\u0435\u0441\u0442\u0430.\n\u0420\u0430\u0437\u0434\u0435\u043b\u0438\u0442\u044c \u043d\u0430 \u043d\u0435\u0441\u043a\u043e\u043b\u044c\u043a\u043e \u043f\u043e\u0440\u0446\u0438\u0439 \u0438 \u043a\u0430\u0436\u0434\u0443\u044e \u0440\u0430\u0441\u043a\u0430\u0442\u0430\u0442\u044c \u0432 \u043a\u043e\u043b\u0431\u0430\u0441\u043a\u0443.\n\u041a\u0430\u0436\u0434\u0443\u044e \u043a\u043e\u043b\u0431\u0430\u0441\u043a\u0443 \u0440\u0430\u0437\u0440\u0435\u0437\u0430\u0442\u044c \u043d\u0430 \u043a\u0443\u0441\u043e\u0447\u043a\u0438.\n\u0412\u0430\u0440\u0438\u0442\u044c \u0432 \u043f\u043e\u0434\u0441\u043e\u043b\u0435\u043d\u043d\u043e\u043c \u043a\u0438\u043f\u044f\u0442\u043a\u0435 5-7 \u043c\u0438\u043d\u0443\u0442 \u043f\u043e\u0441\u043b\u0435 \u0432\u0441\u043f\u043b\u044b\u0432\u0430\u043d\u0438\u044f \u0438\u043b\u0438 \u0436\u0430\u0440\u0438\u0442\u044c/\u0432\u044b\u043f\u0435\u043a\u0430\u0442\u044c \u0434\u043e \u0440\u0443\u043c\u044f\u043d\u043e\u0439 \u043a\u043e\u0440\u043e\u0447\u043a\u0438."
# menu.db.db.recipesCollection.update(newRecipe['__id'], newRecipe)

# food_class = menu.db.identifyFoodClass(['Butter', 'Cheese', 'Sausage', 'Bread'])
# print(food_class)



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
import jsons
settings_path = os.path.join(os.path.dirname(__file__), 'test2.json')
store = JsonStore(settings_path)
import yaml

with open(os.path.join(os.path.dirname(__file__), "test.yml"), 'r', encoding='cp1251') as stream:
    data_loaded = yaml.safe_load(stream)
    # print(data_loaded)
    store.put('recipes', recipes=data_loaded)

data_get = store.get('recipes')
# print(data_get['recipes'])
for r in data_get['recipes']:
    h = jsons.load(r, Recipe)
    # menu.db.updateRecipe(h)
    # print(h.food_class)

recipes = menu.db.db.recipesCollection
for recipe in recipes:
    print(recipe['__id'])
    print(recipe['title'])
    print(recipe['description'])
    print(recipe['nutrients'])

menu.disconnectDB()



# -
#   title: 
#   description: >
    
#   img: no_image.png
#   prepareTime: short
#   repeat: false
#   tags: 
#   - завтрак
#   ingredients: