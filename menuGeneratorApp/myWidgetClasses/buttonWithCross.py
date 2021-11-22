from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivy.properties import (
    ColorProperty,
    ListProperty,
    StringProperty,
    ObjectProperty
)
from kivy.metrics import dp

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

class MyToggleButton(MDFillRoundFlatIconButton, MDToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)