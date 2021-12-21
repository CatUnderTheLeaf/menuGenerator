from datetime import date, timedelta
import os
import yaml

# This needs to be here to display the images on Android
os.environ['KIVY_IMAGE'] = 'pil,sdl2'

from classes.classMenu import Menu
from classes.classRecipe import Recipe


from myWidgetClasses.customButtons import *
from myWidgetClasses.menuSettings import MenuSettings
from myWidgetClasses.RecipeWidget import RecipeWidget
from myWidgetClasses.RecipeSelectionList import RecipeListItem, RecipeSelectionList
from myWidgetClasses.otherWidgetClasses import *

from kivy.uix.screenmanager import NoTransition
from kivy.utils import get_color_from_hex
from kivy.storage.jsonstore import JsonStore

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivymd.utils.fitimage import FitImage

class MenuGeneratorApp(MDApp):  
    overlay_color = get_color_from_hex("#6042e4")
    dialog = None
    custom_sheet = None
    # Create Menu object        
    menu = Menu()
    

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

    """ 
    Change Screen by name
    
     """
    def changeScreen(self, name):
        self.root.ids.screen_manager.current = name

    """
    Set settings in Menu object

    :param settings: MenuSettings object
    """
    def setSettingsInMenu(self, timePeriod, repeatDishes, meals):
        self.set_n_days(timePeriod)
        self.menu.repeatDishes = repeatDishes
        self.menu.update_mpd(meals)

    """
    update Rules in db 

    :param changedRules: Dict of changed rules
    """
    def updateRules(self, changedRules):
        if changedRules:
            self.menu.db.updateRules(changedRules)

    """
    Add Settings widget on the screen
    """
    def add_settingsWidget(self):
        if not len(self.root.ids.settingsScroll.children):
            initValues = {
                'timePeriod': self.menu.timePeriod,
                'repeat': self.menu.repeatDishes,
                'meals': self.menu._mpd,
                'rules': self.menu.db.getRules().rules,
                'tags': self.menu.db.getTags()
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
                            self.updateRules(settings.changedRules),
                            settings.updateInitValues(),
                            self.generateMenuTabs(),
                            self.changeScreen("Menu")
                        )
                    ),
                    MDFlatButton(
                        text="Discard all changes",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: (
                            self.dialog.dismiss(), 
                            settings.setInitialValues()
                            )
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
            self.root.ids.recipe_scroll.tags = self.menu.db.getTags()
            self.root.ids.recipe_scroll.products = self.menu.db.getProducts()
            for recipe in self.menu.db.getRecipes():
                self.root.ids.recipe_scroll.addRecipeInList(recipe)

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
     
    '''Remove recipeWidget and
    remove recipe from db 

    :param instance_recipe_scroll: RecipeSelectionList
    '''
    def deleteRecipes(self, instance_recipe_scroll):
        recipes = instance_recipe_scroll.get_selected_list_items()
        ids = []
        for recipeWidget in recipes:
            ids.append(recipeWidget.instance_item.recipe.id)
            instance_recipe_scroll.remove_widget(recipeWidget)     
        instance_recipe_scroll.selected_mode = False
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
            recipeWidget = RecipeWidget(recipe = instance.recipe, parentWidget=instance, recipe_scroll=self.root.ids.recipe_scroll)           
        else:
            self.root.ids.editRecipeBar.title = "Add new recipe"
            recipeWidget = RecipeWidget(recipe = Recipe(), recipe_scroll=self.root.ids.recipe_scroll)

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
                recipeWidget.parentWidget.redrawRecipeListItem(recipeWidget.recipe)
            else:                
                self.root.ids.recipe_scroll.addRecipeInList(recipeWidget.recipe)
                
    
    '''
    switch the selection mode "on" or "off"

    :param instance_recipe_scroll: RecipeSelectionList
    :param mode: Bool
    '''
    def set_selection_mode(self, instance_recipe_scroll, mode):
        if mode:
            md_bg_color = self.overlay_color
            left_action_items = [
                [
                    "close",
                    lambda x: self.unselectAllRecipes(instance_recipe_scroll),
                ]
            ]
            right_action_items = [["trash-can", lambda x: self.deleteRecipes(instance_recipe_scroll)]]
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

    :param instance_recipe_scroll: RecipeSelectionList
    '''
    def unselectAllRecipes(self, instance_recipe_scroll):
        instance_recipe_scroll.unselected_all()
        instance_recipe_scroll.last_selected = False

    '''
    add or increase number of selected items in the toolbar

    :param instance_recipe_scroll: RecipeSelectionList with recipes
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

    :param instance_recipe_scroll: RecipeSelectionList with recipes
    :param instance_selection_item: selected item
    '''
    def on_unselected(self, instance_recipe_scroll, instance_selection_item):
        if instance_recipe_scroll.get_selected_list_items():
            self.root.ids.recipeListToolbar.title = str(
                len(instance_recipe_scroll.get_selected_list_items())
            )
        else:
            instance_recipe_scroll.last_selected = True
 
if __name__ == '__main__':    
    MenuGeneratorApp().run()