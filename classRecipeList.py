import random
""" 
a class that represent a list of recipes,
has a bunch of useful filtering and randomizing functions

list - list of Recipe objects
 """

class RecipeList:
    def __init__(self, list):        
        self.list = list

    def __repr__(self):
       return repr(self.list)

    def __str__(self):
       return str(self.list)
    
    # shuffle recipe list
    def shuffle(self):
        random.shuffle(self.list)
        return self.list

    # when you can't afford to have duplicates while sampling your data.
    def sampleN(self, n=1, cat=None):
        sublist = self.list
        if cat is not None:
            print("filter with category")
            sublist = self.filterCategory(cat)
        newList = random.sample(sublist, n)
        return newList

    # when you can afford to have duplicates in your sampling
    def choicesN(self, n=1, cat=None):
        sublist = self.list
        if cat is not None:
            print("filter with category")
            sublist = self.filterCategory(cat)
        newList = random.choices(sublist, k=n)
        return newList

    def filterCategory(self, cat):
        sublist = [x for x in self.list if x.category==cat]
        return sublist

        
