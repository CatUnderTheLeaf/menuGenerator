from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
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

KV = '''
<MyScreen>

    MDBoxLayout:
        orientation: "vertical"
        adaptive_size: True
        spacing: "12dp"
        padding: "56dp"
        pos_hint: {"center_x": .5, "center_y": .5}

        MDLabel:
            text: "Multiple choice"
            bold: True
            font_style: "H5"
            adaptive_size: True

        MDBoxLayout:
            id: chip_box
            adaptive_size: True
            spacing: "8dp"

            MyChip:
                text: "Elevator"
                on_press: if self.active: root.removes_marks_all_chips()

            MyChip:
                text: "Washer / Dryer"
                on_press: if self.active: root.removes_marks_all_chips()

            MyChip:
                text: "Fireplace"
                on_press: if self.active: root.removes_marks_all_chips()


ScreenManager:

    MyScreen:

<MyChip>:
    # icon_check_color: 1, 1, 1, 1
    text_color: 1, 1, 1, 1
    _no_ripple_effect: True
    icon: ''
    icon_left: ''
    icon_right: ''

<updatedMDChip>:
    size_hint_y: None
    height: "32dp"
    spacing: "8dp"
    adaptive_width: True
    radius: 16 if self.radius == [0, 0, 0, 0] else self.radius
    padding:
        "12dp" if not self.icon_left else "4dp", \
        0, \
        "12dp" if not self.icon_right else "8dp", \
        0
    md_bg_color:
        app.theme_cls.primary_dark \
        if root.active else \
        app.theme_cls.primary_color        

    canvas.before:
        Color:
            rgba:
                self.line_color \
                if not self.disabled else \
                app.theme_cls.disabled_hint_text_color
        Line:
            width: 1
            rounded_rectangle:
                ( \
                self.x, \
                self.y, \
                self.width, \
                self.height, \
                *self.radius, \
                self.height \
                )

    MDRelativeLayout:
        id: relative_box
        size_hint: None, None
        size: ("24dp", "24dp") if root.icon_left else (0, 0)
        pos_hint: {"center_y": .5}
        radius: self.height / 2

        MDIcon:
            id: icon_left
            icon: root.icon_left
            size_hint: None, None
            size: ("28dp", "28dp") if root.icon_left else (0, 0)
            theme_text_color: "Custom"
            pos_hint: {"center_y": .5}
            pos: 0, -2
            text_color:
                ( \
                root.icon_left_color \
                if root.icon_left_color else \
                root.theme_cls.disabled_hint_text_color \
                ) \
                if not self.disabled else app.theme_cls.disabled_hint_text_color

        MDBoxLayout:
            id: icon_left_box
            size_hint: None, None
            radius: self.height / 2
            size: ("28dp", "28dp") if root.icon_left else (0, 0)
            pos: 0, -2

        MDIcon:
            id: check_icon
            icon: "check"
            pos_hint: {"center_y": 0.5}
            size_hint: None, None
            size: "28dp", "28dp"
            color: (1, 1, 1, 1) if not root.icon_check_color else root.icon_check_color
            pos: 2, -2

    MDLabel:
        id: label
        text: root.text
        adaptive_size: True
        markup: True
        pos_hint: {"center_y": .5}
        color:
            ( \
            root.text_color \
            if root.text_color else \
            root.theme_cls.disabled_hint_text_color \
            ) \
            if not self.disabled else app.theme_cls.disabled_hint_text_color

    MDIcon:
        id: icon_right
        icon: root.icon_right
        size_hint: None, None
        size: ("18dp", "18dp") if root.icon_right else (0, 0)
        font_size: "18sp" if root.icon_right else 0
        theme_text_color: "Custom"
        pos_hint: {"center_y": .5}
        text_color:
            ( \
            root.icon_right_color \
            if root.icon_right_color else \
            root.theme_cls.disabled_hint_text_color \
            ) \
            if not self.disabled else app.theme_cls.disabled_hint_text_color
'''

class updatedMDChip(
    ThemableBehavior,
    RectangularRippleBehavior,
    FakeRectangularElevationBehavior,
    TouchBehavior,
    ButtonBehavior,
    MDBoxLayout,
):
    text = StringProperty()
    """
    Chip text.
    :attr:`text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    icon = StringProperty("checkbox-blank-circle", deprecated=True)
    """
    Chip icon.
    .. deprecated:: 1.0.0
        Use :attr:`icon_right` and :attr:`icon_left` instead.
    :attr:`icon` is an :class:`~kivy.properties.StringProperty`
    and defaults to `'checkbox-blank-circle'`.
    """

    icon_left = StringProperty()
    """
    Chip left icon.
    .. versionadded:: 1.0.0
    :attr:`icon_left` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    icon_right = StringProperty()
    """
    Chip right icon.
    .. versionadded:: 1.0.0
    :attr:`icon_right` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    color = ColorProperty(None, deprecated=True)
    """
    Chip color in ``rgba`` format.
    .. deprecated:: 1.0.0
    :attr:`color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    text_color = ColorProperty(None)
    """
    Chip's text color in ``rgba`` format.
    :attr:`text_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    icon_color = ColorProperty(None, deprecated=True)
    """
    Chip's icon color in ``rgba`` format.
    .. deprecated:: 1.0.0
        Use :attr:`icon_right_color` and :attr:`icon_left_color` instead.
    :attr:`icon_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    icon_right_color = ColorProperty(None)
    """
    Chip's right icon color in ``rgba`` format.
    .. versionadded:: 1.0.0
    :attr:`icon_right_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    icon_left_color = ColorProperty(None)
    """
    Chip's left icon color in ``rgba`` format.
    .. versionadded:: 1.0.0
    :attr:`icon_left_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    icon_check_color = ColorProperty(None)
    """
    Chip's check icon color in ``rgba`` format.
    .. versionadded:: 1.0.0
    :attr:`icon_check_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    check = BooleanProperty(False, deprecated=True)
    """
    If `True`, a checkmark is added to the left when touch to the chip.
    .. deprecated:: 1.0.0
    :attr:`check` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    selected_chip_color = ColorProperty(None, deprecated=True)
    """
    The color of the chip that is currently selected in ``rgba`` format.
    .. deprecated:: 1.0.0
    :attr:`selected_chip_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `None`.
    """

    active = BooleanProperty(False)
    """
    Whether the check is marked or not.
    .. versionadded:: 1.0.0
    :attr:`active` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_long_touch(self, *args):
        if self.active:
            return
        self.active = True if not self.active else False

    def on_active(self, instance_check, active_value: bool):
        if active_value:
            self.do_animation_check((0, 0, 0, 0.4), 1)
        else:
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
            self.icon_check_color = self.theme_cls.primary_color
        else:
            self.active = True
            self.icon_check_color = (1, 1, 1, 1)
  
class MyChip(updatedMDChip):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon_check_color = self.theme_cls.primary_color

    

class MyScreen(MDScreen):
    def removes_marks_all_chips(self):
        print("hello")


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)


Test().run()