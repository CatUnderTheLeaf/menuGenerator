from datetime import date, timedelta
from classes.classRecipe import Recipe
import jsons

from classes.classMenuDB import MenuDB
""" 
a class that represent a list of recipes,
has a bunch of useful filtering and randomizing functions
 """

class Menu:
    """ 
    mpd: meals per day
    menu: dict of recipes per meals
    n: number of days
    repeatDishes: if dishes can be eaten on more than one day
    
    """
    menu = {}
    
    @property
    def mpd(self):
        sorted_keys = sorted(self._mpd.keys())
        return [self._mpd[key] for key in sorted_keys]

    def update_mpd(self, meals):
        self._mpd = meals

    def __init__(self):
        self._mpd = {}
        self.n = 1
        self.timePeriod = "day"
        self.repeatDishes = True

    def connectDB(self, db_type, db_path):
        self.db = MenuDB(db_type, db_path)

    def disconnectDB(self):
        self.db.disconnect()

    def __repr__(self):
       return repr(self.db.getRecipes())

    def __str__(self):
        menu = []
        menu.append("!!!-----------------generated menu----------------!!!")
        for day_str in self.menu:
            day = date.fromisoformat(day_str)
            menu.append("\n{}, {}:".format(day, day.strftime("%a")))
            for meal in self.mpd:
                if meal in self.menu[day_str]:
                    menu.append("{} - {}".format(meal, self.menu[day_str][meal]))
        return "\n".join(menu)
    
    """ 
    serialize Menu to JSON
    
    :return: JSON object
     """
    def toJson(self):
        jsonMenu = jsons.dump(self.menu)
        return jsonMenu

    """ 
    deserialize Menu from JSON

    :param genMenu: JSON object
    
     """
    def loadFromJson(self, genMenu):
        if genMenu:
            testMenu = {}
            for day_str in genMenu:
                testMenu[day_str] = {}
                testMenu[day_str]['prepTime'] = genMenu[day_str]['prepTime']
                for meal in self.mpd:
                    if meal in genMenu[day_str]:
                        testMenu[day_str][meal] = jsons.load(genMenu[day_str][meal], Recipe) if genMenu[day_str][meal] is not None else None
            self.menu = testMenu

    """ 
    generate Menu for n days

    :param sdate: start date
    :param edate: end date
    
     """
    def generateDailyMenu(self, sdate=date.today(), edate=date.today()):
        self.menu = {}
        self.n = (edate - sdate).days + 1
        days = [sdate + timedelta(days=i) for i in range(self.n)]
        
        self.db.generate_subsets(self.mpd)

        self.getEmptyMenu(days)
        self.discardMeals()
        self.fillMenu()
                
        return

    """ 
    generate empty menu with corresponding prep times

    :param days: calendar dates
    
     """
    def getEmptyMenu(self, days):
        prepTimes = self.db.getRules().getPrepTimes(days)
        self.menu = {day.isoformat(): {'prepTime': prepTimes[day]} for day in days}
        return

    """ 
    fill in the menu with discarded meals
    
     """
    def discardMeals(self):
        days = self.menu.keys()
        days_meals = self.db.getRules().filterDiscardedMeals(days)
        # discard meals if there are rules
        for (day, meals) in days_meals:
            for meal in meals:
                self.menu[day][meal] = None
        
        return

    """ 
    fill in the menu
    
     """
    def fillMenu(self):
        # for each meal/day get recipe from the corresponding subset
        for date in self.menu:
            for meal in self.mpd:
                if meal not in self.menu[date]:                    
                    cur_recipe = self.db.chooseRecipe(meal, self.menu[date]['prepTime'])
                    self.menu[date][meal] = cur_recipe
                    # if dishes can be repeated search for next available day and meal
                    if self.repeatDishes and cur_recipe and cur_recipe.repeat:
                        availableDay = self.findAvailableDay(date, cur_recipe)
                        if availableDay:
                            nextDate, nextMeal = availableDay
                            self.menu[nextDate][nextMeal] = cur_recipe
                # if recipe is already set delete it from all sets, 
                # so no two equal dishes in one day 
                else:
                    used_recipe = self.menu[date][meal]
                    if used_recipe is not None:
                        self.db.deleteRecipeFromSets(used_recipe)
        
        return

    """ 
    find next available slot in the menu for a dish
    which can be eaten more than one time

    :param old_date: day of recipe in Menu
    :param recipe: a recipe of the dish
    :return: tuple (day, meal) if slot is available
    """
    def findAvailableDay(self, old_date, recipe):
        dates = sorted(self.menu.keys())
        s_ind = dates.index(old_date)
        new_dates = dates[s_ind+1:]
        for date in new_dates:
            for meal in self.mpd:
                if meal not in self.menu[date]:                    
                    check = self.db.checkRecipe(recipe, self.db.subsets[meal]['tag'], self.db.subsets[meal]['nutr'], self.menu[date]['prepTime'])
                    if check:
                        return (date, meal)       
        return
        