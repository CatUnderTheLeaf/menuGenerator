import os
# import gettext

from kivy.lang import Observable
from kivy.utils import platform

import plyerAndroidClasses.copyGettext as gettext

# internationalization made with the help of
# https://github.com/tito/kivy-gettext-example
class Lang(Observable):
    observers = []
    lang = None

    def __init__(self, defaultlang):
        super(Lang, self).__init__()
        self.ugettext = None
        self.lang = defaultlang
        self.switch_lang(self.lang)

    def _(self, text):
        return self.ugettext(text)

    def fbind(self, name, func, args, **kwargs):
        if name == "_":
            self.observers.append((func, args, kwargs))
        else:
            return super(Lang, self).fbind(name, func, *args, **kwargs)

    def funbind(self, name, func, args, **kwargs):
        if name == "_":
            key = (func, args, kwargs)
            if key in self.observers:
                self.observers.remove(key)
        else:
            return super(Lang, self).funbind(name, func, *args, **kwargs)

    def switch_lang(self, lang):
        # get the right locales directory, and instanciate a gettext
        locale_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "localisation")
        if platform == "android":
            from android.storage import app_storage_path
            app_path = app_storage_path()
            locale_dir = os.path.join(app_path, 'app', 'localisation')
            
        locales = gettext.translation('messages', locale_dir, languages=[lang])
        self.ugettext = locales.gettext
        self.lang = lang

        # update all the kv rules attached to this text
        for func, largs, kwargs in self.observers:
            func(largs, None, None)


tr = Lang("EN")