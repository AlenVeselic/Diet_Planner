#! python3

# dietPlannerInterface.py - simple tkinter interface made to put the functions in dietPlanner.py to use in a visual manner

# import all needed things: tkinter for gui generationm, dietPlanner for backend operations, logginf for debug
from tkinter import *

import ttkbootstrap as ttk

import dietPlanner
import logging

from Pages.Page_Class import Page

from Pages.Page1 import Page1
from Pages.Page2 import Page2
from Pages.Page3 import Page3
from Pages.DietPlannerList import DietPlannerList

# getSubcategories - refreshes data and retrieves subcategories for the currently selected category


# refreshes the global food database
def refreshData(*args):
    foodData = dietPlanner.getShelve()


class MainView(Frame):
    p1 = None
    p3 = None
    dietPlannerListPage = None

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.p1 = Page1(self, root)
        p2 = Page2(self, root)
        self.p3 = Page3(self, root)
        self.dietPlannerListPage = DietPlannerList(self, root)

        buttonframe = Frame(self)
        container = Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        self.p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.dietPlannerListPage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = Button(buttonframe, text="Page 1", command=self.p1.show)
        b2 = Button(buttonframe, text="Create diet plan", command=p2.show)
        b3 = Button(
            buttonframe,
            text="Food list",
            command=lambda: [self.p3.refresh(), self.p3.show()],
        )
        b4 = Button(
            buttonframe, text="Create new food", command=self.dietPlannerListPage.show
        )

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(
            side="left",
        )

        self.p1.show()


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
