import pickle
from classMenu import Menu

#-------------helper code 
# with open('menuItems') as f:
#     menuList = [line.rstrip() for line in f]
# print("------------menuList is read from file")
# print(menuList)
# # add recipe objects to a list
# recipeList = []
# for item in menuList:
#     new_recipe = Recipe(title=item)
#     recipeList.append(new_recipe)
# dump list in a file
# with open('recipe.list', 'wb') as file:
#   pickle.dump(recipeList, file)
# with open('category') as f:
#     cats = [line.rstrip() for line in f]
# print("------------cat is read from file")
# print(cats)
#-------------end of helper code 


# read from file
with open('recipe.list', 'rb') as file:
    recipeList = Menu(pickle.load(file))

print("------------from Menu object")
for recipe in recipeList.list:
    print(recipe)

# when you can't afford to have duplicates while sampling your data.
print(recipeList)
subList = recipeList.sampleN(3)
print("------------subList")
print(subList)

# when you can afford to have duplicates in your sampling
choices = recipeList.choicesN(3)
print("------------choices")
print(choices)

# sample with category, eg "breakfast"
subList = recipeList.sampleN(3, "breakfast")
subList = recipeList.sampleN(3, "dinner")
print("------------subList with filter")
print(subList)