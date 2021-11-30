from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDFillRoundFlatIconButton, MDFillRoundFlatIconButton, MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.uix.behaviors import ToggleButtonBehavior
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    StringProperty,
    ObjectProperty,
    ListProperty,
    DictProperty,
    ColorProperty,
    NumericProperty
)

KV = '''

<MyToggleButton>:
    background_down: app.theme_cls.primary_dark

<IconToggleButton>:
    background_down: app.theme_cls.primary_dark
    background_normal: app.theme_cls.primary_color
    theme_text_color: "Custom"            
    md_bg_color: self.background_normal
    text_color: 1, 1, 1, 1
    text: " "
    on_release: app.set_n_days(self)

<RulesWidget>:
    cols: 1
    adaptive_height: True
    # spacing: dp(5)
    # padding: dp(5)

<RulesContent>:
    cols: 1
    adaptive_height: True
    spacing: dp(20)
    padding: 0, dp(20), 0, 0
    width: Window.width
    
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
                                        on_release: app.on_meal_check(self, self.value)
                                        check: True

                                    MDChip:
                                        text: "Brunch"
                                        icon: "food-variant"
                                        value: 1
                                        on_release: app.on_meal_check(self, self.value)
                                        check: True

                                    MDChip:
                                        text: "Lunch"
                                        icon: "pasta"
                                        value: 2
                                        on_release: app.on_meal_check(self, self.value)
                                        check: True
                                    
                                    MDChip:
                                        text: "Supper"
                                        icon: "pot-steam"
                                        value: 3
                                        on_release: app.on_meal_check(self, self.value)
                                        check: True

                                    MDChip:
                                        text: "Dinner"
                                        icon: "noodles"
                                        value: 4
                                        on_release: app.on_meal_check(self, self.value)
                                        check: True                                
                                
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
'''


class MyToggleButton(MDFillRoundFlatIconButton, MDToggleButton):
    pass

class IconToggleButton(MDIconButton, ToggleButtonBehavior):
    def __init__(self, **kwargs):
            super(IconToggleButton, self).__init__(**kwargs)            

    def on_state(self, widget, value):
        if value == 'down':
            self.md_bg_color = self.background_down
        else:
            self.md_bg_color = self.background_normal
    background_normal = ColorProperty(None)
    background_down = ColorProperty(None)


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
                state = 'normal'
                if icon in self.rules[meal]:
                    state = 'down'
                button = IconToggleButton(icon=self.icons[icon])
                button.state = state
                iconsStack.add_widget(button)
            self.add_widget(iconsStack)

class Test(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        rules = {'Breakfast': ['low_carb', 'high_carb', 'fat', 'free'], 
                'Lunch': ['low_carb', 'high_carb', 'protein', 'fat', 'free'], 
                'Dinner': ['protein', 'fat', 'free', 'low_carb']}
        self.screen.ids.settingsRules.add_widget(MDExpansionPanel(
                    content = RulesContent(rules=rules),
                    panel_cls=MDExpansionPanelOneLine(
                        text="'Nutritions per meal' rules"
                    )
                ))


    def build(self):
        return self.screen

    def pr(self, widget):
        print("hello")
        for child in widget.children:
            print(child.state)

    def set_n_days(self, text):
        print("hello")
        pass


Test().run()