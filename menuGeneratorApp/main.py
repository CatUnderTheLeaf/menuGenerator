from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

class MenuGenerator(BoxLayout):
    pass

class MenuGeneratorApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        return MenuGenerator()

if __name__ == '__main__':
    MenuGeneratorApp().run()