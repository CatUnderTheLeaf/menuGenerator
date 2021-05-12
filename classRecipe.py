# a class that represent a single recipe

class Recipe:
    def __init__(self, title="", ingridients=[], prepareTime="short", text=""):        
        self.title = title
        # TODO later implement, now it is not so important
        # self.img = img
        self.ingridients = ingridients
        self.prepareTime = prepareTime
        self.description = text     