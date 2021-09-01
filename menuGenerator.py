from datetime import date, timedelta

from classMenu import Menu

# Create Menu object
menu = Menu()

# generate menu for n+1 days applying rules
n = 10
sdate = date.today()
edate = sdate + timedelta(days=n)
menu.generateDailyMenu(sdate, edate)
# print(menu)
# print(menu.menu)