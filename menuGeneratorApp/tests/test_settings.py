from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.button import MDFillRoundFlatIconButton, BaseButton
from kivy.uix.behaviors import ToggleButtonBehavior
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.metrics import dp, sp
from kivymd.uix.behaviors import (
    CircularRippleBehavior,
)
from kivy.properties import (
    DictProperty,
    ColorProperty,
    StringProperty,
    ObjectProperty,
    BooleanProperty,
    ListProperty
)
from kivymd.uix.list import MDList, OneLineListItem

KV = '''

<MyToggleButton>:
    background_down: app.theme_cls.primary_dark

MDScreen:

    MDBoxLayout:
        orientation: "vertical"
        
        MDNavigationLayout:

            ScreenManager:
                id: screen_manager
                
                MDScreen:
                    name: "scr2"

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(5)

                        MDToolbar:
                            id: settings
                            pos_hint: {"top": 1}
                            title: "Settings"
                            left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

                        ScrollView:
                            
                            MDGridLayout:
                                padding: dp(20)
                                spacing: dp(10)
                                cols: 1
                                adaptive_height: True
                                
                                MDLabel:
                                    text: "Time period"
                                    theme_text_color: "Custom"
                                    text_color: app.theme_cls.primary_dark
                                    font_style: 'H6'
                                    
                                Widget:
                                    size_hint_y: None
                                    height: dp(5)
                                
                                MDStackLayout:
                                    adaptive_height: True
                                    spacing: dp(5)
                                    id: timePeriod

                                    MyToggleButton:
                                        text: "day"
                                        icon: "calendar-today"
                                        group: "timePeriod"
                                        on_release: app.set_n_days(self.text)
                                    
                                    MyToggleButton:
                                        text: "week"
                                        icon: "calendar-week"
                                        group: "timePeriod"
                                        on_release: app.set_n_days(self.text)
                                    
                                    MyToggleButton:
                                        text: "month"
                                        icon: "calendar-month"
                                        group: "timePeriod"
                                        on_release: app.set_n_days(self.text)
                                                                    
                                MDSeparator:
                                
                                MDGridLayout:
                                    cols: 2
                                    adaptive_height: True                            

                                    MDLabel:
                                        text: "Repeat dishes"
                                        theme_text_color: "Custom"
                                        text_color: app.theme_cls.primary_dark
                                        font_style: 'H6'

                                    MDSwitch:
                                        id: repeatDishes
                                        on_active: app.on_repeat_switch(*args)                                    
                                
                                MDSeparator:
                                
                                Widget:
                                    size_hint_y: None
                                    height: dp(5)
                            
                                MDLabel:
                                    text: "Meals"
                                    theme_text_color: "Custom"
                                    text_color: app.theme_cls.primary_dark
                                    font_style: 'H6'

                                Widget:
                                    size_hint_y: None
                                    height: dp(5)

                                MDGridLayout:
                                    cols: 1
                                    adaptive_height: True
                                    spacing: dp(5)
                                    id: meals                                

                                    MDChip:
                                        text: "Breakfast"                                    
                                        icon: "bowl-mix"
                                        value: 0
                                        on_release: app.updateMeals(self)
                                        check: True
                                        state: "down"

                                    MDChip:
                                        text: "Brunch"
                                        icon: "food-variant"
                                        value: 1
                                        on_release: app.updateMeals(self)
                                        check: True

                                    MDChip:
                                        text: "Lunch"
                                        icon: "pasta"
                                        value: 2
                                        on_release: app.updateMeals(self)
                                        check: True
                                        state: "down"
                                    
                                    MDChip:
                                        text: "Supper"
                                        icon: "pot-steam"
                                        value: 3
                                        on_release: app.updateMeals(self)
                                        check: True

                                    MDChip:
                                        text: "Dinner"
                                        icon: "noodles"
                                        value: 4
                                        on_release: app.updateMeals(self)
                                        check: True  
                                        state: "down"                              
                                
                                MDSeparator:
                                
                                Widget:
                                    size_hint_y: None
                                    height: dp(5)
                            
                                MDLabel:
                                    text: "Rules"
                                    theme_text_color: "Custom"
                                    text_color: app.theme_cls.primary_dark
                                    font_style: 'H6'

                                Widget:
                                    size_hint_y: None
                                    height: dp(5)

                                RulesWidget:
                                    id: settingsRules

<RulesDayButtons>    
    cols: 1
    orientation: 'tb-lr'
    adaptive_height: True
    spacing: dp(5)
    padding: 0, dp(20), 0, 0
    width: Window.width

    MDStackLayout:
        adaptive_height: True
        id: rulesToggleButtons
        
    MDStackLayout:
        adaptive_height: True
        id: rulesDays

        TextRoundButton:            
            value: "Monday"
            on_release: root.toggleDay(self)
        TextRoundButton:
            value: "Tuesday"
            on_release: root.toggleDay(self)
        TextRoundButton:
            value: "Wednesday"
            on_release: root.toggleDay(self)
        TextRoundButton:
            value: "Thursday"
            on_release: root.toggleDay(self)
        TextRoundButton:
            value: "Friday"
            on_release: root.toggleDay(self)
        TextRoundButton:
            value: "Saturday"
            on_release: root.toggleDay(self)
        TextRoundButton:
            value: "Sunday"
            on_release: root.toggleDay(self)


<TextRoundButton>
    background_down: app.theme_cls.primary_dark
    background_normal: app.theme_cls.primary_color
    theme_text_color: "Custom"       
    text_color: 1, 1, 1, 1     
    md_bg_color: self.background_normal
    user_font_size: '24sp'
    value: ""
    text: self.value[:2]

    canvas:
        Clear
        Color:
            rgba: root.md_bg_color
        Ellipse:
            size: self.size
            pos: self.pos
            source: self.source if hasattr(self, "source") else ""

    size: "48dp", "48dp"
    padding: (0, 0, 0, 0)

    MDLabel:
        adaptive_size: True
        -text_size: None, None
        pos_hint: {"center_y": .5}
        id: label
        text: root.text
        size_hint_x: None
        width: self.texture_size[0]
        color: root.text_color if root.text_color else (root.theme_cls.text_color)
        markup: True

<RulesWidget>:
    cols: 1
    adaptive_height: True

<RulesTagsMeals>:
    orientation: 'vertical'
    adaptive_height: True
    padding: dp(15), dp(56), dp(15), dp(15)
    spacing: dp(15)
    width: Window.width    

<RulesTagsMealsBox>    
    orientation: 'vertical'
    adaptive_height: True
    spacing: dp(10)
    padding: 0, 0, 0, 0
    width: Window.width

    MDLabel:
        text: root.text

    MDStackLayout:
        adaptive_height: True
        id: mealTags
        height: 0
    
    MDBoxLayout:
        adaptive_height: True
        padding: dp(11), 0, 0, 0            

        ClickableTextFieldRound:
            id: click_text_field
            size_hint_x: None
            width: "200dp"
            hint_text: "Add new tag"

    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        height: 0
        width: Window.width

        RecycleView:
            id: rv
            key_viewclass: 'viewclass'
            key_size: 'height'            

            RecycleBoxLayout:
                default_size: dp(200), dp(48)
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
    
    MDSeparator:
    

<ClickableTextFieldRound>:
    size_hint_y: None
    height: text_field.height

    MDTextFieldRound:
        id: text_field
        hint_text: root.hint_text
        text: root.text
        color_active: app.theme_cls.primary_light
        on_text: if self.focus: root.parent.parent.refresh(self.text, self)

    MDIconButton:
        icon: "plus"
        ripple_scale: .5
        pos_hint: {"center_y": .5}
        pos: text_field.width - self.width + dp(8), 0
        on_release: root.parent.parent.set_item(text_field.text, text_field)

<ButtonWithCross>:  
    id: box
    size_hint: None,  None
    height: "26dp"
    padding: "8dp", 0, 0, 0
    width:
        self.minimum_width - (dp(10) if DEVICE_TYPE == "desktop" else dp(20)) \
        if root.icon != 'close' else self.minimum_width

    canvas:
        Color:
            rgba: root.theme_cls.primary_color if not root.color else root.color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: root.radius
    
    MDLabel:
        adaptive_size: True
        -text_size: None, None
        pos_hint: {"center_y": .5}
        id: label
        text: root.text
        size_hint_x: None
        width: self.texture_size[0]
        color: root.text_color if root.text_color else (root.theme_cls.text_color)
        markup: True
    
    MDIconButton:
        id: lbl_ic
        icon: root.icon
        theme_text_color: "Custom"
        adaptive_size: True
        pos_hint: {"center_y": .5}
        on_release: root.removeCustomWidget(root.parentId, root)
'''

class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    focus = BooleanProperty()

class RulesDayButtons(MDGridLayout):
    rules = DictProperty()
    group = StringProperty()
    icons = DictProperty()
    filter = DictProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setInitValues()

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
        self.ids.rulesToggleButtons.children[-1].state = "down"
        self.toggleToggleButton(self.ids.rulesToggleButtons.children[-1])

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

class RulesTagsMealsBox(MDBoxLayout):
    text = StringProperty()
    tags = ListProperty()
    allTags = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setInitValues()

    def setInitValues(self):
        # self.ids.mealTags.clear_widgets()
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
        print(self.allTags)
        print(currentTags)
        print(list(set(self.allTags) - set(currentTags)))
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
        print(self.ids.rv.data)
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
            self.ids.mealTags.add_widget(ButtonWithCross(
                                                text=text,
                                                parentId=self.ids.mealTags))

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
            self.add_widget(RulesTagsMealsBox(text=f"For {meal} serve only with these tags:", tags=tags, allTags=self.allTags))
        
class ButtonWithCross(MDBoxLayout, ThemableBehavior):    
    color = ColorProperty(None)
    parentId = ObjectProperty()
    text = StringProperty()
    icon = StringProperty("close")
    text_color = ColorProperty(None)
    radius = ListProperty(
        [
            dp(12),
        ]
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    '''remove widget from its parent

    :param parentId: parent id of the Widget to remove
    :param instance: a Widget to remove;
    '''
    def removeCustomWidget(self, parentId, instance):
        parentId.remove_widget(instance)       

class RulesWidget(MDGridLayout):
    pass

class TextRoundButton(CircularRippleBehavior, BaseButton, ToggleButtonBehavior):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.bind(primary_palette=self.update_md_bg_color)
        Clock.schedule_once(self.set_size)
        Clock.schedule_once(self.set_text_color)
        self.on_md_bg_color(self, [0.0, 0.0, 0.0, 0.0])

    def set_size(self, interval):
        """
        Sets the custom icon size if the value of the `user_font_size`
        attribute is not zero. Otherwise, the icon size is set to `(48, 48)`.
        """

        self.width = (
            "48dp" if not self.user_font_size else dp(self.user_font_size + 23)
        )
        self.height = (
            "48dp" if not self.user_font_size else dp(self.user_font_size + 23)
        )

    def update_md_bg_color(self, instance, value):
        if self.md_bg_color != [0.0, 0.0, 0.0, 0.0]:
            self.md_bg_color = self.theme_cls._get_primary_color()

    def set_text_color(self, interval):
        if not self.text_color:
            self.text_color = self.theme_cls._get_text_color()

    def on_state(self, widget, value):
        if value == 'down':
            self.md_bg_color = self.background_down
        else:
            self.md_bg_color = self.background_normal


class MyToggleButton(MDFillRoundFlatIconButton, MDToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Test(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        tags = {'meat', 'veggie', 'egg', 'dough food', 'breakfast'}
        rules = {'short': ({'Wednesday', 'Friday', 'Thursday', 'Monday', 'Tuesday'}, 0), 
                'long': ({'Saturday', 'Sunday'}, 1), 
                'medium': ({'Saturday', 'Wednesday', 'Friday', 'Sunday', 'Thursday', 'Monday', 'Tuesday'}, 17)}
        icons = {
            "short": "clock-time-one-outline",
            "medium": "clock-time-five-outline",
            "long": "clock-time-nine-outline"
        }
        self.screen.ids.settingsRules.add_widget(MDExpansionPanel(
                    content = RulesDayButtons(rules=rules, group="rulesTimePeriod", icons=icons),
                    panel_cls=MDExpansionPanelOneLine(
                        text="'Prepare time per day' rules"
                    )
                ))
        
        # Check meal chip as it was saved in settings
        self.meals = {"0": "Breakfast", "2": "Lunch", "4": "Dinner"}
        meal_chips = self.screen.ids.meals.children
        
        for chip in meal_chips:
            if str(chip.value) in self.meals and not len(chip.ids.box_check.children):
                chip.ids.box_check.add_widget(MDIcon(
                            icon="check",
                            size_hint=(None, None),
                            size=("26dp", "26dp"),
                            font_size=sp(20)
                        ))
        rules = {'Lunch': ({'Sunday'}, 16)}
        icons = {
            "Breakfast": "bowl-mix",
            "Brunch": "food-variant",
            "Lunch": "pasta",
            "Supper": "pot-steam",
            "Dinner": "noodles"
        }

        rulesDiscardMeal = MDExpansionPanel(
                    content = RulesDayButtons(rules=rules, group="rulesDiscardMeal", icons=icons, filter=self.meals),
                    panel_cls=MDExpansionPanelOneLine(
                        text="'Discarded meal per day' rules"
                    )
                )

        self.screen.ids.settingsRules.add_widget(rulesDiscardMeal)
        self.screen.ids['rulesDiscardMeal'] = rulesDiscardMeal


        rules = {'Breakfast': ({'breakfast'}, 2), 
                'Lunch': (set(), 21), 
                'Brunch': (set(), 22), 
                'Supper': (set(), 23), 
                'Dinner': (set(), 24)}
        
        rulesTagsMeal = MDExpansionPanel(
                    content = RulesTagsMeals(rules=rules, filter=self.meals, allTags=tags),
                    panel_cls=MDExpansionPanelOneLine(
                        text="'Tags per meal' rules"
                    )
                )

        self.screen.ids.settingsRules.add_widget(rulesTagsMeal)
        self.screen.ids['rulesTagsMeal'] = rulesTagsMeal
        # !!!!Don't forget in updateMeals() to set filter anew

    def build(self):
        return self.screen

    def updateMeals(self, chip):
        if chip.value in self.meals:
            del self.meals[chip.value]
        else:
            self.meals[chip.value] = chip.text
        self.screen.ids.rulesDiscardMeal.content.filter = self.meals
        self.screen.ids.rulesDiscardMeal.content.setInitValues()
        self.screen.ids.rulesTagsMeal.content.filter = self.meals
        self.screen.ids.rulesTagsMeal.content.setInitValues()


Test().run()