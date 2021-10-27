import os
from pathlib import Path
from datetime import date, timedelta
from classes.classSqliteDB import SqliteDB
from classes.classUnqliteDB import UnqliteDB

class MenuDB:
    
    def __init__(self, type, param):
        if type=='sqlite':
            self.db = SqliteDB(param)
        if type=='unqlite':
            self.db = UnqliteDB(param)
    
    def disconnect(self):
        self.db.disconnect()
