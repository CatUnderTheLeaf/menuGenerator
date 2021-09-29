from datetime import date, timedelta
import os

from classes.classMenu import Menu

from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.list import OneLineListItem
from kivy.uix.screenmanager import NoTransition

from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine

class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class Content(MDBoxLayout):
    text = StringProperty("android")
    pass

class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''

class MenuGeneratorApp(MDApp):
    p = os.path.dirname(__file__)
    # Create Menu object
    menu = Menu(p)

    # generate menu for n+1 days applying rules
    n = 10
    sdate = date.today()
    edate = sdate + timedelta(days=n)
    menu.generateDailyMenu(sdate, edate)

    def on_start(self):
        self.root.ids.screen_manager.transition = NoTransition()
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


if __name__ == '__main__':    
    MenuGeneratorApp().run()