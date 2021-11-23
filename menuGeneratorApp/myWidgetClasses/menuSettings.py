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
    initValues = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # initValues are saved separately
        # so we can check if smth was changed
        self.setInitialValues()                

    """
    Set initital values
    """
    def setInitialValues(self):
        self.timePeriod = self.initValues['timePeriod']
        self.repeat = self.initValues['repeat']
        self.meals = self.initValues['meals']
        # Check timePeriod chip as it was saved in settings
        chips = self.ids.timePeriod.children
        for chip in chips:
            if chip.text==self.timePeriod:
                chip.state = 'down'

        # Check meal chip as it was saved in settings
        meal_chips = self.ids.meals.children
        for chip in meal_chips:
            if str(chip.value) in self.meals and not len(chip.ids.box_check.children):
                chip.ids.box_check.add_widget(MDIcon(
                            icon="check",
                            size_hint=(None, None),
                            size=("26dp", "26dp"),
                            font_size=sp(20),
                        ))

    """
    Update initial values if changes were saved

    :param timePeriod: str
    :param repeatDishes: Bool
    :param meals: Dict 
    """
    def updateInitValues(self, timePeriod, repeat, meals):
        self.initValues['timePeriod'] = timePeriod
        self.initValues['repeat'] = repeat
        self.initValues['meals'] = meals

    """
    Update meals dictionary on chip-click

    :param chip: meals MDChip
    """
    def updateMeals(self, chip):
        if chip.value in self.meals:
            del self.meals[chip.value]
        else:
            self.meals[chip.value] = chip.text

    """
    Check if values were changed

    :return: Bool
    """
    def hasChanged(self):
        return ((self.timePeriod != self.initValues['timePeriod']) 
            or (self.repeat != self.initValues['repeat']) 
            or (self.meals != self.initValues['meals']))
        