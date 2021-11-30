from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.properties import (
    DictProperty,
    StringProperty,
    BooleanProperty,
    ObjectProperty
)
from kivy.metrics import sp, dp

from myWidgetClasses.customButtons import IconToggleButton

class MenuSettings(MDGridLayout):
    timePeriod = StringProperty()
    repeat = BooleanProperty(False)
    meals = DictProperty()
    initValues = DictProperty()
    rules = ObjectProperty()

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
        self.rules = self.initValues['rules']
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
                            font_size=sp(20)
                        ))

        self.ids.settingsRules.add_widget(MDExpansionPanel(
                    content = RulesContent(rules=self.rules.rules['meal_nutrient']),
                    panel_cls=MDExpansionPanelOneLine(
                        text="'Nutritions per meal' rules"
                    )
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

class RulesWidget(MDGridLayout):
    pass        

class RulesContent(MDGridLayout):
    rules = DictProperty()
    icons = DictProperty({
        'low_carb': 'leaf',
        'high_carb': 'barley',
        'fat': 'peanut',
        'protein': 'fish',
        'free': 'shaker'})
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for meal in self.rules:
            self.add_widget(MDLabel(text=f"For {meal} use:"))
            iconsStack = MDStackLayout(adaptive_height=True, spacing=dp(5))
            for icon in self.icons:
                button = IconToggleButton(icon=self.icons[icon])
                if icon in self.rules[meal]:
                    button.state = 'down'
                iconsStack.add_widget(button)
            self.add_widget(iconsStack)
 