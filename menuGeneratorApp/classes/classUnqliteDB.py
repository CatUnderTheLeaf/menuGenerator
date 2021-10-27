from datetime import date, timedelta
from unqlite import UnQLite

class UnqliteDB:
    
    def __init__(self, params):
        self.db = UnQLite(params)
        self.products = self.db.collection('products')
        self.products.create() 
        
        print(self.products.all())
        self.recipes = self.db.collection('recipes')
        self.recipes.create() 
        print(self.recipes.all())

    def disconnect(self):
        self.db.close()
