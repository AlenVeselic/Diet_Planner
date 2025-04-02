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
from Pages.DietPlannerList import DietPlannerList
from Pages.DietPlanArchive import DietPlanArchive
from Pages.ActiveDietPlan import ActiveDietPlan
from Pages.Profile import Profile
from Pages.Settings import Settings
from Pages.CategoryList import CategoryList
from Pages.ModifySubcategoy import ModifySubcategory

# getSubcategories - refreshes data and retrieves subcategories for the currently selected category


# refreshes the global food database
def refreshData(*args):
    foodData = dietPlanner.getShelve()


class MainView(ttk.Frame):
    deleteItemPage = None
    foodList = None
    dietPlannerListPage = None

    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.deleteItemPage = DeleteItemPage(self, root)
        dietPlan = DietPlanPage(self, root)
        self.foodList = FoodListPage(self, root)
        self.dietPlannerListPage = DietPlannerList(self, root)
        dietPlanArchive = DietPlanArchive(self, root)
        activeDietPlan = ActiveDietPlan(self, root)
        profile = Profile(self, root)
        settings = Settings(self, root)
        categoryList = CategoryList(self, root)
        modifySubcategory = ModifySubcategory(self, root)

        buttonframe = ttk.Frame(self)
        container = ttk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        self.deleteItemPage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        dietPlan.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.foodList.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.dietPlannerListPage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        dietPlanArchive.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        activeDietPlan.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        profile.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        settings.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        categoryList.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        modifySubcategory.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = Button(buttonframe, text="Delete Item", command=self.deleteItemPage.show)
        b2 = Button(buttonframe, text="Create diet plan", command=dietPlan.show)
        b3 = Button(
            buttonframe,
            text="Food list",
            command=lambda: [self.foodList.refresh(), self.foodList.show()],
        )
        b4 = Button(
            buttonframe, text="Create new food", command=self.dietPlannerListPage.show
        )
        dietPlanArchiveButton = Button(
            buttonframe, text="Diet Plan Archive", command=dietPlanArchive.show
        )

        activeDietPlanButton = Button(
            buttonframe, text="Active Diet Plan", command=activeDietPlan.show
        )
        profileButton = Button(buttonframe, text="Profile", command=profile.show)
        settingsButton = Button(buttonframe, text="Settings", command=settings.show)
        categoryListButton = Button(
            buttonframe, text="Category List", command=categoryList.show
        )
        modifySubcategoryButton = Button(
            buttonframe, text="Modify Subcategory", command=modifySubcategory.show
        )

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")
        dietPlanArchiveButton.pack(side=LEFT)
        activeDietPlanButton.pack(side=LEFT)
        profileButton.pack(side=LEFT)
        settingsButton.pack(side=LEFT)
        categoryListButton.pack(side=LEFT)
        modifySubcategoryButton.pack(side=LEFT)

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
