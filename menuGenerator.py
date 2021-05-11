import random

with open('menuItems') as f:
    menuList = [line.rstrip() for line in f]
print("------------menuList is read from file")
print(menuList)

# when you can't afford to have duplicates while sampling your data.
subList = random.sample(menuList, 7)
print("------------subList")
print(subList)
print("------------menuList is unchanged")
print(menuList)

# when you can afford to have duplicates in your sampling
choices = random.choices(menuList, k=7)
print("------------choices")
print(choices)
print("------------menuList after choices")
print(menuList)

random.shuffle(menuList)
print("------------menuList changes, shuffle in place")
print(menuList)

