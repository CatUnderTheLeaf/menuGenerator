from datetime import date, timedelta
import re
from logging import raiseExceptions
import os
import yaml
import math

from classes.classMenu import Menu
from classes.classRecipe import Recipe

from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.list import OneLineListItem, MDList, OneLineIconListItem, TwoLineAvatarIconListItem
from kivy.uix.screenmanager import NoTransition
from kivymd.theming import ThemableBehavior
from kivymd.icon_definitions import md_icons
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.chip import MDChip
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDFillRoundFlatIconButton

from kivy.metrics import dp, sp
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ListProperty,
    StringProperty,
    ObjectProperty,
    NumericProperty
)
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine, MDExpansionPanelOneLine
from kivymd.uix.label import MDIcon
from kivymd.uix.selection import MDSelectionList
from kivymd.utils.fitimage import FitImage
from kivy.utils import get_color_from_hex

from kivy.storage.jsonstore import JsonStore

class MyToggleButton(MDFillRoundFlatIconButton, MDToggleButton):
    def __init__(self, **kwargs):
        self.background_down = MDApp.get_running_app().theme_cls.primary_dark
        super().__init__(**kwargs)

class MyExpansionPanel(MDExpansionPanel):
    products = ListProperty()
    ingredientWidget = ObjectProperty()
    
    def on_open(self):
        if len(self.content.ids.chooseIngredients.children)<1:
            ingredients = []
            for button_with_cross in self.ingredientWidget.children:
                ingredients.append(button_with_cross.text)
            for product in self.products:
                chip = MDChip(text=product, check=True, icon='')
                chip.bind(on_release=self.markIngredient)
                if product in ingredients and not len(chip.ids.box_check.children):
                    chip.ids.box_check.add_widget(MDIcon(
                                icon="check",
                                size_hint=(None, None),
                                size=("26dp", "26dp"),
                                font_size=sp(20),
                            ))
                self.content.ids.chooseIngredients.add_widget(chip)
    
    def markIngredient(self, instance_chip):
        if not len(instance_chip.ids.box_check.children):
            self.ingredientWidget.add_widget(ButtonWithCross(
                                            text=instance_chip.text,
                                            parentId=self.ingredientWidget))
        else:
            for button_with_cross in self.ingredientWidget.children:
                if button_with_cross.text==instance_chip.text:
                    self.ingredientWidget.remove_widget(button_with_cross)
        
class DescriptionContent(MDBoxLayout):
    text = StringProperty()

class ContentCustomSheet(MDBoxLayout):    
    rows = NumericProperty()

class BottomCustomSheet(MDBoxLayout):
    text = StringProperty()

class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))

class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

class dialogItem(OneLineIconListItem):
    divider = None
    icon = StringProperty()

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class Content(MDBoxLayout):
    text = StringProperty()

class Tab(MDFloatLayout, MDTabsBase):
    day = ObjectProperty()

class RecipeListItem(TwoLineAvatarIconListItem):
    text = StringProperty()
    secondary_text = StringProperty()
    img_source = StringProperty()
    recipe = ObjectProperty()    

class RecipeSelectionList(MDSelectionList):
    last_selected = BooleanProperty()

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

class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    focus = BooleanProperty()

class RecipeWidget(MDBoxLayout):
    recipe = ObjectProperty()
    parentWidget = ObjectProperty()

class MenuGeneratorApp(MDApp):  
    overlay_color = get_color_from_hex("#6042e4")
    dialog = None
    custom_sheet = None
    

    """ 
    Generate Menu tabs for n days
    delete previous tabs and load content to the first new tab
    
     """
    def generateMenuTabs(self):        
        # old tabs to remove if exist 
        # because I can't delete all tabs but one 
        del_tabs = self.root.ids.tabs.get_tab_list()
        
        # generate Menu for new dates
        sdate = date.today()
        n = self.menu.n
        edate = sdate + timedelta(days=n-1)
        self.menu.generateDailyMenu(sdate, edate)

        # add new Tab widgets
        for day in self.menu.menu:
            day_title = "\n{}, {} {}".format(day.strftime("%A"), day.day, day.strftime("%b"))
            tab = Tab(title=day_title, day=day)                
            self.root.ids.tabs.add_widget(tab)

        all_tabs = self.root.ids.tabs.get_tab_list()
        
        # remove old tabs from previous if exist
        for i in range(len(del_tabs)):            
            self.root.ids.tabs.remove_widget(all_tabs[i])

        # fill first tab with content
        self.fillTabs(self.root.ids.tabs.get_tab_list()[0].tab)

    """ 
    Fill the content of a tab

    :param instance_tab: <__main__.Tab object>    
     """
    def fillTabs(self, instance_tab):
        for meal in self.menu.mpd:
            recipe = self.menu.menu[instance_tab.day][meal]
            if (recipe is not None):
                instance_tab.ids.box.add_widget(
                    OneLineListItem(text=f"{meal}")
                )
                img_box = MDBoxLayout(size_hint_y=None, height="200dp", orientation='vertical')
                img_box.add_widget(FitImage(source=recipe.img))
                instance_tab.ids.box.add_widget(img_box)
                icon = "clock-time-one-outline"
                if recipe.prepareTime=="medium":
                    icon = "clock-time-five-outline"
                elif recipe.prepareTime=="long":
                    icon = "clock-time-nine-outline"
                
                content = DescriptionContent()
                content.ids.recipe_text.text = recipe.description
                instance_tab.ids.box.add_widget(MDExpansionPanel(
                    icon=icon,
                    content = content,
                    panel_cls=MDExpansionPanelTwoLine(
                        text=f"{recipe}",
                        secondary_text=f"{', '.join(recipe.ingredients)}"
                    )
                ))

    """ 
    Set transition between Screens
    Load settings
    Generate Menu
    
     """
    def on_start(self):
        timePeriod = "day"
        repeatDishes = False
        meals = {"0": "Breakfast", "2": "Lunch", "4": "Dinner"}
        
        self.root.ids.screen_manager.transition = NoTransition()
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True
        )

        # Create Menu object        
        self.menu = Menu()

        # load db_type and db_path
        with open(os.path.join(os.path.dirname(__file__), "app_settings.yml"), 'r') as stream:
            data_loaded = yaml.safe_load(stream)

        db = data_loaded['DB_TYPE']
        db_path = os.path.join(os.path.dirname(__file__), data_loaded['MENU_DB'])
        self.menu.connectDB(db, db_path)

        settings_path = os.path.join(os.path.dirname(__file__), data_loaded['MENU_SETTINGS'])
        self.store = JsonStore(settings_path)

        # load settings from the storage
        if self.store.exists('settings'):
            timePeriod = self.store.get('settings')['timePeriod']            
            repeatDishes = self.store.get('settings')['repeatDishes']
            meals = self.store.get('settings')['meals']
        
        # set settings in the menu
        self.set_n_days(timePeriod)
        self.menu.repeatDishes = repeatDishes
        for key in meals:
            self.menu.update_mpd(int(key), meals[key])

        # set settings on the screen
        self.setChooseChip(self.root.ids.timePeriod, timePeriod)
        self.root.ids.repeatDishes.active = repeatDishes
        self.setMealChipColor(meals)

        # generate menu for n+1 days applying rules
        self.generateMenuTabs()
    
    """ 
    Save settings to a storage
    
     """
    def on_stop(self):
        self.store.put('settings', timePeriod=self.menu.timePeriod, 
                            repeatDishes=self.menu.repeatDishes,
                            meals = self.menu._mpd)
        self.menu.disconnectDB()

    """ 
    Load all recipes to the Recipe list scroll
    if it is empty
 
     """
    def get_recipes(self):
        if not len(self.root.ids.recipe_scroll.children):
            for recipe in self.menu.db.getRecipes():
                self.addRecipeInList(recipe)

    """ 
    add one recipe to the Recipe list scroll

    :param recipe: Recipe object
 
     """
    def addRecipeInList(self, recipe):
        list_item = RecipeListItem(
                        text=f"{recipe}",
                        secondary_text=f"{', '.join(recipe.ingredients)}",
                        recipe = recipe
                    )
        self.root.ids.recipe_scroll.add_widget(list_item)

    '''Called when switching tabs.

    :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
    :param instance_tab: <__main__.Tab object>;
    :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
    :param tab_text: text or name icon of tab;
    '''
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):        
        if len(instance_tab.ids.box.children)<1:
            self.fillTabs(instance_tab)
    
    '''Check chip as it was saved in settings

    :param id: widget id, container of chips
    :param value: text of the chip;
    '''
    def setChooseChip(self, id, value):
        chips = id.children
        for chip in chips:
            if chip.text==value:
                chip.state = 'down'

    '''Check meal chip as it was saved in settings

    :param meals: dict (chip.value: chip.text)
    '''
    def setMealChipColor(self, meals):
        chips = self.root.ids.meals.children
        for chip in chips:
            if str(chip.value) in meals:
                chip.ids.box_check.add_widget(MDIcon(
                            icon="check",
                            size_hint=(None, None),
                            size=("26dp", "26dp"),
                            font_size=sp(20),
                        ))

    '''
    Set number of days and timeperiod

    :param value: text of the chip in settings;
    '''
    def set_n_days(self, value):        
        if value=="day":
            self.menu.n = 1
            self.menu.timePeriod = "day"
        if value=="week":
            self.menu.n = 7
            self.menu.timePeriod = "week"
        if value=="month":
            self.menu.n = 30
            self.menu.timePeriod = "month"    

    '''Called when clicking on repeat Switch in settings.

    :param checkbox: kivymd.uix.chip.MDChip.checkbox
    :param value: text of the chip;
    '''
    def on_repeat_switch(self, checkbox, value):
        if value:
            self.menu.repeatDishes = True
        else:
            self.menu.repeatDishes = False

    '''Called when checking meals in settings.

    :param instance: kivymd.uix.chip.MDChip
    :param value: text of the chip;
    '''
    def on_meal_check(self, instance, value):
        self.menu.update_mpd(value, instance.text)
     
    '''remove widget from its parent

    :param parentId: parent id of the Widget to remove
    :param instance: a Widget to remove;
    '''
    def removeCustomWidget(self, parentId, instance):
        parentId.remove_widget(instance)

    '''Remove recipeWidget and
    remove recipe from db 

    :param instance: a Widget with recipe;
    '''
    def deleteRecipes(self, recipes):
        ids = []
        for recipeWidget in recipes:
            ids.append(recipeWidget.instance_item.recipe.id)
            self.removeCustomWidget(self.root.ids.recipe_scroll, recipeWidget)
        self.root.ids.recipe_scroll.selected_mode = False
        self.menu.db.deleteRecipes(ids)


    '''Load edit recipe screen
    and all recipe info to edit 

    :param instance: a Widget with recipe;
    '''
    def edit_recipe(self, instance={}):
        if instance and instance.parent.owner.last_selected:
            instance.parent.owner.last_selected = False
            return
        self.root.ids.screen_manager.current = "scr4"
        
        # remove old widget
        self.root.ids.editRecipeScroll.clear_widgets()
        # form new recipe
        if instance:
            self.root.ids.editRecipeBar.title = "Edit recipe"
            recipeWidget = RecipeWidget(recipe = instance.recipe, parentWidget=instance)
            recipe = instance.recipe        
            recipeWidget.ids.recipeTitle.text = recipe.title
            # load new ingredients
            for ingredient in recipe.ingredients:
                recipeWidget.ids.recipeIngredients.add_widget(ButtonWithCross(
                                            text=ingredient,
                                            parentId=recipeWidget.ids.recipeIngredients))
                
            # set recipe prepare
            self.setChooseChip(recipeWidget.ids.recipePrepareTime, recipe.prepareTime)
            
            # set if recipe can be used on two consecutive days
            recipeWidget.ids.recipeRepeatDish.active = recipe.repeat

            # load new tags
            for tag in recipe.tags:
                recipeWidget.ids.recipeTags.add_widget(ButtonWithCross(
                                            text=tag,
                                            parentId=recipeWidget.ids.recipeTags))
            
            recipeWidget.ids.recipeDescription.text = recipe.description
        else:
            self.root.ids.editRecipeBar.title = "Add new recipe"
            recipeWidget = RecipeWidget(recipe = Recipe())

        # add recipeWidget
        self.root.ids.editRecipeScroll.add_widget(recipeWidget)

    '''Save all recipe info 

    :param recipeWidget: a Widget with recipe;
    '''    
    def saveRecipe(self, recipeWidget):
        # form recipe data
        if recipeWidget.ids.recipeTitle.text=='':
            recipeWidget.ids.recipeTitle.error = True
            recipeWidget.ids.recipeTitle.focus = True
        else:
            recipeWidget.recipe.title = recipeWidget.ids.recipeTitle.text
            recipeWidget.recipe.img = recipeWidget.ids.recipeImg.source
            recipeWidget.recipe.ingredients = []
            for ingredient in recipeWidget.ids.recipeIngredients.children:
                recipeWidget.recipe.ingredients.append(ingredient.text)
            recipeWidget.recipe.prepareTime = "short"
            for prepareTime in recipeWidget.ids.recipePrepareTime.children:
                if prepareTime.state=='down':
                    recipeWidget.recipe.prepareTime = prepareTime.text
            recipeWidget.recipe.tags = []
            for tag in recipeWidget.ids.recipeTags.children:
                recipeWidget.recipe.tags.append(tag.text)
            recipeWidget.recipe.repeat = recipeWidget.ids.recipeRepeatDish.active
            recipeWidget.recipe.description = recipeWidget.ids.recipeDescription.text
            self.menu.db.updateRecipe(recipeWidget.recipe)

            # return to recipeList screen
            self.root.ids.screen_manager.current = "scr3"
            # redraw recipe widget in scrollview
            # or add a new one list item
            if recipeWidget.parentWidget:
                self.redrawRecipeWidget(recipeWidget.parentWidget, recipeWidget.recipe)
            else:
                self.addRecipeInList(recipeWidget.recipe)

    '''redraw recipeWidget in the scrollview
    with new recipe info 

    :param parentWidget: a Widget in the scrollview
    :param newRecipe: new recipe info
    '''    
    def redrawRecipeWidget(self, parentWidget, newRecipe):
        parentWidget.text=f"{newRecipe}"
        parentWidget.img_source = newRecipe.img
        parentWidget.secondary_text=f"{', '.join(newRecipe.ingredients)}"
        parentWidget.recipe = newRecipe

    '''
    return back to recipe list without saving
    '''    
    def returnBack(self):
        self.root.ids.screen_manager.current = "scr3"

    '''
    switch the selection mode "on" or "off"
    '''
    def set_selection_mode(self, instance_recipe_scroll, mode):
        if mode:
            md_bg_color = self.overlay_color
            left_action_items = [
                [
                    "close",
                    lambda x: self.unselectAllRecipes(),
                ]
            ]
            right_action_items = [["trash-can", lambda x: self.deleteRecipes(instance_recipe_scroll.get_selected_list_items())]]
        else:
            md_bg_color = (0, 0, 0, 1)
            left_action_items = [["menu", lambda x: self.root.ids.nav_drawer.set_state("open")]]
            right_action_items = []
            self.root.ids.recipeListToolbar.title = "All recipes"

        self.root.ids.recipeListToolbar.left_action_items = left_action_items
        self.root.ids.recipeListToolbar.right_action_items = right_action_items

    '''
    unselect all Recipes
    and mark that all was unselected
    '''
    def unselectAllRecipes(self):
        self.root.ids.recipe_scroll.unselected_all()
        self.root.ids.recipe_scroll.last_selected = False

    '''
    add or increase number of selected items in the toolbar

    :param instance_recipe_scroll: MDSelectionList with recipes
    :param instance_selection_item: selected item
    '''
    def on_selected(self, instance_recipe_scroll, instance_selection_item):
        self.root.ids.recipeListToolbar.title = str(
            len(instance_recipe_scroll.get_selected_list_items())
        )

    '''
    decrease or remove number of selected items in the toolbar
    mark that last item was removed 
    (used for a workaround because 
    on_press or on_release events of RecipeListItem 
    are called after SelectionItem.on_touch*
    and there can be a situation, when
    you want to unselect the last selected item, 
    so you click on it, selected_mode is false, item is not selected,
    and it goes straight to RecipeListItem.on_release and opens 'edit' Screen)

    :param instance_recipe_scroll: MDSelectionList with recipes
    :param instance_selection_item: selected item
    '''
    def on_unselected(self, instance_recipe_scroll, instance_selection_item):
        if instance_recipe_scroll.get_selected_list_items():
            self.root.ids.recipeListToolbar.title = str(
                len(instance_recipe_scroll.get_selected_list_items())
            )
        else:
            instance_recipe_scroll.last_selected = True

    '''
    refresh dropdown items for tag search

    :param textField: tags text field
    :param recipeWidget: recipe Widget with recycle view
    '''
    def refresh(self, text, textField, recipeWidget):
        def add_tag_item(tag):
            recipeWidget.ids.rv.data.append(
                {
                    "viewclass": "OneLineListItem",
                    "text": tag,
                    "on_release": lambda x=tag: self.set_item(x, textField, recipeWidget)
                }
            )

        if len(text) > 0:
            recipeWidget.ids.rv.data = []
            currentTags = []
            for tag in recipeWidget.ids.recipeTags.children:
                currentTags.append(tag.text)
            for tag in self.menu.db.getUnusedTags(currentTags):
                if text in tag:
                    add_tag_item(tag)            
        else:
            recipeWidget.ids.rv.data = []
        
        if recipeWidget.ids.rv.data:
                recipeWidget.ids.rv.parent.height = dp(205)
        else:
            recipeWidget.ids.rv.parent.height = 0
            
    '''
    add new tag to the tags stackLayout

    :param text__item: string text
    :param textField: tags text field
    :param recipeWidget: recipe Widget with recycle view
    '''
    def set_item(self, text__item, textField, recipeWidget):
        text = ' '.join(text__item.split())
        if len(text):
            textField.focus = False
            textField.text = ''
            recipeWidget.ids.rv.data = []
            recipeWidget.ids.rv.parent.height = 0
            recipeWidget.ids.recipeTags.add_widget(ButtonWithCross(
                                                text=text,
                                                parentId=recipeWidget.ids.recipeTags))

    def show_example_list_bottom_sheet(self, ingredients, ingredientWidget):
        products = self.menu.db.getProducts()
        custom_sheet = BottomCustomSheet()   
        for category in products:
            cat_text = ''
            if ',' in category:
                cat_text = ', '.join(w[0].upper() + w[1:] for w in category.split(','))
            elif '_' in category:
                cat_text = ' '.join(category.split('_')).capitalize()
            else:
                cat_text = category.capitalize()
            panel = MyExpansionPanel(
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
        self.file_manager_open()
        '''
        Found out on android.developers that actually for "All files" is needed the permission MANAGE_EXTERNAL_STORAGE.

Just put in buildozer.spec file MANAGE_EXTERNAL_STORAGE also:

(list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE No need to put it in the py code as you mnetioned for the other other permissions. they are ok in the code to avoit asking for the permission every time the app is launched.

But, after the app is installed you'll have to go on the app permission to all the management of all files allow permission

Worked for me, hope it helps.
You need to change self.file_manager.show('/') to

self.file_manager.show(primary_ext_storage)
where primary_ext_storage is the file directory on your android phone. You also need to declare below.

from android.storage import primary_external_storage_path
primary_ext_storage = primary_external_storage_path()
primary_external_storage_path() returns Android’s so-called “primary external storage”, often found at /sdcard/ and potentially accessible to any other app. It compares best to the Documents directory on Windows.

On top of that, you need to add the following code in your script to ensure there is permission to access to the storage on the phone.

from android.permissions import request_permissions, Permission
request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
Do not be confused by the name of primary_ext_storage . It is not referring to your android phone SD card. Instead, it will be pointing to your internal storage.

For external storage on android phone, you can use

from android.storage import secondary_external_storage_path
secondary_ext_storage = secondary_external_storage_path()
        '''

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
        if os.path.isfile(path):
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

    def open_camera(self):
        print("camera")
        

if __name__ == '__main__':    
    MenuGeneratorApp().run()
