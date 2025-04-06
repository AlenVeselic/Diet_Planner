import pprint
from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page
import dietPlanner


class CategoryList(Page):

    categories = None
    categoryListFrame = None

    categoryWidgets: list[Widget] = []

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        self.label = Label(self.frame, text="Category List")
        self.label.pack(side="top", fill="both", expand=True)

        self.categoryListFrame = ttk.Frame(self.frame)
        self.categoryListFrame.pack(side="top", fill="both", expand=True)

        if not self.categories:
            noCategoriesLabel = Label(
                self.categoryListFrame, text="There are no categories"
            )
            noCategoriesLabel.pack(side=TOP, expand=True, fill="x")
            self.categoryWidgets.append(noCategoriesLabel)
        else:
            for category in self.categories:
                categoryLabel = Label(self.categoryListFrame, text=category["name"])
                categoryLabel.pack(side=TOP, expand=True, fill="x")
                self.categoryWidgets.append(categoryLabel)

    def refresh(self):
        self.categories = dietPlanner.getCategories()

        for widget in self.categoryWidgets:
            widget.pack_forget()

        self.categoryWidgets = []
        for category in self.categories:
            categoryLabel = Label(self.categoryListFrame, text=category["name"])
            categoryLabel.pack(side=TOP, expand=True, fill="x")
            self.categoryWidgets.append(categoryLabel)

        self.root.update()
