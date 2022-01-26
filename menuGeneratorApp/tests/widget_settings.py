from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.list import MDList, OneLineIconListItem
from kivymd.uix.button import MDFillRoundFlatIconButton, BaseButton, MDFlatButton
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

MDScreen:

    MDBoxLayout:
        orientation: "vertical"
        
        MDNavigationLayout:

            ScreenManager:
                id: screen_manager
                
                MDScreen:
                    name: "Menu"
                    
                    MDBoxLayout:
                        orientation: "vertical"
                        id: menu

                        MDToolbar:
                            pos_hint: {"top": 1}
                            title: "Menu"
                            left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                            right_action_items: [["refresh", lambda x: app.generateMenuTabs(), "reGenerate Menu"]]


                        MDBoxLayout:
                            id: empty_menu
                            orientation: "vertical"
                            spacing: dp(10)
                            padding: dp(10)

                            Widget:

                            MDLabel:
                                text: "Menu is not generated yet"
                                halign: "center"

                            MDIconButton:
                                icon: "refresh"
                                pos_hint: {"center_x": .5}
                                on_release: app.generateMenuTabs()

                            Widget:
                
            MDNavigationDrawer:
                id: nav_drawer

                ContentNavigationDrawer:
                    screen_manager: screen_manager
                    nav_drawer: nav_drawer

<ContentNavigationDrawer>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"
    screen_manager: root.screen_manager
    nav_drawer: root.nav_drawer

    AnchorLayout:
        anchor_x: "left"
        size_hint_y: None
        height: avatar.height

        Image:
            id: avatar
            size_hint: None, None
            size: "56dp", "56dp"
            source: "data/logo/kivy-icon-256.png"

    MDLabel:
        text: "Menu Generator"
        font_style: "Button"
        adaptive_height: True

    ScrollView:
        screen_manager: root.screen_manager
        nav_drawer: root.nav_drawer

        DrawerList:
            id: md_list
            screen_manager: root.screen_manager
            nav_drawer: root.nav_drawer
            
            ItemDrawer:
                text: "Menu"
                text_color: app.theme_cls.primary_color
                cur_screen: "Menu"
                icon: "book-open-variant"

            ItemDrawer:
                text: "Settings"
                cur_screen: "Settings"
                icon: "cog"
                on_press: app.add_settingsWidget()

            ItemDrawer:
                text: "Recipes"
                cur_screen: "AllRecipes"
                icon: "nutrition"
                on_press: app.get_recipes()
    
    MDBoxLayout:
        spacing: dp(10)
        padding: dp(10)
        adaptive_height: True

        TextToggleButton:
            text: "EN"
            group: "language"
            # custom_color: 0, 1, 0, 1

        MDSeparator:
            orientation: "vertical"
            height: dp(10)
        
        TextToggleButton:
            text: "RU"
            group: "language"
            # custom_color: 0, 1, 0, 1
               
<ItemDrawer>:
    theme_text_color: "Custom"
    on_press:
        self.parent.set_color_item(self)
        self.parent.nav_drawer.set_state("close")
        self.parent.screen_manager.current = root.cur_screen
        

    IconLeftWidget:
        icon: root.icon
        theme_text_color: "Custom"
        text_color: root.text_color

<TextToggleButton>:
    font_color_normal: app.theme_cls.text_color
    font_color_down: app.theme_cls.primary_color
    theme_text_color: "Custom"
    height: dp(10)
    width: dp(15)

'''

class TextToggleButton(MDFlatButton, MDToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))

class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class Test(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        

    def build(self):
        return self.screen


Test().run()