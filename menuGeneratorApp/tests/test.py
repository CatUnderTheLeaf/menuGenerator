'''
Camera Example
==============

This example demonstrates a simple use of the camera. It shows a window with
a buttoned labelled 'play' to turn the camera on and off. Note that
not finding a camera, perhaps because gstreamer is not installed, will
throw an exception during the kv language processing.

'''

# Uncomment these lines to see all the messages
# from kivy.logger import Logger
# import logging
# Logger.setLevel(logging.TRACE)

# from kivymd.app import MDApp
# from kivy.lang import Builder
# from kivy.uix.boxlayout import BoxLayout
# import time
# Builder.load_string('''
# <CameraClick>:
#     orientation: 'vertical'
#     Camera:
#         id: camera
#         resolution: (640, 480)
#         play: False
#     ToggleButton:
#         text: 'Play'
#         on_press: camera.play = not camera.play
#         size_hint_y: None
#         height: '48dp'
#     Button:
#         text: 'Capture'
#         size_hint_y: None
#         height: '48dp'
#         on_press: root.capture()
# ''')


# class CameraClick(BoxLayout):
#     def capture(self):
#         '''
#         Function to capture the images and give them the names
#         according to their captured time and date.
#         '''
#         camera = self.ids['camera']
#         timestr = time.strftime("%Y%m%d_%H%M%S")
#         camera.export_to_png("IMG_{}.png".format(timestr))
#         print("Captured")


# class TestCamera(App):

#     def build(self):
#         return CameraClick()


# TestCamera().run()


from os.path import dirname
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.theming import ThemeManager
from kivy.properties import StringProperty

import time

Builder.load_string("""


<ScreenManagement>:
    ScreenOne:
        name: "screen_one"
    ScreenTwo:
        name: "screen_two"
    ScreenThree:
        name: "screen_three"
        id: entry
    ScreenFour:
        name: "screen_four"

<ScreenOne>:
    canvas:
        Color:
            rgb: [.30,.50,.99]
        Rectangle:
            pos: self.pos
            size: self.size
    FloatLayout:
        MDFillRoundFlatButton:
            color: [1,1,1,1]
            text: "Перейти к созданию фото"
            pos_hint: {'center_x':.50, 'center_y':.50}
            on_press:
                root.manager.transition.direction = 'up'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_two'

<ScreenTwo>:
    canvas:
        Color:
            rgb: [.30,.50,.99]
        Rectangle:
            pos: self.pos
            size: self.size
    FloatLayout:
        MDFillRoundFlatButton:
            color: [1,1,1,1]
            text: "Выбрать фон"
            pos_hint: {'center_x':.50, 'center_y':.10}
            on_press:
                root.manager.transition.direction = 'up'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_three'
        MDIconButton:
            icon: 'chevron-double-right'
            pos_hint: {'center_x':.95, 'center_y':.10}
            on_press:
                root.manager.transition.direction = 'down'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_one'

<ScreenThree>:
    id: entry
    canvas:
        Color:
            rgb: [.30,.50,.99]
        Rectangle:
            pos: self.pos
            size: self.size
    FloatLayout:
        Camera:
            id: camera
            index: 0
            resolution: (1280,720)
            play: True  
        MDFillRoundFlatButton:
            text: "take photo"
            pos_hint: {'center_x': 0.50, 'center_y': .10}
            on_press:
                root.capture()   #TAKE PHOTO
                root.manager.transition.direction = 'up'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_four'    
        MDIconButton:
            icon: 'chevron-double-right'
            pos_hint: {'center_x':.95, 'center_y':.10}
            on_press:
                root.manager.transition.direction = 'down'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_two'

<ScreenFour>:
    canvas:
        Color:
            rgb: [.30,.50,.99]
        Rectangle:
            pos: self.pos
            size: self.size
    FloatLayout:
        Image:
            id: img

        MDIconButton:
            icon: 'chevron-double-right'
            pos_hint: {'center_x':.95, 'center_y':.10}
            on_press:
                root.manager.transition.direction = 'down'
                root.manager.transition.duration = 1
                root.manager.current = 'screen_three'
""")


class ScreenOne(Screen):
    pass


class ScreenTwo(Screen):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Blue'
    main_widget = None


class ScreenThree(Screen):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Blue'
    main_widget = None
    photo = StringProperty('')

    def capture(self):
        camera = self.ids['camera']
        self.photo = f"{dirname(__file__)}/IMG_{time.strftime('%Y%m%d_%H%M%S')}.png"
        camera.export_to_png(self.photo)
        print("Captured")


class ScreenFour(Screen):

    def on_pre_enter(self, *args):
        self.ids.img.source = self.manager.ids.entry.photo


class ScreenManagement(ScreenManager):
    pass


class Interface(MDApp):

    def build(self):
        return ScreenManagement()


sample_app = Interface()
sample_app.run()