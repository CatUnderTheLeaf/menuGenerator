from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.label import MDIcon
from kivy.properties import (
    ListProperty,
    ObjectProperty
)
from kivy.metrics import sp

from myWidgetClasses.customButtons import ButtonWithCross, MyChip

class IngredientsExpansionPanel(MDExpansionPanel):
    products = ListProperty()
    ingredientWidget = ObjectProperty()
    
    def on_open(self):
        if len(self.content.ids.chooseIngredients.children)<1:
            ingredients = []
            for button_with_cross in self.ingredientWidget.children:
                ingredients.append(button_with_cross.text)
            for product in self.products:
                chip = MyChip(text=product)
                chip.bind(on_release=self.markIngredient)
                if product in ingredients:
                    chip.active = True
                self.content.ids.chooseIngredients.add_widget(chip)
    
    def markIngredient(self, instance_chip):
        if instance_chip.active:
            self.ingredientWidget.add_widget(ButtonWithCross(
                                            text=instance_chip.text,
                                            parentId=self.ingredientWidget))
        else:
            for button_with_cross in self.ingredientWidget.children:
                if button_with_cross.text==instance_chip.text:
                    self.ingredientWidget.remove_widget(button_with_cross)
        