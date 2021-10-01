from datetime import date, timedelta
import os

from classes.classMenu import Menu

from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivymd.uix.list import OneLineListItem, MDList, OneLineIconListItem
from kivy.uix.screenmanager import NoTransition
from kivymd.theming import ThemableBehavior
from kivymd.toast import toast

from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine

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
    pass

class Tab(MDFloatLayout, MDTabsBase):
    day = ObjectProperty()
    '''Class implementing content for a tab.'''

class MenuGeneratorApp(MDApp):

    p = os.path.dirname(__file__)
    # Create Menu object
    menu = Menu(p)

    # generate menu for n+1 days applying rules
    n = 4
    
    """ 
    Generate Menu tabs for n days
    delete previous tabs and load content to the first new tab
    
     """
    def generateMenuTabs(self):
        # TODO now spinner frizes when new tabs are generating
        # self.root.ids.spinner.active = True
        # old tabs to remove if exist
        del_tabs = self.root.ids.tabs.get_tab_list()
        
        # generate Menu for new dates
        sdate = date.today()
        edate = sdate + timedelta(days=self.n-1)
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
    Generate Menu
    
     """
    def on_start(self):
        self.root.ids.screen_manager.transition = NoTransition()
        self.generateMenuTabs()
            

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        '''Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''
        if len(instance_tab.ids.box.children)<1:
            self.fillTabs(instance_tab)
    pass


    def callback(self, instance, value):
        if value=="day":
            self.n = 1
        if value=="week":
            self.n = 7
        if value=="month":
            self.n = 30


if __name__ == '__main__':    
    MenuGeneratorApp().run()