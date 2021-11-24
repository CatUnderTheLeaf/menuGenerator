from datetime import date, timedelta
import os
import yaml
import math

from classes.classMenu import Menu
from classes.classRecipe import Recipe

from myWidgetClasses.myExpansionPanel import IngredientsExpansionPanel
from myWidgetClasses.buttonWithCross import ButtonWithCross
from myWidgetClasses.menuSettings import MenuSettings
from myWidgetClasses.RecipeWidget import RecipeWidget
from myWidgetClasses.otherWidgetClasses import *

from kivy.core.window import Window
from kivy.uix.screenmanager import NoTransition
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.storage.jsonstore import JsonStore

from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.list import OneLineListItem
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine, MDExpansionPanelOneLine
from kivymd.utils.fitimage import FitImage

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
        self.setSettingsInMenu(timePeriod, repeatDishes, meals)

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

    def changeScreen(self, name):
        self.root.ids.screen_manager.current = name

    """
    Set settings in Menu object

    :param timePeriod: str
    :param repeatDishes: Bool
    :param meals: Dict
    """
    def setSettingsInMenu(self, timePeriod, repeatDishes, meals):
        self.set_n_days(timePeriod)
        self.menu.repeatDishes = repeatDishes
        self.menu.update_mpd(meals)

    """
    Add Settings widget on the screen
    """
    def add_settingsWidget(self):
        if not len(self.root.ids.settingsScroll.children):
            initValues = {
                'timePeriod': self.menu.timePeriod,
                'repeat': self.menu.repeatDishes,
                'meals': self.menu._mpd,
            }
            self.root.ids.settingsScroll.add_widget(MenuSettings(initValues = initValues))

    """
    Show dialog if there were made changes in Settings

    :param settings: MenuSettings object
    """
    def saveSettingsDialog(self, settings):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Apply changes?",
                text="Settings were changed. In order to save them please click on 'Apply and regenerate' button. Else your changes will not be saved.",
                buttons=[
                    MDFlatButton(
                        text="Apply and regenerate",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: (
                            self.dialog.dismiss(),
                            self.setSettingsInMenu(settings.timePeriod, settings.repeat, settings.meals),
                            settings.updateInitValues(settings.timePeriod, settings.repeat, settings.meals),
                            self.generateMenuTabs(),
                            self.root.ids.nav_drawer.set_state("open"))
                    ),
                    MDFlatButton(
                        text="Discard",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: (
                            self.dialog.dismiss(), 
                            settings.setInitialValues(),
                            self.root.ids.nav_drawer.set_state("open"))
                    ),
                ],
            )
        self.dialog.open()

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
        self.changeScreen("EditRecipe")
        
        # remove old widget
        self.root.ids.editRecipeScroll.clear_widgets()
        # form new recipe
        if instance:
            self.root.ids.editRecipeBar.title = "Edit recipe"
            recipeWidget = RecipeWidget(recipe = instance.recipe, parentWidget=instance)           
        else:
            self.root.ids.editRecipeBar.title = "Add new recipe"
            recipeWidget = RecipeWidget(recipe = Recipe())

        # add recipeWidget
        self.root.ids.editRecipeScroll.add_widget(recipeWidget)

    '''Save all recipe info 

    :param recipeWidget: a Widget with recipe;
    '''    
    def saveRecipe(self, recipeWidget):
        if recipeWidget.saveRecipe():
            self.menu.db.updateRecipe(recipeWidget.recipe)
            
            # return to recipeList screen
            self.changeScreen("AllRecipes")
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
        self.changeScreen("AllRecipes")

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

    def show_ingredients_bottom_sheet(self, ingredients, ingredientWidget):
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
