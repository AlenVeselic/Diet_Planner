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

    debugNavigationButtons = []

    pages: dict[str, Page] = {}

    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)

        pageDefinitions: dict = {
            "DeleteItem": DeleteItemPage,
            "DietPlan": DietPlanPage,
            "FoodList": FoodListPage,
            "AddEditFood": AddEditFoodItem,
            "DietPlanArchive": DietPlanArchive,
            "ActiveDietPlan": ActiveDietPlan,
            "Profile": Profile,
            "Settings": Settings,
            "CategoryList": CategoryList,
            "ModifySubcategory": ModifySubcategory,
        }

        for definition in pageDefinitions.keys():
            self.pages[definition] = pageDefinitions[definition](self, root)

        buttonframe = ttk.Frame(self)
        container = ttk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        for page in self.pages.keys():
            self.pages[page].place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        self.debugNavigationButtons = [
            {"text": "Delete Item", "command": self.pages["DeleteItem"].show},
            {"text": "Create diet plan", "command": self.pages["DietPlan"].show},
            {
                "text": "Food list",
                "command": lambda: [
                    self.pages["FoodList"].refresh(),
                    self.pages["FoodList"].show(),
                ],
            },
            {"text": "Create new food", "command": self.pages["AddEditFood"].show},
            {
                "text": "Diet Plan Archive",
                "command": lambda: [
                    self.pages["DietPlanArchive"].show(),
                    self.pages["DietPlanArchive"].refresh(),
                ],
            },
            {"text": "Active Diet Plan", "command": self.pages["ActiveDietPlan"].show},
            {"text": "Profile", "command": self.pages["Profile"].show},
            {"text": "Settings", "command": self.pages["Settings"].show},
            {
                "text": "Category List",
                "command": lambda: [
                    self.pages["CategoryList"].refresh(),
                    self.pages["CategoryList"].show(),
                ],
            },
            {
                "text": "Modify Subcategory",
                "command": self.pages["ModifySubcategory"].show,
            },
        ]

        for buttonDefinition in self.debugNavigationButtons:
            button = Button(
                buttonframe,
                text=buttonDefinition["text"],
                command=buttonDefinition["command"],
            )
            button.pack(side=LEFT)

        self.pages["DeleteItem"].show()



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
