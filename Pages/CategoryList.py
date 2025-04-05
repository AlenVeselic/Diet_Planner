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

        self.canvas = Canvas(self, borderwidth=0, background="white")

        self.pageFrame = ttk.Frame(self.canvas, padding="5")
        # self.foodFrame.pack(side="top", fill="both", expand=True)

        self.verticalScrollBar = Scrollbar(
            self, orient=VERTICAL, command=self.canvas.yview
        )

        self.canvas.configure(yscrollcommand=self.verticalScrollBar.set)

        self.verticalScrollBar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas.create_window(
            (4, 4), window=self.pageFrame, anchor=NW, tags="self.foodFrame"
        )

        self.pageFrame.bind("<Configure>", self.onFrameConfigure)

        self.label = Label(self.pageFrame, text="Category List")
        self.label.pack(side="top", fill="both", expand=True)

        self.categoryListFrame = ttk.Frame(self.pageFrame)
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

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

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
