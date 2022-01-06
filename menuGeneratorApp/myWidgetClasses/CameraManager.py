import os
import time

from kivy.properties import (
    ObjectProperty,
    StringProperty
)
from kivy.uix.modalview import ModalView

from kivymd.theming import ThemableBehavior
from kivymd.uix.relativelayout import MDRelativeLayout

class CameraManager(ThemableBehavior, MDRelativeLayout):
    exit_manager = ObjectProperty(lambda x: None)
    photo = StringProperty('')
    directory = ObjectProperty(None)

    _window_manager = None
    _window_manager_open = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.ids.xcamera.force_landscape()
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
        self.photo = filename