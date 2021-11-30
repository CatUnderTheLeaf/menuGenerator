from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.label import MDIcon
from kivymd.uix.chip import MDChip
from kivy.properties import (
    ListProperty,
    ObjectProperty
)
from kivy.metrics import sp

from myWidgetClasses.customButtons import ButtonWithCross

class IngredientsExpansionPanel(MDExpansionPanel):
    products = ListProperty()
    ingredientWidget = ObjectProperty()
    
    def on_open(self):
        if len(self.content.ids.chooseIngredients.children)<1:
            ingredients = []
            for button_with_cross in self.ingredientWidget.children:
                ingredients.append(button_with_cross.text)
            for product in self.products:
                chip = MDChip(text=product, check=True, icon='')
                chip.bind(on_release=self.markIngredient)
                if product in ingredients and not len(chip.ids.box_check.children):
                    chip.ids.box_check.add_widget(MDIcon(
                                icon="check",
                                size_hint=(None, None),
                                size=("26dp", "26dp"),
                                font_size=sp(20),
                            ))
                self.content.ids.chooseIngredients.add_widget(chip)
    
    def markIngredient(self, instance_chip):
        if not len(instance_chip.ids.box_check.children):
            self.ingredientWidget.add_widget(ButtonWithCross(
                                            text=instance_chip.text,
                                            parentId=self.ingredientWidget))
        else:
            for button_with_cross in self.ingredientWidget.children:
                if button_with_cross.text==instance_chip.text:
                    self.ingredientWidget.remove_widget(button_with_cross)
        