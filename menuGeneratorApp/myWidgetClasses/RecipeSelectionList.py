from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.selection import MDSelectionList

from kivy.properties import (
    BooleanProperty,
    StringProperty,
    ObjectProperty,
    ListProperty,
    DictProperty
)
class RecipeListItem(TwoLineAvatarIconListItem):
    text = StringProperty()
    secondary_text = StringProperty()
    img_source = StringProperty()
    recipe = ObjectProperty()

    '''redraw recipeWidget in the scrollview
    with new recipe info 

    :param parentWidget: a Widget in the scrollview
    :param newRecipe: new recipe info
    '''    
    def redrawRecipeListItem(self, newRecipe):
        self.text=f"{newRecipe}"
        self.img_source = newRecipe.img
        self.secondary_text=f"{', '.join(newRecipe.ingredients)}"
        self.recipe = newRecipe

class RecipeSelectionList(MDSelectionList):
    last_selected = BooleanProperty()
    tags = ListProperty()
    products = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    """ 
    add one recipe to the Recipe list scroll

    :param recipe: Recipe object
 
     """
    def addRecipeInList(self, recipe):
        list_item = RecipeListItem(
                        text=f"{recipe}",
                        secondary_text=f"{', '.join(recipe.ingredients)}",
                        recipe = recipe
                    )
        self.add_widget(list_item)