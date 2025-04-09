#! python3

# dietPlannerInterface.py - simple tkinter interface made to put the functions in dietPlanner.py to use in a visual manner

# import all needed things: tkinter for gui generationm, dietPlanner for backend operations, logginf for debug
from tkinter import *

import ttkbootstrap as ttk

import dietPlanner
import logging

from Pages.Page_Class import Page

from Pages.DeleteItemPage import DeleteItemPage
from Pages.DietPlan import DietPlanPage
from Pages.FoodListPage import FoodListPage
from Pages.AddEditFoodItem import AddEditFoodItem
from Pages.DietPlanArchive import DietPlanArchive
from Pages.ActiveDietPlan import ActiveDietPlan
from Pages.Profile import Profile
from Pages.Settings import Settings
from Pages.CategoryList import CategoryList
from Pages.ModifySubcategory import ModifySubcategory

# getSubcategories - refreshes data and retrieves subcategories for the currently selected category


# refreshes the global food database
def refreshData(*args):
    foodData = dietPlanner.getShelve()


class MainView(ttk.Frame):
    deleteItemPage = None
    foodList = None
    addEditFoodItemPage = None
    dietPlanArchive = None
    activeDietPlan = None

    debugNavigationButtons = []

    pages = []

    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.deleteItemPage = DeleteItemPage(self, root)
        dietPlan = DietPlanPage(self, root)
        self.foodList = FoodListPage(self, root)
        self.addEditFoodItemPage = AddEditFoodItem(self, root)
        self.dietPlanArchive = DietPlanArchive(self, root)
        self.activeDietPlan = ActiveDietPlan(self, root)
        profile = Profile(self, root)
        settings = Settings(self, root)
        categoryList = CategoryList(self, root)
        modifySubcategory = ModifySubcategory(self, root)
        
        self.pages = [self.deleteItemPage, dietPlan, self.foodList, self.addEditFoodItemPage, self.dietPlanArchive, self.activeDietPlan, profile, settings, categoryList, modifySubcategory]


        buttonframe = ttk.Frame(self)
        container = ttk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        for page in self.pages:
            page.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        self.debugNavigationButtons = [{"text": "Delete Item", "command": self.deleteItemPage.show}, {"text": "Create diet plan", "command": dietPlan.show}, {"text": "Food list",
            "command": lambda: [self.foodList.refresh(), self.foodList.show()]}, 
            {"text": "Create new food", "command": self.addEditFoodItemPage.show}
    , 
            {"text": "Diet Plan Archive",
            "command": lambda: [
                self.dietPlanArchive.show(),
                self.dietPlanArchive.refresh(),
            ]
            },
        
            {"text": "Active Diet Plan", "command": self.activeDietPlan.show}
        , {"text": "Profile", "command": profile.show}, {"text": "Settings", "command": settings.show}, 
            {"text": "Category List",
            "command": lambda: [categoryList.refresh(), categoryList.show()],
            },
        
            {"text": "Modify Subcategory", "command": modifySubcategory.show}
         
        ]

        for buttonDefinition in self.debugNavigationButtons:
            button = Button(buttonframe, text=buttonDefinition["text"], command=buttonDefinition["command"])
            button.pack(side=LEFT)

        self.deleteItemPage.show()


# if __name__ == "__main__":

#     # gui initialization


#     #  mainloop initiation
#     root.mainloop()

if __name__ == "__main__":
    # logging basic configuration initialization

    logging.basicConfig(
        level=logging.DEBUG, format=(" %(levelname)s - %(asctime)s - %(message)s")
    )

    root = ttk.Window(themename="journal")

    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)

    root.wm_geometry("400x400")
    root.mainloop()
