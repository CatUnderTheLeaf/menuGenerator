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
    '''Class implementing content for a tab.'''

class MenuGeneratorApp(MDApp):

    p = os.path.dirname(__file__)
    # Create Menu object
    menu = Menu(p)

    # generate menu for n+1 days applying rules
    n = 10
    

    def generateMenuTabs(self):
        # TODO now spinner frizes when new tabs are generating
        # self.root.ids.spinner.active = True
        # remove old tabs if exist
        # unfortunately it will leave the last tab
        first_time = True
        tabs = self.root.ids.tabs.get_tab_list()
        for del_tab in tabs:
            first_time = False
            self.root.ids.tabs.remove_widget(del_tab)
        
        # new dates
        sdate = date.today()
        edate = sdate + timedelta(days=self.n)
        self.menu.generateDailyMenu(sdate, edate)

        # add new Tab widgets
        for day in self.menu.menu:
            day_title = "\n{}, {} {}".format(day.strftime("%A"), day.day, day.strftime("%b"))
            tab = Tab(title=day_title)
            for meal in self.menu.mpd:
                recipe = self.menu.menu[day][meal]
                if (recipe is not None):
                    tab.ids.box.add_widget(
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
                    tab.ids.box.add_widget(panel)            
            self.root.ids.tabs.add_widget(tab)

        # remove last tab from previous if exists
        if not first_time:
            self.root.ids.tabs.remove_widget(self.root.ids.tabs.get_tab_list()[0])

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
        pass
        # instance_tab.ids.container.text = tab_text
    pass

    def callback(self, instance, value):
        toast(value)


if __name__ == '__main__':    
    MenuGeneratorApp().run()