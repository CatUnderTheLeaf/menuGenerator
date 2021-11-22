from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDIcon
from kivy.properties import (
    DictProperty,
    StringProperty,
    BooleanProperty
)
from kivy.metrics import sp

class MenuSettings(MDGridLayout):
    timePeriod = StringProperty()
    repeat = BooleanProperty(False)
    meals = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Check timePeriod chip as it was saved in settings
        chips = self.ids.timePeriod.children
        for chip in chips:
            if chip.text==self.timePeriod:
                chip.state = 'down'

        # Check meal chip as it was saved in settings
        meal_chips = self.ids.meals.children
        for chip in meal_chips:
            if chip.value in self.meals:
                chip.ids.box_check.add_widget(MDIcon(
                            icon="check",
                            size_hint=(None, None),
                            size=("26dp", "26dp"),
                            font_size=sp(20),
                        ))

    def updateMeals(self, chip):
        if chip.value in self.meals:
            del self.meals[chip.value]
        else:
            self.meals[chip.value] = chip.text