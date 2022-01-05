import re
import os
import math
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.camera import Camera
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, ColorProperty, ListProperty, NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.chip import MDChip
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine

from kivymd.uix.list import OneLineIconListItem
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarListItem

KV = '''

<dialogItem>
    on_release:
        app.dialog.dismiss()
        app.open_gallery() if root.icon=='image' else app.get_camera()

    IconLeftWidget:
        icon: root.icon

<RecipeWidget>:
    id: editRecipe
    orientation: "vertical"
    adaptive_height: True
    padding: dp(48)
    spacing: dp(15)

    SmartTile:
        id: recipeImg
        source: "menuGeneratorApp\img\/no_image.png"
        size_hint_y: None
        height: dp(200)
        box_color: (0, 0, 0, 0)
        on_release: app.show_simple_dialog()

    MDTextField:
        id: recipeTitle
        hint_text: "Title"
        required: True
        helper_text_mode: "on_error"

    MDLabel:
        text: "Ingredients"

    MDStackLayout:
        adaptive_height: True
        spacing: dp(5)
        id: recipeIngredients

        MDChip:
            text: "Ingredient1"
            check: True

        MDChip:
            text: "Ingredient2"
            check: True

        MDChip:
            text: "Ingredient3"
            check: True
    
    MDIconButton:
        icon: "plus"
        theme_text_color: "Custom"
        md_bg_color: app.theme_cls.primary_color
        user_font_size: "20sp"
        on_release: app.show_ingredients_bottom_sheet(root.ids.recipeIngredients)

    MDSeparator:

    MDLabel:
        text: "Prepare time"

    MDStackLayout:
        adaptive_height: True
        spacing: dp(5)
        id: recipePrepareTime

        MDChip:
            text: "short"
            icon: "clock-time-one-outline"
            on_release: app.on_choseChip_check(self, self.text)
            check: True

        MDChip:
            text: "medium"
            icon: "clock-time-five-outline"
            on_release: app.on_choseChip_check(self, self.text)
            check: True

        MDChip:
            text: "long"
            icon: "clock-time-nine-outline"
            on_release: app.on_choseChip_check(self, self.text)
            check: True

    MDSeparator:

    MDGridLayout:
        cols: 2
        adaptive_height: True                            

        MDLabel:
            text: "Repeat dish?"

        MDSwitch:
            id: recipeRepeatDish

    MDSeparator:

    MDLabel:
        text: "Tags"   

    MDStackLayout:
        adaptive_height: True
        spacing: dp(5)
        id: recipeTags

        MDChip:
            text: "tag1"
            check: True

        MDChip:
            text: "tag2"
            check: True

        MDChip:
            text: "tag3"
            check: True
   
    MDBoxLayout:
        adaptive_height: True
        padding: dp(12), 0,0,0  

        ClickableTextFieldRound:
            id: click_text_field
            size_hint_x: None
            width: "200dp"
            hint_text: "Add new tag"
    
    MDBoxLayout:
        orientation: 'vertical'
        adaptive_height: True
        height: 0

        RecycleView:
            id: rv
            key_viewclass: 'viewclass'
            key_size: 'height'            

            RecycleBoxLayout:
                default_size: dp(200), dp(48)
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
    
    MDSeparator:
    
    MDTextField:
        id: recipeDescription
        multiline: True
        hint_text: "Prepare instructions"

<BottomCustomSheet>:
    orientation: "vertical"
    size_hint_y: None
    height: "400dp"
    padding: dp(20)
    
    ScrollView:
        
        MDBoxLayout:
            orientation: "vertical"
            adaptive_height: True
            id: custom_sheet_grid
        
<ContentCustomSheet>:
    orientation: "vertical"
    padding: dp(20), dp(20), dp(20), 0
    height: chooseIngredients.height
    adaptive_height: True
        
    MDGridLayout:
        cols: 2
        orientation: 'tb-lr'
        adaptive_height: True
        height: dp(26)*root.rows + self.spacing[0]*(root.rows-1)
        spacing: dp(5)
        id: chooseIngredients

<ClickableTextFieldRound>:
    size_hint_y: None
    height: text_field.height

    MDTextFieldRound:
        id: text_field
        hint_text: root.hint_text
        text: root.text
        color_active: app.theme_cls.primary_light
        on_text: if self.focus: app.refresh(self.text, self, root.parent.parent)

    MDIconButton:
        icon: "plus"
        ripple_scale: .5
        pos_hint: {"center_y": .5}
        pos: text_field.width - self.width + dp(8), 0
        on_release: app.set_item(text_field.text, text_field, root.parent.parent)
            

<ButtonWithCross>:  
    id: box
    size_hint: None,  None
    height: "26dp"
    padding: "8dp", 0, 0, 0
    width:
        self.minimum_width - (dp(10) if DEVICE_TYPE == "desktop" else dp(20)) \
        if root.icon != 'close' else self.minimum_width

    canvas:
        Color:
            rgba: root.theme_cls.primary_color if not root.color else root.color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: root.radius
    
    MDLabel:
        adaptive_size: True
        -text_size: None, None
        pos_hint: {"center_y": .5}
        id: label
        text: root.text
        size_hint_x: None
        width: self.texture_size[0]
        color: root.text_color if root.text_color else (root.theme_cls.text_color)
        markup: True
    
    MDIconButton:
        id: lbl_ic
        icon: root.icon
        theme_text_color: "Custom"
        adaptive_size: True
        pos_hint: {"center_y": .5}
        on_release: app.removeCustomWidget(root.parentId, root)    


MDScreen
    MDBoxLayout:
        orientation: "vertical"

        MDToolbar:
            id: editRecipeBar
            pos_hint: {"top": 1} 
            title: "Edit recipe"
            left_action_items: [["arrow-left"]]
            right_action_items: [["check"]]


        ScrollView:
            id: editRecipeScroll

            RecipeWidget:
                
           
'''
# class BodyManagerWithPreview(MDBoxLayout):
    # """Base class for folder icons and thumbnails images in ``preview`` mode."""

class dialogItem(OneLineIconListItem):
    divider = None
    icon = StringProperty()

class IngredientsExpansionPanel(MDExpansionPanel):
    products = ListProperty()
    def on_open(self):
        if len(self.content.ids.chooseIngredients.children)<1:
            for product in self.products:
                self.content.ids.chooseIngredients.add_widget(MDChip(
                                            text=product, check=True))
        

class BottomCustomSheet(MDBoxLayout):
    text = StringProperty()

class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    focus = BooleanProperty()

class RecipeWidget(MDBoxLayout):
    recipe = ObjectProperty()
    parentWidget = ObjectProperty()

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

class ContentCustomSheet(MDBoxLayout):    
    rows = NumericProperty()

class BottomCustomSheet(MDBoxLayout):
    text = StringProperty()

class Test(MDApp):
    dialog = None
    custom_sheet = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True
        )
        self.screen = Builder.load_string(KV)

    def file_manager_open(self):
        path = os.path.join(os.path.dirname(__file__), "img/")
        self.file_manager.show(path)  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        self.setRecipeImage(path)

    def setRecipeImage(self, path):
        self.root.ids.editRecipeScroll.children[0].ids.recipeImg.source = path

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def refresh(self, text, textField, recipeWidget):
        def add_icon_item(name_icon):
            recipeWidget.ids.rv.data.append(
                {
                    "viewclass": "OneLineListItem",
                    "text": name_icon,
                    "on_release": lambda x=name_icon: self.set_item(x, textField, recipeWidget)
                }
            )

        if len(text) > 1:
            recipeWidget.ids.rv.data = []
            for name_icon in md_icons.keys():
                if text in name_icon:
                    add_icon_item(name_icon)
            # print(recipeWidget.ids.rv.data)
            if recipeWidget.ids.rv.data:
                recipeWidget.ids.rv.parent.height = dp(205)
            else:
                recipeWidget.ids.rv.parent.height = 0
        else:
            recipeWidget.ids.rv.data = []
            recipeWidget.ids.rv.parent.height = 0
            

    def set_item(self, text__item, textField, recipeWidget):
        text = re.sub(r"\s+", "", text__item)
        if len(text):
            textField.focus = False
            textField.text = ''
            recipeWidget.ids.rv.data = []
            recipeWidget.ids.rv.parent.height = 0
            recipeWidget.ids.recipeTags.add_widget(ButtonWithCross(
                                                text=text,
                                                parentId=recipeWidget.ids.recipeTags))
    
    def show_ingredients_bottom_sheet(self, ingredientWidget):
        products = {'cereals_grains_pasta_bread_vegan': ['Cereals', 'Bulgur', 'Cornmeal', 'Pasta', 'Rice', 'Wheat', 
        'Bread', 'Oat', 'Vegan Milk', 'Cous-cous', 'Sugar'], 
        'dairy': ['Milk', 'Buttermilk', 'Yogurt'], 
        'dried_beans': ['Dried Beans', 'Dried Peas', 'Lentils'], 
        'low_carb_veggies': ['Avocado', 'Olives', 'Carrots', 'Snowpeas', 'Ginger', 'Onion', 'Kohlrabi', 
        'Swede', 'Capsicum', 'Red Capsicum', 'Cabbage', 'White Cabbage', 'Turnip', 'Fennel', 'Leek', 'Squash', 
        'Spaghetti Squash', 'Bamboo Shoots', 'Celeriac', 'Red Cabbage', 'Green Beans', 
'Green Capsicum', 'Patty-pan Squash', 'Eggplant', 'Tomato', 'Kale', 'Savoy Cabbage', 'Yellow Wax Beans', 
'Rocket', 'Brussel Sprouts', 'Hairy Melon', 'Radish', 'Cauliflower', 'Cucumber', 'Zucchini Flowers', 'Cos Lettuce',
 'Bean Sprouts', 'Zucchini', 'Asparagus', 'Okra', 'Artichoke Hearts', 'Celery', 'Silverbeet', 'Chinese Broccoli', 
 'Mignonette Leaves', 'Chilli', 'Radicchio', 'English Spinach', 'Spinach', 'Bok Choy', 'Alfalfa Sprouts', 'Broccoli', 'Curly Endive', 'Mushroom'], 
 'fat_nuts': ['Margarine', 'Mayonnaise', 'Almonds', 'Cashews', 'Pecans', 'Peanuts', 'Walnuts', 'Nuts', 'Seeds', 'Pine nuts', 'Oil', 
 'Corn Oil', 'Cottonseed Oil', 'Sunflower Oil', 'Olive Oil', 'Peanut Oil', 'Salad dressing', 'Butter', 'Bacon', 'Coconut', 'Cream', 'Sour Cream', 'Cream cheese'], 
 'fruits': ['Apples', 'Applesauce', 'Apricots', 'Banana', 'Blackberries', 'Blueberries', 'Cantaloupe', 'Cherries', 'Figs', 'Grapefruit', 'Grapes', 'Honeydew melon',
  'Melon', 'Kiwi', 'Mandarin', 'Mango', 'Nectarines', 'Orange', 'Papaya', 'Peach', 'Pear', 'Persimmon', 'Pineapple', 'Plum', 'Pomegranat', 'Raspberries', 'Strawberries', 
  'Tangerine', 'Watermelon', 'Dates', 'Prunes', 'Raisins', 'Juice', 'Cranberries', 'Rhubarb'], 'high_carb_veggies': ['Corn', 'Beans', 'Lima Beans', 'Peas', 'Green Peas', 
  'Plaintain', 'Potato', 'Winter Squash', 'Sweet Potato'], 
  'meat_fish_cheese_eggs': ['Beef', 'Pork', 'Veal', 'Chicken', 'Turkey', 'Fish', 'Crab', 'Lobster', 'Scallops', 
  'Shrimp', 'Clams', 'Oysters', 'Venison', 'Rabbit', 'Pheasant', 'Duck', 'Goose', 'Cottage Cheese', 'Cheese', 'Egg', 'Tofu', 'Sausage', 'Salami'], 
  'other_seasoning': ['Bouillon', 'Water', 'Cocoa Powder', 'Coffee', 'Tea', 'Tonic Water', 'Gelatin', 'Catsup', 
  'Horseradish', 'Mustard', 'Vinegar', 'Basil', 'Lemon Pepper', 'Celery Seeds', 'Lime', 'Cinnamon', 'Lime Juice', 
  'Chili Powder', 'Mint', 'Chives', 'Onion Powder', 'Curry', 'Oregano', 'Dill', 'Paprika', 'Vanilla Extract', 
  'Pepper', 'Garlic', 'Pimento', 'Garlic Powder', 'Spices', 'Herbs', 'Soy Sauce']}
        custom_sheet = BottomCustomSheet()   
        for category in products:
            cat_text = ''
            if ',' in category:
                cat_text = ', '.join(w[0].upper() + w[1:] for w in category.split(','))
            elif '_' in category:
                cat_text = ' '.join(category.split('_')).capitalize()
            else:
                cat_text = category.capitalize()
            panel = IngredientsExpansionPanel(
                        products=products[category],
                        ingredientWidget=ingredientWidget,
                        content=ContentCustomSheet(rows=math.ceil(len(products[category])/2)),            
                        panel_cls=MDExpansionPanelOneLine(
                            text=f"{cat_text}"
                        )
                    )
            custom_sheet.ids.custom_sheet_grid.add_widget(panel)
        self.custom_sheet = MDCustomBottomSheet(screen=custom_sheet, radius_from="top")
        self.custom_sheet.open()

    def build(self):
        return self.screen

    def show_simple_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Set recipe image",
                type="simple",
                items=[
                    dialogItem(text="Choose from gallery", icon='image'),
                    dialogItem(text="Take a picture", icon='camera')
                ],
            )
        self.dialog.open()

    def open_gallery(self):
        print("gallery")
        self.file_manager_open()

    def get_camera(self):
        print("camera")
        # cam = Camera()

Test().run()