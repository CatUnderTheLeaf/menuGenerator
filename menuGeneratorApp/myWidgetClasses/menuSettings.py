from copy import copy
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.properties import (
    DictProperty,
    StringProperty,
    BooleanProperty
)
from kivy.metrics import sp, dp

from myWidgetClasses.customButtons import IconToggleButton

class MenuSettings(MDGridLayout):
    timePeriod = StringProperty()
    repeat = BooleanProperty(False)
    meals = DictProperty()
    changedRules = DictProperty(None)
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
                            font_size=sp(20)
                        ))

        if not 'settingsRules' in self.ids:
            rulesWidget = RulesWidget(initRules=self.initValues['rules'])
            self.add_widget(rulesWidget)
            # add to self.ids
            self.ids['settingsRules'] = rulesWidget
        else:
            self.ids.settingsRules.setInitValues()

    """
    Update initial values if changes were saved

    :param timePeriod: str
    :param repeatDishes: Bool
    :param meals: Dict 
    """
    def updateInitValues(self):
        self.initValues['timePeriod'] = copy(self.timePeriod)
        self.initValues['repeat'] = copy(self.repeat)
        self.initValues['meals'] = copy(self.meals)
        if self.changedRules:
            for meal_rule in self.changedRules['meal_nutrient']:
                nutrients, id = self.changedRules['meal_nutrient'][meal_rule]
                self.initValues['rules']['meal_nutrient'][copy(meal_rule)] = (copy(nutrients), copy(id))
            self.changedRules = {}
            

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
            or (self.meals != self.initValues['meals'])
            or (self.rulesHasChanged()))

    """
    Check if rules were changed

    :return: Bool
    """
    def rulesHasChanged(self):
        if self.ids.settingsRules.hasChanged():
            self.changedRules = self.ids.settingsRules.hasChanged()
            return True
        else:
            return False

class RulesWidget(MDGridLayout):
    initRules = DictProperty(None)
    rules = DictProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.setInitValues()

    """
    Set initital values
    """
    def setInitValues(self):
        self.rules['meal_nutrient'] = {}
        for meal_rule in self.initRules['meal_nutrient']:
            nutrients, id = self.initRules['meal_nutrient'][meal_rule]
            self.rules['meal_nutrient'][copy(meal_rule)] = (copy(nutrients), copy(id))
        
        self.clear_widgets()
        self.add_widget(MDExpansionPanel(
                    content = RulesContent(rules=self.rules['meal_nutrient']),
                    panel_cls=MDExpansionPanelOneLine(
                        text="'Nutritions per meal' rules"
                    )
                ))

    """
    Check if rules were changed

    :return: Bool
    """            
    def hasChanged(self):
        hasChanged = False
        changes = {}
        changes['meal_nutrient'] = {}
        for meal_rule in self.initRules['meal_nutrient']:
            if self.initRules['meal_nutrient'][meal_rule] != self.rules['meal_nutrient'][meal_rule]:
                changes['meal_nutrient'][meal_rule] = self.rules['meal_nutrient'][meal_rule]
                hasChanged = True
        if hasChanged:
            return changes
        else:
            return False

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
        for meal_rule in self.rules:
            self.add_widget(MDLabel(text=f"For {meal_rule} use:"))
            iconsStack = MDStackLayout(adaptive_height=True, spacing=dp(5))
            for nutrient in self.icons:
                button = IconToggleButton(icon=self.icons[nutrient])
                button.parentWidget=self
                nutrients, id = self.rules[meal_rule]
                button.value={id: nutrient}                
                if nutrient in nutrients:
                    button.state = 'down'
                iconsStack.add_widget(button)
            self.add_widget(iconsStack)
    
        """
    Update rules dictionary on icon-click

    :param chip: meals MDChip
    """
    def updateNutrientRules(self, value):
        for meal_rule in self.rules:
            nutrients, id = self.rules[meal_rule]
            for rule_id in value:
                if id==rule_id:
                    if value[rule_id] in nutrients:
                        nutrients.remove(value[rule_id])
                    else:
                        nutrients.add(value[rule_id])       