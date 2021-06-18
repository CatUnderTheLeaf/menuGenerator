# menuGenerator
A script to generate menu for n days.

There are many ways to generate a menu. One can try MIP (mixed-integer programming) or genetic algorithm.

When I plan a menu I have a bunch of rules:
- on Working days I don't have much time for cooking
- at weekend I can prepare dishes with long cooking time
- only at breakfast I eat 'breakfast' dishes
- at breakfast I eat low- or no-protein food
- at lunch I eat all
- at dinner I eat low- or no-carb food
- on Sunday at breakfast I eat thin or thick pancakes
- on Sunday at lunch I order food at the restaurant
- I can eat same main dish for several days with different sidedishes
- often I need to cook several sidedishes because not all family members eat the same

I have read a wonderful article ["Wizards and warriors"](https://ericlippert.com/2015/04/27/wizards-and-warriors-part-one/) and post on [Stackoverflow](https://stackoverflow.com/questions/55226942/python-how-to-to-make-set-of-rules-for-each-class-in-a-game). It helped me, because primarly I intended to make class hierarchies and express rules by writing code inside methods. In the article author described a system, where rules are data, not code, and finds it to be more flexible. So I decided to give it a try.

- Step ? (for future):
  - [ ] there are main dishes and multiple sidedishes

- Step 7:
  - [ ] I can eat one dish today at dinner and tomorrow at lunch   

- Step 6:
  - [x] add day names to generating
  - [x] add prepareTime to recipes
  - [x] add new rules for days of week
  - [x] on Sunday I eat pancakes and order food from cafe
  - [x] in recipe I want to use "Capsicum" along "Red Capsicum" or "Green Capsicum"
  - [x] Avocado is fat and low_carb
>   !!!-----------------generated menu----------------!!!
> 
> Wednesday:
> Breakfast - oat porridge  -  ['breakfast']
> Lunch - sandwich  -  ['dinner']
> Dinner - eggs with mayo  -  ['dinner']
> 
> Thursday:
> Breakfast - pancakes  -  ['breakfast', 'dough food']
> Lunch - salad  -  ['dinner']
> Dinner - meat balls  -  ['dinner']
> 
> Friday:
> Breakfast - pancakes  -  ['breakfast', 'dough food']
> Lunch - pizza  -  ['dinner']
> Dinner - omelette  -  ['dinner']
> 
> Saturday:
> Breakfast - pancakes  -  ['breakfast', 'dough food']
> Lunch - youghurt  -  ['breakfast']
> Dinner - eggs with mayo  -  ['dinner']
> 
> Sunday:
> Breakfast - pancakes  -  ['breakfast', 'dough food']
> Lunch - fruit salad  -  ['breakfast']
> Dinner - vienne steak  -  ['dinner']
> 
> Monday:
> Breakfast - fruit salad  -  ['breakfast']
> Lunch - pancakes  -  ['breakfast', 'dough food']
> Dinner - youghurt  -  ['breakfast']
> 
> Tuesday:
> Breakfast - musli  -  ['breakfast']
> Lunch - fruit salad  -  ['breakfast']
> Dinner - eggs with mayo  -  ['dinner']

- Step 5:
  - [x] load anew when there are changes in products lists
  - [x] make difference between low and high carbs
  - [x] rename category to tags
  - [x] why pancakes are not whole carb?

- Step 4:
  - [x] add products to recipes
  - [x] add rules for categorizing recipes (carbs, protein, fats)
  - [x] add new menu rules and generate menu
> Breakfast
> ['carb', 'fat', 'free']
> ['oat porridge', 'musli', 'fruit salad', 'oat porridge', 'fruit salad', 'musli', 'oat porridge']
> 
> Lunch
> ['carb', 'protein', 'fat', 'free']
> ['cake', 'ragout', 'ragout', 'cous-cous', 'fried fish', 'fried fish', 'salad']
> 
> Dinner
> ['protein', 'fat', 'free']
> ['vienne steak', 'eggs with mayo', 'omelette', 'meat balls', 'eggs with mayo', 'chicken wings', 'vienne steak']

- Step 3:
  - [x] rename class RecipeList to Menu
  - [x] add some rules for generating
  - [x] generate simple menu

- Step 2:
  - [x] add tags to the class (breakfast, dinner, etc.)
  - [x] add a RecipeList class with filter functions
  - [x] choose 7/14/21... items with criteria

- Step 1:
  - [x] create a Recipe class
  - [x] dump and load Recipe objects to a file

- Step 0:
  - [x] read menu items from file
  - [x] randomize
  - [x] choose 7/14/21... items
