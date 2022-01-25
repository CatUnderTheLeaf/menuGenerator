from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDFillRoundFlatIconButton, MDIconButton, BaseButton
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior, ButtonBehavior
from kivymd.uix.behaviors import CircularRippleBehavior, RectangularRippleBehavior, FakeRectangularElevationBehavior, TouchBehavior
from kivy.properties import (
    ColorProperty,
    ListProperty,
    StringProperty,
    ObjectProperty,
    DictProperty,
    BooleanProperty
)
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock

class ButtonWithCross(MDBoxLayout, ThemableBehavior):    
    color = ColorProperty(None)
    parentId = ObjectProperty()
    text = StringProperty()
    amount = StringProperty()
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

class MyToggleButton(MDFillRoundFlatIconButton, MDToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class IconToggleButton(MDIconButton, ToggleButtonBehavior):    
    background_normal = ColorProperty(None)
    background_down = ColorProperty(None)
    value = ObjectProperty(None)
    parentWidget = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(IconToggleButton, self).__init__(**kwargs)            

    def on_state(self, widget, value):
        if value == 'down':
            self.md_bg_color = self.background_down
        else:
            self.md_bg_color = self.background_normal

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

# MDChip class from version 1.0.0
class updatedMDChip(
    ThemableBehavior,
    RectangularRippleBehavior,
    FakeRectangularElevationBehavior,
    TouchBehavior,
    ButtonBehavior,
    MDBoxLayout,
):
    text = StringProperty()
    icon = StringProperty("checkbox-blank-circle", deprecated=True)
    icon_left = StringProperty()
    icon_right = StringProperty()
    color = ColorProperty(None, deprecated=True)
    text_color = ColorProperty(None)
    icon_color = ColorProperty(None, deprecated=True)
    icon_right_color = ColorProperty(None)
    icon_left_color = ColorProperty(None)
    icon_check_color = ColorProperty(None)
    check = BooleanProperty(False, deprecated=True)
    selected_chip_color = ColorProperty(None, deprecated=True)
    active = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_long_touch(self, *args):
        if self.active:
            return
        self.active = True if not self.active else False

    def on_active(self, instance_check, active_value: bool):
        if active_value:
            self.icon_check_color = (1, 1, 1, 1)
            self.do_animation_check((0, 0, 0, 0.4), 1)            
        else:
            self.icon_check_color = self.theme_cls.primary_color
            self.do_animation_check((0, 0, 0, 0), 0)
            

    def do_animation_check(
        self, md_bg_color: list, scale_value: int
    ):
        Animation(md_bg_color=md_bg_color, t="out_sine", d=0.1).start(
            self.ids.icon_left_box
        )
        Animation(            
            t="out_sine",
            d=0.1,
        ).start(self.ids.check_icon)

        if not self.icon_left:
            if scale_value:
                self.ids.check_icon.x = -dp(4)
                Animation(size=(dp(24), dp(24)), t="out_sine", d=0.1).start(
                    self.ids.relative_box
                )
            else:
                self.ids.check_icon.x = 0
                Animation(size=(0, 0), t="out_sine", d=0.1).start(
                    self.ids.relative_box
                )

    def on_press(self, *args):
        if self.active:
            self.active = False
        else:
            self.active = True
  
class MyChip(updatedMDChip):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon_check_color = self.theme_cls.primary_color