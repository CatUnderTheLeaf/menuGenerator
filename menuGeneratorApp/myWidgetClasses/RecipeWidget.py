import os
import math
import datetime
from classes.classLang import tr

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.expansionpanel import MDExpansionPanelOneLine

from kivy.metrics import dp
from kivy.core.window import Window
from kivy.properties import (
    ObjectProperty
)

from kivy.utils import platform

from myWidgetClasses.customButtons import ButtonWithCross
from myWidgetClasses.myExpansionPanel import IngredientsExpansionPanel
from myWidgetClasses.otherWidgetClasses import dialogItem, BottomCustomSheet, ContentCustomSheet

class RecipeWidget(MDBoxLayout):
    recipe = ObjectProperty()
    parentWidget = ObjectProperty()
    recipe_scroll = ObjectProperty()
    dialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        # file manager
        self.file_manager_open = False
        # Camera manager
        self.camera_manager_open = False

        if self.parentWidget:
            self.ids.recipeTitle.text = self.recipe.title
            # load new ingredients
            for ingredient, amount in self.recipe.ingredients.items():
                self.ids.recipeIngredients.add_widget(ButtonWithCross(
                                            text=ingredient,
                                            amount=amount,
                                            input=True, 
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
            if chip.value==value:
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
            self.recipe.ingredients = {}
            for ingredient in self.ids.recipeIngredients.children:
                self.recipe.ingredients[ingredient.text] = ingredient.ids.ingredientAmount.text
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
    
    '''
    get tags that are not used,
    no need to show same tags

    :param currentTags: tags used in recipe
    '''
    def getUnusedTags(self, currentTags):
        # Tags are in RecipeSelectionList
        allTags = set(self.recipe_scroll.tags)
        return list(allTags - set(currentTags))

    '''
    refresh dropdown items for tag search

    :param textField: tags text field
    :param recipeWidget: recipe Widget with recycle view
    '''
    def refresh(self, text, textField):
        def add_tag_item(tag):
            self.ids.rv.data.append(
                {
                    "viewclass": "OneLineListItem",
                    "text": tag,
                    "on_release": lambda x=tag: self.set_item(x, textField)
                }
            )

        if len(text) > 0:
            self.ids.rv.data = []
            currentTags = []
            for tag in self.ids.recipeTags.children:
                currentTags.append(tag.text)
            for tag in self.getUnusedTags(currentTags):
                if text in tag:
                    add_tag_item(tag)            
        else:
            self.ids.rv.data = []
        
        if self.ids.rv.data:
                self.ids.rv.parent.height = dp(205)
        else:
            self.ids.rv.parent.height = 0
    
    '''
    add new tag to the tags stackLayout

    :param text__item: string text
    :param textField: tags text field
    :param recipeWidget: recipe Widget with recycle view
    '''
    def set_item(self, text__item, textField):
        text = ' '.join(text__item.split())
        if len(text):
            textField.focus = False
            textField.text = ''
            self.ids.rv.data = []
            self.ids.rv.parent.height = 0
            self.ids.recipeTags.add_widget(ButtonWithCross(
                                                text=text,
                                                parentId=self.ids.recipeTags))

    ''' 
    show Bottom Sheet with ingredients 
    grouped by category
    '''
    def show_ingredients_bottom_sheet(self):
        ingredientWidget = self.ids.recipeIngredients
        products = self.recipe_scroll.products
        custom_sheet = BottomCustomSheet()   
        for category in products:
            cat_text = ''
            if ',' in category:
                cat_text = ', '.join(tr._(w).capitalize() for w in category.split(','))
            elif '_' in category:
                cat_text = tr._(' '.join(category.split('_'))).capitalize()
            else:
                cat_text = tr._(category).capitalize()
            panel = IngredientsExpansionPanel(
                        products=products[category],
                        ingredientWidget=ingredientWidget,
                        content=ContentCustomSheet(rows=math.ceil(len(products[category])/2)), 
                        panel_cls=MDExpansionPanelOneLine(
                            text=f"{cat_text}"
                        )
                    )
            custom_sheet.ids.custom_sheet_grid.add_widget(panel)
        self.custom_sheet = MDCustomBottomSheet(screen=custom_sheet, radius_from="top")
        self.custom_sheet.open()

    ''' 
    show Dialog to set recipe image 
    '''
    def show_set_image_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title=tr._("Set recipe image"),
                type="simple",
                items=[
                    dialogItem(text=tr._("Choose from gallery"), icon='image', on_release=lambda x: (
                                self.dialog.dismiss(), 
                                self.open_gallery()
                                )),
                    dialogItem(text=tr._("Take a picture"), icon='camera', on_release=lambda x: (
                                self.dialog.dismiss(), 
                                self.get_camera()
                                )),
                ],
            )
        self.dialog.open()
    
    ''' 
    open FileManager and show images
    '''
    def open_gallery(self):
        def check_filechooser_permission():
            """
            Android runtime `STORAGE` permission check.
            """
            if not platform == 'android':
                return True
            from android.permissions import Permission, check_permission
            return (check_permission(Permission.WRITE_EXTERNAL_STORAGE) and 
                    check_permission(Permission.READ_EXTERNAL_STORAGE))

        def check_request_filechooser_permission(callback=None):
            """
            Android runtime `STORAGE` permission check & request.
            """
            had_permission = check_filechooser_permission()
            if not had_permission:
                from android.permissions import Permission, request_permissions
                permissions = [Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE]
                request_permissions(permissions, callback)
            return had_permission

        def on_permissions_callback(permissions, grant_results):
            if all(grant_results):
                self.open_filechooser()
                
        if check_request_filechooser_permission(callback=on_permissions_callback):
            self.open_filechooser()

    def open_filechooser(self):
        if platform == "android":
            from android.storage import primary_external_storage_path 
            path = os.path.join(primary_external_storage_path(), 'Pictures')
            from plyerAndroidClasses.filechooser import AndroidFileChooser
            filechooser = AndroidFileChooser()
            filechooser.open_file(path=path, on_selection=self.select_path, filters=["image", "*jpg", "*png"], preview=True)
            self.file_manager_open = True
        else:
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "img/")
            print("Here should be fileChooser")
        
    
    '''
    It will be called when you click on the file name
    or the catalog selection button.

    :type path: str;
    :param path: path to the selected directory or file;
    '''   
    def select_path(self, path):
        self.exit_file_manager()
        if os.path.isfile(path[0]):
            self.ids.recipeImg.source = path[0]

    '''
    Called when the user reaches the root of the directory tree.
    '''
    def exit_file_manager(self, *args):
        self.file_manager_open = False

    '''
    Called when buttons are pressed on the mobile device.
    '''
    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            print("Buttons were pressed")
        return True
    
    '''
    Called when the user closes camera.
    '''
    def exit_camera_manager(self, filepath):
        self.camera_manager_open = False
        if(os.path.exists(filepath)):
            if (os.path.getsize(filepath)!=0):
                self.ids.recipeImg.source = filepath
            else:
                os.remove(filepath)
        else:
            print("unable to save.")

    '''
    Called when user choose to use camera.
    '''
    def get_camera(self):

        def check_camera_permission():
            """
            Android runtime `CAMERA` permission check.
            """
            if not platform == 'android':
                return True
            from android.permissions import Permission, check_permission
            permission = Permission.CAMERA
            return check_permission(permission)

        def check_request_camera_permission(callback=None):
            """
            Android runtime `CAMERA` permission check & request.
            """
            had_permission = check_camera_permission()
            if not had_permission:
                from android.permissions import Permission, request_permissions
                permissions = [Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE]
                request_permissions(permissions, callback)
            return had_permission

        def on_permissions_callback(permissions, grant_results):
            if all(grant_results):
                self.take_camera_picture()
                
        if check_request_camera_permission(callback=on_permissions_callback):
            self.take_camera_picture()

    def take_camera_picture(self):        
        if platform == "android":
            from android.storage import primary_external_storage_path
            dstpath = os.path.join(primary_external_storage_path(), 'Pictures', 'MenuGenerator')
            if not os.path.isdir(dstpath):
                os.mkdir(dstpath)

            self.camera_manager_open = True

            from plyerAndroidClasses.camera import AndroidCamera
            file_name = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S.jpg')
            camera = AndroidCamera()            
            camera.take_picture(filename=os.path.join(dstpath, file_name),
                            on_complete=self.exit_camera_manager)       
        else:
            dstpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "img/")
            print("Here should be camera opened")

        