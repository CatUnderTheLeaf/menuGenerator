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

    _window_manager = None
    _window_manager_open = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)      

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

    def capture(self):
        camera = self.ids['camera']
        if platform == "android":
            from android.storage import primary_external_storage_path, app_storage_path
            dstpath = os.path.join(primary_external_storage_path(), 'Pictures', 'MenuGenerator')
            if not os.path.isdir(dstpath):
                os.mkdir(dstpath)
        else:
            dstpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "img/")

        self.photo = os.path.join(dstpath, f"IMG_{time.strftime('%Y%m%d_%H%M%S')}.png")
        camera.export_to_png(self.photo)
        print("Captured")