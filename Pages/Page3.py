from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page
import dietPlanner


class Page3(Page):
    foodData = None
    currentLabels = None

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        self.foodData = dietPlanner.getShelve()
        # label = Label(self, text="This is page 3")
        # label.pack(side="top", fill="both", expand=True)

        foodFrame = ttk.Frame(self, padding="5")
        foodFrame.pack(side="top", fill="both", expand=True)
        # foodFrame.grid(column=1, row=1, sticky=(N, W, E, S))

        # mainCategoryBox["bg"] = "white"

        foodFrame.grid_columnconfigure(1, weight=1)
        foodFrame.grid_rowconfigure(2, weight=1)

        foodFrame.grid_columnconfigure(2, weight=1)
        foodFrame.grid_columnconfigure(3, weight=1)

        self.allFoodList = ttk.Frame(foodFrame, padding="5")
        self.allFoodList.grid(column=1, row=4, rowspan=4, sticky=(N, W, E, S))

        ttk.Label(self.allFoodList, text="All food items").pack()
        self.currentLabels = []
        for item in self.foodData["items"]:
            label = ttk.Label(self.allFoodList, text=item["name"])
            label.pack()
            self.currentLabels.append(label)

        foodFrame.grid_rowconfigure(0, weight=1)
        foodFrame.grid_columnconfigure(0, weight=1)
        foodFrame.grid_rowconfigure(4, weight=1)
        foodFrame.grid_columnconfigure(6, weight=1)

    def refresh(self):
        self.foodData = dietPlanner.getShelve()

        for label in self.currentLabels:
            label.pack_forget()

        self.currentLabels = []
        for item in self.foodData["items"]:
            label = ttk.Label(self.allFoodList, text=item["name"])
            label.pack()
            self.currentLabels.append(label)
