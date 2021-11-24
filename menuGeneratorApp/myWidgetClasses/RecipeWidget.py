from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import (
    ObjectProperty
)

from myWidgetClasses.buttonWithCross import ButtonWithCross

class RecipeWidget(MDBoxLayout):
    recipe = ObjectProperty()
    parentWidget = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # initValues are saved separately
        # so we can check if smth was changed
        if self.parentWidget:
            self.ids.recipeTitle.text = self.recipe.title
            # load new ingredients
            for ingredient in self.recipe.ingredients:
                self.ids.recipeIngredients.add_widget(ButtonWithCross(
                                            text=ingredient,
                                            parentId=self.ids.recipeIngredients))
                
            # set recipe prepare
            self.setChooseChip(self.ids.recipePrepareTime, self.recipe.prepareTime)
            
            # set if recipe can be used on two consecutive days
            self.ids.recipeRepeatDish.active = self.recipe.repeat

            # load new tags
            for tag in self.recipe.tags:
                self.ids.recipeTags.add_widget(ButtonWithCross(
                                            text=tag,
                                            parentId=self.ids.recipeTags))
            
            self.ids.recipeDescription.text = self.recipe.description

    '''Check chip for prepareTime

    :param id: widget id, container of chips
    :param value: text of the chip;
    '''
    def setChooseChip(self, id, value):
        chips = id.children
        for chip in chips:
            if chip.text==value:
                chip.state = 'down'

    '''Save all recipe info 

    :return: Bool if recipe can be saved
    '''    
    def saveRecipe(self):
        # form recipe data
        if self.ids.recipeTitle.text=='':
            self.ids.recipeTitle.error = True
            self.ids.recipeTitle.focus = True
            return False
        else:
            self.recipe.title = self.ids.recipeTitle.text
            self.recipe.img = self.ids.recipeImg.source
            self.recipe.ingredients = []
            for ingredient in self.ids.recipeIngredients.children:
                self.recipe.ingredients.append(ingredient.text)
            self.recipe.prepareTime = "short"
            for prepareTime in self.ids.recipePrepareTime.children:
                if prepareTime.state=='down':
                    self.recipe.prepareTime = prepareTime.text
            self.recipe.tags = []
            for tag in self.ids.recipeTags.children:
                self.recipe.tags.append(tag.text)
            self.recipe.repeat = self.ids.recipeRepeatDish.active
            self.recipe.description = self.ids.recipeDescription.text
            return True