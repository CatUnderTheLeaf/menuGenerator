import os
from pathlib import Path
from datetime import date, timedelta
import sqlite3

MENU_DB = 'db/menuDB.db'

class MenuDB:
    
    def __init__(self, parent_path):
        self.con = sqlite3.connect(os.path.join(parent_path, MENU_DB))
        self.cur = self.con.cursor()
    
    def disconnect(self):
        self.con.close()
