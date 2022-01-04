from datetime import date, timedelta
import os

from classes.classMenu import Menu

# Create Menu object

import yaml
with open(os.path.join(os.path.dirname(__file__), "app_settings.yml"), 'r') as stream:
    data_loaded = yaml.safe_load(stream)

db = data_loaded['DB_TYPE']
db_path = os.path.join(os.path.dirname(__file__), data_loaded['MENU_DB'])

menu = Menu()

menu.connectDB(db, db_path)

# generate menu for n+1 days applying rules
n = 10
sdate = date.today()
edate = sdate + timedelta(days=n)
meals = {"0": "Breakfast", "2": "Lunch", "4": "Dinner"}
menu.update_mpd(meals)

# menu.generateDailyMenu(sdate, edate)
# print(menu)
# rules = menu.db.db.rulesCollection
# for rule in rules:
#     print(rule)
# print(rules[1])
# rules[1] = {'rule': 'long prepareTime on Saturday, Sunday'}
# rules[13] = {'rule': 'For Breakfast use low_carb, high_carb, fat, free'}
# rules.store({'rule': 'For Supper use '})
# tags = menu.db.getTags()
# print(tags)
# products = menu.db.db.products
# products[0] = {'food_class': 'cereals,grains,pasta,bread,vegan', 'name': 'Cereals'}
    
# for rule in products:
    # if rule['food_class']=='cereals,grains,pasta,bread,vegan is high_carb':
        # products[rule['__id']] = {'food_class': 'cereals,grains,pasta,bread,vegan', 'name': rule['name']}
    # print(rule)
# dstpath = 'c:\my_projects\menuGenerator\menuGeneratorApp\img'
dstpath = '/storage/img'
dstpath = ''
# menu.db.db.updateRecipeImgPath(dstpath)
# recipes = menu.db.getRecipes()
recipes = menu.db.db.recipesCollection
for recipe in recipes:
    # menu.db.updateRecipe(recipe)
    print(recipe)
    # print(recipe.img)

# food_class = menu.db.identifyFoodClass(['Butter', 'Cheese', 'Sausage', 'Bread'])
# print(food_class)

menu.disconnectDB()

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