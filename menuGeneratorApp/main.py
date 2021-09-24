from datetime import date, timedelta

from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase

class MenuGenerator(MDBoxLayout):
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

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        '''Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''

        instance_tab.ids.container.text = tab_text
    pass
    # def build(self):
    #     return MenuGenerator()

if __name__ == '__main__':
    MenuGeneratorApp().run()