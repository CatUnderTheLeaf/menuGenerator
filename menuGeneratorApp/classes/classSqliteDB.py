from datetime import date, timedelta
import sqlite3

class SqliteDB:
    
    def __init__(self, path, dic):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS products
               (product_id INTEGER PRIMARY KEY, product TEXT, food_class TEXT)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS recipes
               (recipe_id INTEGER PRIMARY KEY, title TEXT, img TEXT, ingredients TEXT, prepareTime TEXT, description TEXT, tags TEXT, repeat TEXT, food_class TEXT, nutrients TEXT)''')
        
        # print(dic)
        # self.title = title
        # self.img = img
        # self.ingredients = ingredients
        # self.food_class = food_class
        # self.nutrients = nutrients
        # self.prepareTime = prepareTime
        # self.description = text
        # self.tags = tags
        # self.repeat = repeat
        # l = [(rec.title, ','.join(rec.ingredients), rec.prepareTime, rec.description, ','.join(rec.tags), rec.repeat, ','.join(rec.food_class), ','.join(rec.nutrients)) for rec in dic]
        # print(l)
      
        # self.cur.executemany("INSERT INTO recipes (title, ingredients, prepareTime, description, tags, repeat, food_class, nutrients) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", l)
        # self.con.commit()
        for row in self.cur.execute('SELECT * FROM recipes ORDER BY recipe_id'):
            print(row)

    
    def disconnect(self):
        self.con.close()
