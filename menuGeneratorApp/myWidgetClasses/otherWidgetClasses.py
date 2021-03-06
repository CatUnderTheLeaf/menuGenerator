from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.relativelayout import MDRelativeLayout

from kivymd.uix.tab import MDTabsBase

from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList, OneLineIconListItem
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    StringProperty,
    ObjectProperty,
    NumericProperty
)
     
class DescriptionContent(MDBoxLayout):
    text = StringProperty()

class ContentCustomSheet(MDBoxLayout):    
    rows = NumericProperty()

class BottomCustomSheet(MDBoxLayout):
    text = StringProperty()

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

class dialogItem(OneLineIconListItem):
    divider = None
    icon = StringProperty()
    parentWidget = ObjectProperty()

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class Tab(MDFloatLayout, MDTabsBase):
    day = ObjectProperty()

class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    focus = BooleanProperty()