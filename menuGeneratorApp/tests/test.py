#!/usr/bin/env python
import os
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import (
    ObjectProperty,
    StringProperty
)
from kivy.uix.modalview import ModalView

from kivymd.theming import ThemableBehavior
from kivymd.uix.relativelayout import MDRelativeLayout

kv = """
#:import XCamera kivy_garden.xcamera.XCamera

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
                            id: empty
                            orientation: "vertical"
                            spacing: dp(10)
                            padding: dp(10)

                            Widget:

                            MDLabel:
                                text: "click to photo"
                                halign: "center"

                            MDIconButton:
                                icon: "refresh"
                                pos_hint: {"center_x": .5}
                                on_release: app.open_camera()

                            Widget:


<CameraManager>:
    MDBoxLayout:
        orientation: "vertical"
        spacing: dp(5)

        MDToolbar:
            id: toolbar
            left_action_items: [["chevron-left", lambda x: root.exit_manager(1)]]
            elevation: 10
    
        XCamera:
            id: xcamera
            on_picture_taken: 
                root.picture_taken(*args)
                root.exit_manager(1)
       

"""

class CameraManager(ThemableBehavior, MDRelativeLayout):
    exit_manager = ObjectProperty(lambda x: None)
    photo = StringProperty('')
    directory = ObjectProperty(None)

    _window_manager = None
    _window_manager_open = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.xcamera.force_landscape()
        self.ids.xcamera.directory = self.directory

    def show(self):

        if not self._window_manager:
            self._window_manager = ModalView(
                size_hint=self.size_hint, auto_dismiss=False
            )
            
            self._window_manager.add_widget(self)
        if not self._window_manager_open:
            self._window_manager.open()
            self._window_manager_open = True

    def close(self):
        """Closes the file manager window."""

        self._window_manager.dismiss()
        self._window_manager_open = False
    
    def picture_taken(self, obj, filename):
        print('Picture taken and saved to {}'.format(filename))

 

class CameraApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(kv)
        self.camera_manager_open = False
        self.camera_manager = None

    def build(self):
        return self.screen
    
    '''
    Called when the user closes camera.
    '''
    def exit_camera_manager(self, *args):
        self.camera_manager_open = False
        self.camera_manager.close()
        print(self.camera_manager.photo)
        # if os.path.isfile(self.camera_manager.photo):
        #     self.ids.recipeImg.source = self.camera_manager.photo

    def open_camera(self):
        if not self.camera_manager:
                self.camera_manager = CameraManager(
                    exit_manager=self.exit_camera_manager,
                    directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "img/")
                )
        self.camera_manager.show()  # output manager to the screen
        self.camera_manager_open = True

    def picture_taken(self, obj, filename):
        print('Picture taken and saved to {}'.format(filename))


def main():
    CameraApp().run()


if __name__ == '__main__':
    main()
