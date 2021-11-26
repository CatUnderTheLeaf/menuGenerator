from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine

KV = '''

<MyToggleButton>:
    background_down: app.theme_cls.primary_dark

<RulesWidget>:
    cols: 1
    adaptive_height: True
    # spacing: dp(5)
    # padding: dp(5)

<RulesContent@MDGridLayout>:
    cols: 1
    adaptive_height: True
    # spacing: dp(5)
    padding: dp(10)

    MDLabel:
        text: "For Breakfast use:"

    MDStackLayout:
        adaptive_height: True
        id: meal_nutrient 
        
        MDIconButton:
            icon: "leaf"
        
        MDIconButton:
            icon: "barley"
        
        MDIconButton:
            icon: "peanut"
        
        MDIconButton:
            icon: "fish"
        
        MDIconButton:
            icon: "shaker"
    
    MDLabel:
        text: "For Lunch use:"

    MDStackLayout:
        adaptive_height: True
        id: meal_nutrient 
        
        MDIconButton:
            icon: "leaf"
        
        MDIconButton:
            icon: "barley"
        
        MDIconButton:
            icon: "peanut"
        
        MDIconButton:
            icon: "fish"
        
        MDIconButton:
            icon: "shaker"

    MDLabel:
        text: "For Dinner use:"

    MDStackLayout:
        adaptive_height: True
        id: meal_nutrient 
        
        MDIconButton:
            icon: "leaf"
        
        MDIconButton:
            icon: "barley"
        
        MDIconButton:
            icon: "peanut"
        
        MDIconButton:
            icon: "fish"
        
        MDIconButton:
            icon: "shaker"
        



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

class RulesWidget(MDGridLayout):
    pass        

class RulesContent(MDGridLayout):
    pass

class Test(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        self.screen.ids.settingsRules.add_widget(MDExpansionPanel(
                    content = RulesContent(),
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
        pass


Test().run()