from datetime import date, timedelta

from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.tab import MDTabsBase
from kivy.properties import StringProperty
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem, MDList, OneLineListItem, TwoLineAvatarListItem, BaseListItem
from kivymd.icon_definitions import md_icons
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelTwoLine, MDExpansionPanelThreeLine
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
            
            tab = Tab(title=day_title)
            for i in range(3):
                tab.ids.box.add_widget(
                    OneLineListItem(text=f"Meal {i+1} on day {tab.title}")
                )
                panel = MDExpansionPanel(
                    icon= 'language-python',
                    content=Content(text=f"Recipe instructions for recipe {i+1} on day {tab.title}"),
                    panel_cls=MDExpansionPanelTwoLine(
                        text=f"Recipe {i+1}",
                        secondary_text="Secondary text"
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
    # def build(self):
    #     return MenuGenerator()

if __name__ == '__main__':
    MenuGeneratorApp().run()