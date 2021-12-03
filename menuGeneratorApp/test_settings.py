from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDRectangleFlatButton, MDFillRoundFlatIconButton, BaseButton
from kivy.uix.behaviors import ToggleButtonBehavior
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivy.metrics import dp
from kivymd.uix.behaviors import (
    BackgroundColorBehavior,
    CircularElevationBehavior,
    CircularRippleBehavior,
    CommonElevationBehavior,
    FakeRectangularElevationBehavior,
    RectangularRippleBehavior,
)
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    DictProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
)

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

<RulesDayTime>    
    cols: 1
    orientation: 'tb-lr'
    adaptive_height: True
    spacing: dp(5)
    padding: 0, dp(20), 0, 0
    width: Window.width

    MDStackLayout:
        adaptive_height: True
        id: rulesPrepareTime

        MyToggleButton:
            text: "short"
            icon: "clock-time-one-outline"
            group: "rulesPrepareTime"
            state: "down"
        
        MyToggleButton:
            text: "medium"
            icon: "clock-time-five-outline"
            group: "rulesPrepareTime"

        MyToggleButton:
            text: "long"
            icon: "clock-time-nine-outline"
            group: "rulesPrepareTime"

    MDStackLayout:
        adaptive_height: True
        id: rulesPrepareTimeDays

        TextRoundButton:            
            value: "Monday"
        TextRoundButton:
            value: "Tuesday"
        TextRoundButton:
            value: "Wednesday"
        TextRoundButton:
            value: "Thursday"
        TextRoundButton:
            value: "Friday"
        TextRoundButton:
            value: "Saturday"
        TextRoundButton:
            value: "Sunday"


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
    # spacing: dp(5)
    # padding: dp(5)
'''

class RulesDayTime(MDGridLayout):
    rules = DictProperty()
    pass

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
        rules = {'short': {'Monday', 'Thursday', 'Tuesday', 'Friday', 'Wednesday'}, 
                'medium': {'Sunday', 'Monday', 'Thursday', 'Tuesday', 'Friday', 'Saturday', 'Wednesday'}, 
                'long': {'Sunday', 'Saturday'}}
        self.screen.ids.settingsRules.add_widget(MDExpansionPanel(
                    content = RulesDayTime(rules=rules),
                    panel_cls=MDExpansionPanelOneLine(
                        text="'Prepare time per day' rules"
                    )
                ))

    def build(self):
        return self.screen


Test().run()