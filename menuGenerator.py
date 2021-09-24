from datetime import date, timedelta
import os

from classes.classMenu import Menu

p = os.path.dirname(__file__)

# Create Menu object
menu = Menu(p)

# generate menu for n+1 days applying rules
n = 10
sdate = date.today()
edate = sdate + timedelta(days=n)
menu.generateDailyMenu(sdate, edate)
print(menu)