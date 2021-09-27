from datetime import date, timedelta

from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.tab import MDTabsBase
from kivy.properties import StringProperty
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem, MDList, OneLineListItem, TwoLineAvatarListItem, BaseListItem
from kivymd.icon_definitions import md_icons
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine
from kivymd import images_path


class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Custom list item.'''

    icon = StringProperty("android")

class Content(MDBoxLayout):
    text = StringProperty("android")
    pass

class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''

class MenuGeneratorApp(MDApp):
    def on_start(self):
        sdate = date.today()
        for i in range(10):
            day = sdate + timedelta(days=i)
            day_title = "\n{}, {} {}".format(day.strftime("%A"), day.day, day.strftime("%b"))
            self.root.ids.tabs.add_widget(Tab(title=day_title))
        tabs = self.root.ids.tabs.get_tab_list()
        for tab in tabs:
            for i in range(3):
                tab.tab.ids.scroll.add_widget(
                    OneLineListItem(text=f"Meal {i+1} on day {tab.tab.title}")
                )
                # tab.tab.ids.scroll.add_widget(
                #     TwoLineAvatarListItem(text=f"Recipe {i+1}")
                # )
                panel = MDExpansionPanel(
                    content=Content(text=f"Recipe instructions for recipe {i+1} on day {tab.tab.title}"),
                    # content=Content(),
                    icon=f"{images_path}kivymd.png",
                    panel_cls=MDExpansionPanelTwoLine(
                        text=f"Recipe {i+1}",
                        secondary_text="Secondary text here"                        
                    )
                )
                grid = MDGridLayout(cols=1, adaptive_height=True)
                grid.add_widget(panel)
                tab.tab.ids.scroll.add_widget(grid
                )
                
            

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
    # def build(self):
    #     return MenuGenerator()

if __name__ == '__main__':
    MenuGeneratorApp().run()