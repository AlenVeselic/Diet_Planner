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
            categoryHeaderFrame = ttk.Frame(self.categoryListFrame)
            nameHeaderLabel = Label(categoryHeaderFrame, text="Category Name")
            nameHeaderLabel.pack(side=LEFT, expand=True)
            parentHeaderLabel = Label(categoryHeaderFrame, text="Parent Category")
            parentHeaderLabel.pack(side=LEFT, expand=True)
            categoryHeaderFrame.pack(side=TOP, expand=True, fill="x")
            self.categoryWidgets.append(categoryHeaderFrame)

            for category in self.categories:
                categoryFrame = ttk.Frame(self.categoryListFrame)
                categoryLabel = Label(categoryFrame, text=category["name"])
                categoryLabel.pack(side=LEFT, expand=True)
                parentCategory = dietPlanner.getCategoryFromId(self.categories,category["parent_id"])
                if parentCategory:
                    categoryParentLabel = Label(
                        categoryFrame, text=parentCategory["name"]
                    )
                else:
                    categoryParentLabel = Label(categoryFrame, text="None")
                categoryParentLabel.pack(side=LEFT, expand=True)
                categoryFrame.pack(side=TOP, expand=True, fill="x")
                self.categoryWidgets.append(categoryFrame)

    def refresh(self):
        self.categories = dietPlanner.getCategories()

        for widget in self.categoryListFrame.winfo_children():
            widget.destroy()

        self.categoryWidgets = []
        categoryHeaderFrame = ttk.Frame(self.categoryListFrame)
        nameHeaderLabel = Label(categoryHeaderFrame, text="Category Name")
        nameHeaderLabel.pack(side=LEFT, expand=True)
        parentHeaderLabel = Label(categoryHeaderFrame, text="Parent Category")
        parentHeaderLabel.pack(side=LEFT, expand=True)
        categoryHeaderFrame.pack(side=TOP, expand=True, fill="x")

        for category in self.categories:
            categoryFrame = ttk.Frame(self.categoryListFrame)
            categoryLabel = Label(categoryFrame, text=category["name"])
            categoryLabel.pack(side=LEFT, expand=True)
            parentCategory = dietPlanner.getCategoryFromId(self.categories,category["parent_id"])
            if parentCategory:
                categoryParentLabel = Label(
                    categoryFrame, text=parentCategory["name"]
                )
            else:
                categoryParentLabel = Label(categoryFrame, text="None")
            categoryParentLabel.pack(side=LEFT, expand=True)
            categoryFrame.pack(side=TOP, expand=True, fill="x")
            self.categoryWidgets.append(categoryFrame)

        self.root.update()
