import os

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager

from kivy.core.window import Window
from kivy.properties import (
    ObjectProperty
)

from myWidgetClasses.buttonWithCross import ButtonWithCross
from myWidgetClasses.otherWidgetClasses import dialogItem

class RecipeWidget(MDBoxLayout):
    recipe = ObjectProperty()
    parentWidget = ObjectProperty()
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True
        )
        # initValues are saved separately
        # so we can check if smth was changed
        if self.parentWidget:
            self.ids.recipeTitle.text = self.recipe.title
            # load new ingredients
            for ingredient in self.recipe.ingredients:
                self.ids.recipeIngredients.add_widget(ButtonWithCross(
                                            text=ingredient,
                                            parentId=self.ids.recipeIngredients))
                
            # set recipe prepare
            self.setChooseChip(self.ids.recipePrepareTime, self.recipe.prepareTime)
            
            # set if recipe can be used on two consecutive days
            self.ids.recipeRepeatDish.active = self.recipe.repeat

            # load new tags
            for tag in self.recipe.tags:
                self.ids.recipeTags.add_widget(ButtonWithCross(
                                            text=tag,
                                            parentId=self.ids.recipeTags))
            
            self.ids.recipeDescription.text = self.recipe.description

    '''Check chip for prepareTime

    :param id: widget id, container of chips
    :param value: text of the chip;
    '''
    def setChooseChip(self, id, value):
        chips = id.children
        for chip in chips:
            if chip.text==value:
                chip.state = 'down'

    '''Save all recipe info 

    :return: Bool if recipe can be saved
    '''    
    def saveRecipe(self):
        # form recipe data
        if self.ids.recipeTitle.text=='':
            self.ids.recipeTitle.error = True
            self.ids.recipeTitle.focus = True
            return False
        else:
            self.recipe.title = self.ids.recipeTitle.text
            self.recipe.img = self.ids.recipeImg.source
            self.recipe.ingredients = []
            for ingredient in self.ids.recipeIngredients.children:
                self.recipe.ingredients.append(ingredient.text)
            self.recipe.prepareTime = "short"
            for prepareTime in self.ids.recipePrepareTime.children:
                if prepareTime.state=='down':
                    self.recipe.prepareTime = prepareTime.text
            self.recipe.tags = []
            for tag in self.ids.recipeTags.children:
                self.recipe.tags.append(tag.text)
            self.recipe.repeat = self.ids.recipeRepeatDish.active
            self.recipe.description = self.ids.recipeDescription.text
            return True
    
    def show_set_image_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Set recipe image",
                type="simple",
                items=[
                    dialogItem(text="Choose from gallery", icon='image', parentWidget = self),
                    dialogItem(text="Take a picture", icon='camera', parentWidget = self)
                ],
            )
        self.dialog.open()
    
    def open_gallery(self):
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "img/")
        self.file_manager.show(path)  # output manager to the screen
        self.manager_open = True
       
    def select_path(self, path):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''

        self.exit_manager()
        self.setRecipeImage(path)

    def setRecipeImage(self, path):
        if os.path.isfile(path):
            self.ids.recipeImg.source = path

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def open_camera(self):
        print("camera")

    '''
        Found out on android.developers that actually for "All files" is needed the permission MANAGE_EXTERNAL_STORAGE.

Just put in buildozer.spec file MANAGE_EXTERNAL_STORAGE also:

(list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE No need to put it in the py code as you mnetioned for the other other permissions. they are ok in the code to avoit asking for the permission every time the app is launched.

But, after the app is installed you'll have to go on the app permission to all the management of all files allow permission

Worked for me, hope it helps.
You need to change self.file_manager.show('/') to

self.file_manager.show(primary_ext_storage)
where primary_ext_storage is the file directory on your android phone. You also need to declare below.

from android.storage import primary_external_storage_path
primary_ext_storage = primary_external_storage_path()
primary_external_storage_path() returns Android’s so-called “primary external storage”, often found at /sdcard/ and potentially accessible to any other app. It compares best to the Documents directory on Windows.

On top of that, you need to add the following code in your script to ensure there is permission to access to the storage on the phone.

from android.permissions import request_permissions, Permission
request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
Do not be confused by the name of primary_ext_storage . It is not referring to your android phone SD card. Instead, it will be pointing to your internal storage.

For external storage on android phone, you can use

from android.storage import secondary_external_storage_path
secondary_ext_storage = secondary_external_storage_path()
        '''
