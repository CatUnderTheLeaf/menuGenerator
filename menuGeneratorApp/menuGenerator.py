from datetime import date, timedelta
import os

from classes.classMenu import Menu
from classes.classMenuDB import MenuDB

p = os.path.dirname(__file__)



# Create Menu object
menu = Menu(p)

MENU_DB = 'db/menuDB.db'

# menuDB = MenuDB('sqlite', os.path.join(os.path.dirname(__file__), MENU_DB), menu.recipeList)
# menuDB.disconnect()

MENU_UnqliteDB = 'db/menuUnqliteDB.db'
menuDB = MenuDB('unqlite', os.path.join(os.path.dirname(__file__), MENU_UnqliteDB))
menuDB.disconnect()

# generate menu for n+1 days applying rules
# n = 10
# sdate = date.today()
# edate = sdate + timedelta(days=n)
# menu.generateDailyMenu(sdate, edate)
# print(menu)