from copy import copy
from kivymd.uix import button
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.properties import (
    DictProperty,
    StringProperty,
    BooleanProperty,
    ListProperty
)
from kivy.metrics import sp, dp

from myWidgetClasses.customButtons import IconToggleButton, MyToggleButton, ButtonWithCross

"""
Class with all settings user can modify
"""
class MenuSettings(MDGridLayout):
    """ 
    timePeriod: time period to generate menu, day/week/month
    repeat: can recipes be repeated
    meals: meals to include in Menu
    changedRules: all changes user has made
    initValues: initial values
    
    """
    timePeriod = StringProperty()
    repeat = BooleanProperty(False)
    meals = DictProperty()
    tags = ListProperty()
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
            if str(chip.value) in self.meals:
                chip.state = 'down'

        # add new RulesWidget or load it with initital values
        if not 'settingsRules' in self.ids:
            rulesWidget = RulesWidget(initRules=self.initValues['rules'], meals = self.meals, tags=self.initValues['tags'])
            self.add_widget(rulesWidget)
            # add to self.ids
            self.ids['settingsRules'] = rulesWidget
        else:
            self.ids.settingsRules.setInitValues()

    """
    Update initial values if changes were saved

    """
    def updateInitValues(self):
        self.initValues['timePeriod'] = copy(self.timePeriod)
        self.initValues['repeat'] = copy(self.repeat)
        self.initValues['meals'] = copy(self.meals)
        if self.changedRules:
            for meal_rule in self.changedRules['meal_nutrient']:
                nutrients, id = self.changedRules['meal_nutrient'][meal_rule]
                self.initValues['rules']['meal_nutrient'][copy(meal_rule)] = (copy(nutrients), copy(id))
            for period in self.changedRules['time_days']:
                days, id = self.changedRules['time_days'][period]
                self.initValues['rules']['time_days'][copy(period)] = (copy(days), copy(id))
            for period in self.changedRules['meal_discard_day']:
                days, id = self.changedRules['meal_discard_day'][period]
                self.initValues['rules']['meal_discard_day'][copy(period)] = (copy(days), copy(id))
            for meal in self.changedRules['meal_tag']:
                tags, id = self.changedRules['meal_tag'][meal]
                self.initValues['rules']['meal_tag'][copy(meal)] = (copy(tags), copy(id))
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
        # update meals set in Rules 
        self.ids.settingsRules.ids.rulesDiscardMeal.content.filter = self.meals
        self.ids.settingsRules.ids.rulesDiscardMeal.content.setInitValues()
        self.ids.settingsRules.ids.rulesTagsMeal.content.filter = self.meals
        self.ids.settingsRules.ids.rulesTagsMeal.content.setInitValues()
        self.ids.settingsRules.ids.rulesMealNutrients.content.filter = self.meals
        self.ids.settingsRules.ids.rulesMealNutrients.content.setInitValues()

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

"""
    Class of rules
"""
class RulesWidget(MDGridLayout):
    """ 
    initRules: initial values
    rules: all changes user has made
    meals: meals to include in Menu
    
    """
    initRules = DictProperty(None)
    rules = DictProperty()
    meals = DictProperty()
    tags = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.setInitValues()

    """
    Set initital values
    """
    def setInitValues(self):
        # copy rules, so we can have different dicts for old and new values
        self.rules['meal_nutrient'] = {}
        for meal_rule in self.initRules['meal_nutrient']:
            nutrients, id = self.initRules['meal_nutrient'][meal_rule]
            self.rules['meal_nutrient'][copy(meal_rule)] = (copy(nutrients), copy(id))

        self.rules['time_days'] = {}
        for period in self.initRules['time_days']:
            days, id = self.initRules['time_days'][period]
            self.rules['time_days'][copy(period)] = (copy(days), copy(id))

        self.rules['meal_discard_day'] = {}
        for period in self.initRules['meal_discard_day']:
            days, id = self.initRules['meal_discard_day'][period]
            self.rules['meal_discard_day'][copy(period)] = (copy(days), copy(id))

        self.rules['meal_tag'] = {}
        for meal in self.initRules['meal_tag']:
            tags, id = self.initRules['meal_tag'][meal]
            self.rules['meal_tag'][copy(meal)] = (copy(tags), copy(id))
        
        self.clear_widgets()
        rulesMealNutrients = MDExpansionPanel(
                    content = RulesContent(rules=self.rules['meal_nutrient'], filter=self.meals),
                    panel_cls=MDExpansionPanelOneLine(
                        text="'Nutritions per meal' rules"
                    )
                )
        self.add_widget(rulesMealNutrients)        
        self.ids['rulesMealNutrients'] = rulesMealNutrients
        
        icons = {
            "short": "clock-time-one-outline",
            "medium": "clock-time-five-outline",
            "long": "clock-time-nine-outline"
        } 
        rulesTimePeriod = MDExpansionPanel(
                    content = RulesDayButtons(rules=self.rules['time_days'], group="rulesTimePeriod", icons=icons),
                    panel_cls=MDExpansionPanelOneLine(
                        text="'Prepare time per day' rules"
                    )
                )   
        self.add_widget(rulesTimePeriod)
        self.ids['rulesTimePeriod'] = rulesTimePeriod

        icons = {
            "Breakfast": "bowl-mix",
            "Brunch": "food-variant",
            "Lunch": "pasta",
            "Supper": "pot-steam",
            "Dinner": "noodles"
        }
        rulesDiscardMeal = MDExpansionPanel(
                    content = RulesDayButtons(rules=self.rules['meal_discard_day'], group="rulesDiscardMeal", icons=icons, filter=self.meals),
                    panel_cls=MDExpansionPanelOneLine(
                        text="'Discarded meal per day' rules"
                    )
                )

        self.add_widget(rulesDiscardMeal)
        self.ids['rulesDiscardMeal'] = rulesDiscardMeal

        rulesTagsMeal = MDExpansionPanel(
                    content = RulesTagsMeals(rules=self.rules['meal_tag'], filter=self.meals, allTags=self.tags),
                    panel_cls=MDExpansionPanelOneLine(
                        text="'Tags per meal' rules"
                    )
                )

        self.add_widget(rulesTagsMeal)
        self.ids['rulesTagsMeal'] = rulesTagsMeal

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
        changes['time_days'] = {}
        for period in self.initRules['time_days']:
            if self.initRules['time_days'][period] != self.rules['time_days'][period]:
                changes['time_days'][period] = self.rules['time_days'][period]
                hasChanged = True
        changes['meal_discard_day'] = {}
        for period in self.initRules['meal_discard_day']:
            if self.initRules['meal_discard_day'][period] != self.rules['meal_discard_day'][period]:
                changes['meal_discard_day'][period] = self.rules['meal_discard_day'][period]
                hasChanged = True
        changes['meal_tag'] = {}
        for period in self.initRules['meal_tag']:
            if self.initRules['meal_tag'][period] != self.rules['meal_tag'][period]:
                changes['meal_tag'][period] = self.rules['meal_tag'][period]
                hasChanged = True
        if hasChanged:
            return changes
        else:
            return False

"""
Class for nutritions per day rules in MDExpansionPanel

""" 
class RulesContent(MDGridLayout):
    """ 
    rules: all changes user has made
    filter: user sees in rules only 
            meals which are checked in settings.meals
    icons: icons of nutrients
    
    """
    rules = DictProperty()
    filter = DictProperty(None)
    icons = DictProperty({
        'low_carb': 'leaf',
        'high_carb': 'barley',
        'fat': 'peanut',
        'protein': 'fish',
        'free': 'shaker'})
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setInitValues()

    """
    Set initital values
    """
    def setInitValues(self):
        self.clear_widgets()
        if self.filter:
            rules = {x:self.rules[x] for x in self.rules if x in self.filter.values()}
        else:
            rules = self.rules
        for meal_rule in rules:
            self.add_widget(MDLabel(text=f"For {meal_rule} use:"))
            iconsStack = MDStackLayout(adaptive_height=True, spacing=dp(5))
            for nutrient in self.icons:
                button = IconToggleButton(icon=self.icons[nutrient])
                button.parentWidget=self
                nutrients, id = rules[meal_rule]
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

"""
Class for days per timePeriod/meal rules in MDExpansionPanel

"""                 
class RulesDayButtons(MDGridLayout):
    """ 
    rules: all changes user has made
    group: toggle group
    icons: icons of nutrients
    filter: user sees in 'discarded meal' rules only 
            meals which are checked in settings.meals
    
    """
    rules = DictProperty()
    group = StringProperty()
    icons = DictProperty()
    filter = DictProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setInitValues()

    """
    Set initital values
    """
    def setInitValues(self):
        self.ids.rulesToggleButtons.clear_widgets()
        if self.filter:
            icons = {x:self.icons[x] for x in self.icons if x in self.filter.values()}
        else:
            icons = self.icons
        for text in icons:
            button = MyToggleButton(text=text, icon=icons[text], group=self.group)
            button.bind(on_release=self.toggleToggleButton)
            self.ids.rulesToggleButtons.add_widget(button)
        # toggle first button
        if self.ids.rulesToggleButtons.children:
            self.ids.rulesToggleButtons.children[-1].state = "down"
            self.toggleToggleButton(self.ids.rulesToggleButtons.children[-1])

    """
    toggle timePeriod/meal button in rules,
    user see only days for pressed timePeriod/meal

    :param widget: button which was toggled
    """
    def toggleToggleButton(self, widget):
        buttons = self.ids.rulesDays.children            
        if widget.text in self.rules:
            days, id = self.rules[widget.text]
            for button in buttons:
                if button.value in days:
                    button.state = "down"
                else:
                    button.state = "normal"
        else:
            for button in buttons:
                button.state = "normal"       

    """
    toggle round day button in rules
    adds day to the corresponding rule

    :param button: button which was toggled
    """
    def toggleDay(self, button):
        selectedPeriod = self.ids.rulesToggleButtons.children[-1].text
        for period in self.ids.rulesToggleButtons.children:
            if period.state == "down":
                selectedPeriod = period.text
        if selectedPeriod not in self.rules:
                self.rules[selectedPeriod] = (set(), None)
        days, id = self.rules[selectedPeriod]
        if button.state == "down":
            days.add(button.value)
        else:
            days.remove(button.value)

class RulesTagsMeals(MDBoxLayout):
    rules = DictProperty()
    filter = DictProperty(None)
    allTags = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setInitValues()

    def setInitValues(self):
        self.clear_widgets()
        if self.filter:
            rules = {x:self.rules[x] for x in self.rules if x in self.filter.values()}
        else:
            rules = self.rules
        for meal in rules:
            tags, id = rules[meal]
            self.add_widget(RulesTagsMealsBox(meal=meal, tags=tags, allTags=self.allTags))

class RulesTagsMealsBox(MDBoxLayout):
    text = StringProperty()
    meal = StringProperty()
    tags = ListProperty()
    allTags = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setInitValues()

    def setInitValues(self):
        self.text = f"For {self.meal} serve only with these tags:"
        for tag in self.tags:
            self.ids.mealTags.add_widget(ButtonWithCross(
                                            text=tag,
                                            parentId=self.ids.mealTags))
    
    '''
    get tags that are not used,
    no need to show same tags

    :param currentTags: tags used in recipe
    '''
    def getUnusedTags(self, currentTags):
        return list(set(self.allTags) - set(currentTags))

    '''
    refresh dropdown items for tag search

    :param textField: tags text field
    :param recipeWidget: recipe Widget with recycle view
    '''
    def refresh(self, text, textField):
        def add_tag_item(tag):
            self.ids.rv.data.append(
                {
                    "viewclass": "OneLineListItem",
                    "text": tag,
                    "on_release": lambda x=tag: self.set_item(x, textField)
                }
            )

        if len(text) > 0:
            self.ids.rv.data = []
            currentTags = []
            for tag in self.ids.mealTags.children:
                currentTags.append(tag.text)
            for tag in self.getUnusedTags(currentTags):
                if text in tag:
                    add_tag_item(tag)            
        else:
            self.ids.rv.data = []
        if self.ids.rv.data:
            self.ids.rv.parent.height = dp(48)
            
        else:
            self.ids.rv.parent.height = 0
    
    '''
    add new tag to the tags stackLayout

    :param text__item: string text
    :param textField: tags text field
    :param recipeWidget: recipe Widget with recycle view
    '''
    def set_item(self, text__item, textField):
        text = ' '.join(text__item.split())
        if len(text):
            textField.focus = False
            textField.text = ''
            self.ids.rv.data = []
            self.ids.rv.parent.height = 0
            # add new tags to rules
            tags, id = self.parent.rules[self.meal]
            tags.add(text)
            button = ButtonWithCross(
                                    text=text,
                                    parentId=self.ids.mealTags)
            button.ids.lbl_ic.bind(on_release=self.removeRuleTags)
            self.ids.mealTags.add_widget(button)
            
    
    def removeRuleTags(self, button):
        tags, id = self.parent.rules[self.meal]
        tags.remove(button.parent.text)