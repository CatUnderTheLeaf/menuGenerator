import pickle
from classMenu import Menu

#-------------helper code 
# with open('menuItems') as f:
#     menuList = [line.rstrip() for line in f]
# print("------------menuList is read from file")
# print(menuList)
# # add recipe objects to a list
# menu = []
# for item in menuList:
#     new_recipe = Recipe(title=item)
#     menu.append(new_recipe)
# dump list in a file
# with open('recipe.list', 'wb') as file:
#   pickle.dump(menu, file)
# with open('category') as f:
#     cats = [line.rstrip() for line in f]
# print("------------cat is read from file")
# print(cats)

# with open('recipe.list', 'rb') as file:
#     recipeList = pickle.load(file)
# with open('ingridients') as f:
#     ingridients = [line.rstrip() for line in f]
#     print(ingridients)
# for (recipe, ingr) in zip(recipeList, ingridients):
#     recipe.ingridients = ingr
    # print(recipe.title)
    # print(recipe.category)
    # print(recipe.ingridients)
# with open('recipe.list', 'wb') as file:
#     pickle.dump(recipeList, file)
# print(recipeList[0].ingridients)
# make products dictionary
# from pathlib import Path

# products = {}
# for p in Path(r'products').iterdir():
#     with p.open() as f:
#         menuList = [line.rsplit(' - ')[0].rstrip() for line in f]
#         products[p.name] = menuList
# print(products)
# # dump products dict in a file
# with open('class_products.list', 'wb') as file:
#   pickle.dump(products, file)

#-------------end of helper code 






# Create Menu object
menu = Menu()

# generate menu for n days applying rules
menu.generateDailyMenu(7)


