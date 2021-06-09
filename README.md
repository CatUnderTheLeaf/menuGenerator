# menuGenerator
A simple script to generate weekly menu.

Primarly I thought it was a problem like generating a schedule. To solve such problem one can use MIP (mixed-integer programming) or genetic algorithm. But now I think it is not the same problem. In all schedule use cases classes, tasks, nurses, wtv are a fixed number and not so big. I mean it is similar to organizing your stuff in a wardrobe: you have some things and you should put it in a wardrobe without falling out, minimizing space or dividing by theme; all things are there, maybe more on one shelf and less on the other. The problem of generating menu I can compare with filling your wardrobe: from all variety of things in the world you need to select only that things that suit your style, weather or wallet; no need to buy all because you wardrobe will not fit them. For me it is more like permutation vs combination.

I decided to have some set of rules for generating menu. There are python [knowledge bases or expert systems](https://stackoverflow.com/questions/53421492/python-rule-based-engine). Article ["Wizards and warriors"](https://ericlippert.com/2015/04/27/wizards-and-warriors-part-one/) and post on [Stackoverflow](https://stackoverflow.com/questions/55226942/python-how-to-to-make-set-of-rules-for-each-class-in-a-game) inspired me. I will try to make some rules DB and use DSL to retrieve them.
- Step 4:
  - add products to recipes
  - add rules for categorizing recipes (carbs, protein, fats)
  - add new menu rules and generate menu

- Step 3:
  - rename class RecipeList to Menu
  - add some rules for generating
  - generate simple menu

- Step 2:
  - add category to the class (breakfast, dinner, etc.)
  - add a RecipeList class with filter functions
  - choose 7/14/21... items with criteria

- Step 1:
  - create a Recipe class
  - dump and load Recipe objects to a file

- Step 0:
  - read menu items from file
  - randomize
  - choose 7/14/21... items
