from datetime import date, timedelta
from logging import raiseExceptions
import os

from classes.classMenu import Menu

from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivymd.uix.list import OneLineListItem, MDList, OneLineIconListItem, TwoLineAvatarListItem, ImageLeftWidget
from kivy.uix.screenmanager import NoTransition
from kivymd.theming import ThemableBehavior
from kivy.metrics import sp
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivymd.uix.label import MDIcon
from kivymd.utils.fitimage import FitImage
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.chip import MDChip

from kivy.storage.jsonstore import JsonStore

store = JsonStore('menu_settings.json')


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

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class Content(MDBoxLayout):
    text = StringProperty()

class Tab(MDFloatLayout, MDTabsBase):
    day = ObjectProperty()

class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()
    secondary_text = StringProperty()
    source = StringProperty()
    recipe = ObjectProperty()

class MenuGeneratorApp(MDApp):  
    """ 
    Generate Menu tabs for n days
    delete previous tabs and load content to the first new tab
    
     """
    def generateMenuTabs(self):
        # TODO as tabs now has no problems with load do I need spinner???
        # self.root.ids.spinner.active = True
        # old tabs to remove if exist
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
        # TODO if there are many tabs carousel doesn't slide back to the first tab

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
                        img_box.add_widget(FitImage(source="menuGeneratorApp\img\Hot_meal.jpg"))
                        instance_tab.ids.box.add_widget(img_box)
                
                        panel = MDExpansionPanel(
                            icon= 'language-python',
                            content=Content(text=f"Recipe instructions for recipe {recipe}"),
                            panel_cls=MDExpansionPanelTwoLine(
                                text=f"{recipe}",
                                secondary_text=f"{', '.join(recipe.ingridients)}"
                            )
                        )
                        instance_tab.ids.box.add_widget(panel)     

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

        # Create Menu object
        p = os.path.dirname(__file__)
        self.menu = Menu(p)

        # load settings from the storage
        if store.exists('settings'):
            timePeriod = store.get('settings')['timePeriod']            
            repeatDishes = store.get('settings')['repeatDishes']
            meals = store.get('settings')['meals']
        
        # set settings in the menu
        self.set_n_days(timePeriod)
        self.menu.repeatDishes = repeatDishes
        for key in meals:
            self.menu.update_mpd(int(key), meals[key])

        # set settings on the screen
        self.setTimePeriodChipColor(timePeriod)
        self.root.ids.repeatDishes.active = repeatDishes
        self.setMealChipColor(meals)

        # generate menu for n+1 days applying rules
        self.generateMenuTabs()
        self.get_recipes()

    def get_recipes(self):
        for recipe in self.menu.recipeList:
            list_item = SwipeToDeleteItem(
                    text=f"{recipe}",
                    secondary_text=f"{', '.join(recipe.ingridients)}",
                    source="menuGeneratorApp\img\Hot_meal.jpg",
                    recipe = recipe
                )
            self.root.ids.recipe_scroll.add_widget(list_item)

    """ 
    Save settings to a storage
    
     """
    def on_stop(self):
        store.put('settings', timePeriod=self.menu.timePeriod, 
                            repeatDishes=self.menu.repeatDishes,
                            meals = self.menu._mpd)


    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        '''Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''
        if len(instance_tab.ids.box.children)<1:
            self.fillTabs(instance_tab)
    
    '''Check chip as it was saved in settings

    :param tPeriod: text of the chip;
    '''
    def setTimePeriodChipColor(self, tPeriod):
        chips = self.root.ids.timePeriod.children
        for chip in chips:
            if chip.text==tPeriod:
                chip.ids.box_check.add_widget(MDIcon(
                            icon="check",
                            size_hint=(None, None),
                            size=("26dp", "26dp"),
                            font_size=sp(20),
                        ))

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

    '''Set number of days and timeperiod

    :param value: text of the chip in settings;
    '''
    def set_n_days(self, value):        
        if value=="day":
            self.menu.n = 1
            self.menu.timePeriod = "day"
        if value=="week":
            self.menu.n = 7
            self.menu.timePeriod = "week"
        # TODO set n based on which month is now
        if value=="month":
            self.menu.n = 30
            self.menu.timePeriod = "month"    

    '''Called when checking chips.

    :param instance: kivymd.uix.chip.MDChip
    :param value: text of the chip;
    '''
    def on_choseChip_check(self, instance, value):
        # remove all other checks except instance
        for chip in instance.parent.children:
            if chip.text!=value and len(chip.ids.box_check.children):
                check = chip.ids.box_check.children[0]
                chip.ids.box_check.remove_widget(check)

    def on_repeat_switch(self, checkbox, value):
        if value:
            self.menu.repeatDishes = True
        else:
            self.menu.repeatDishes = False

    def on_meal_check(self, instance, value):
        self.menu.update_mpd(value, instance.text)

    def remove_recipe_from_list(self, instance):
        self.root.ids.recipe_scroll.remove_widget(instance)
    
    def edit_recipe(self, instance):
        self.root.ids.screen_manager.current = "scr4"
        recipe = instance.recipe
        self.root.ids.recipeTitle.text = recipe.title
        # remove old ingridients
        all_ingridients = len(self.root.ids.recipeIngridients.children)
        for ingridient in recipe.ingridients:
            self.root.ids.recipeIngridients.add_widget(MDChip(
                                        text=ingridient,
                                        icon='',
                                        check=False))
        # remove old ingridients
        for i in range(all_ingridients):
            self.root.ids.recipeIngridients.remove_widget(self.root.ids.recipeIngridients.children[-1])
        
        # remove old tags
        all_tags = len(self.root.ids.recipeTags.children)
        for tag in recipe.tags:
            self.root.ids.recipeTags.add_widget(MDChip(
                                        text=tag,
                                        icon='',
                                        check=False))
        for i in range(all_tags):
            self.root.ids.recipeTags.remove_widget(self.root.ids.recipeTags.children[-1])
        
        self.root.ids.recipeDescription.text = recipe.description

        
    def saveRecipe(self):
        print("save recipe")
    
    def returnBack(self):
        self.root.ids.screen_manager.current = "scr3"
        

    


if __name__ == '__main__':    
    MenuGeneratorApp().run()