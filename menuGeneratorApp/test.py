from kivy.lang import Builder

from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, ColorProperty, ListProperty, NumericProperty
from kivymd import images_path

KV = '''
<DescriptionContent>:
    padding: dp(20), dp(20), dp(20), 0
    size_hint_y: None
    height: self.minimum_height
    width: app.root.width
    
    MDTextField:
        id: recipe_text
        text: root.text
        disabled: True
        multiline: True
        width: root.width


MDScreen:

    MDBoxLayout:
        orientation: "vertical"

        MDToolbar:
            title: "Expansion panel"
            elevation: 10

        ScrollView:

            MDGridLayout:
                cols: 1
                adaptive_height: True
                id: box
'''


class DescriptionContent(MDBoxLayout):
    text = StringProperty()

class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        text = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Imperdiet sed euismod nisi porta lorem mollis aliquam. Massa tincidunt dui ut ornare lectus sit amet est. Mauris cursus mattis molestie a iaculis at. Nunc sed velit dignissim sodales. Enim neque volutpat ac tincidunt vitae semper quis. Eget mauris pharetra et ultrices neque ornare aenean euismod. Libero id faucibus nisl tincidunt eget nullam non. Velit laoreet id donec ultrices tincidunt. Id volutpat lacus laoreet non curabitur gravida arcu. Arcu dictum varius duis at consectetur. Dignissim enim sit amet venenatis. Convallis posuere morbi leo urna. Dolor sed viverra ipsum nunc aliquet bibendum enim facilisis gravida.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolor",
                "Lorem ipsum dolor sit amet, consectetur ancididunt ut labore et dolor",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolor tempor incididunt ut labore et dolore magna aliqua. Imperdiet sed euismod nisi porta lorem",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolor tempor incididunt ut labore et dolore magna aliqua. Imperdiet sed euismod nisi porta lorem tempor incididunt ut labore et dolore magna aliqua. Imperdiet sed euismod nisi porta lorem"]
        for i in range(5):
            self.root.ids.box.add_widget(MDExpansionPanel(
                    icon="clock-time-one-outline",
                    content = DescriptionContent(text=text[i]),
                    panel_cls=MDExpansionPanelTwoLine(
                        text="Text",
                        secondary_text="Secondary text"
                    )
                )
                
            )


Test().run()