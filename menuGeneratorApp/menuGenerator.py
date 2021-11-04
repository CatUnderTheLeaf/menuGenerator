from datetime import date, timedelta
import os

from classes.classMenu import Menu

# Create Menu object

import yaml
with open(os.path.join(os.path.dirname(__file__), "app_settings.yml"), 'r') as stream:
    data_loaded = yaml.safe_load(stream)

db = data_loaded['DB_TYPE']
db_path = os.path.join(os.path.dirname(__file__), data_loaded['MENU_DB'])

menu = Menu()
menu.connectDB(db, db_path)

# generate menu for n+1 days applying rules
n = 10
sdate = date.today()
edate = sdate + timedelta(days=n)
meals = {"0": "Breakfast", "2": "Lunch", "4": "Dinner"}
for key in meals:
    menu.update_mpd(int(key), meals[key])

# menu.generateDailyMenu(sdate, edate)
# print(menu)
products = menu.db.getProducts()
print(products)

menu.disconnectDB()