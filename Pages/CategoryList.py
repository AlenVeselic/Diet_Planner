import pprint
from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page
import DietPlanner


class CategoryFrame(Frame):
    category = None
    parentCategory = None
    parent = None
    root = None
    page = None

    def __init__(
        self,
        parent,
        category,
        categories,
        root,
        page,
        overrideName=None,
        overrideParent=None,
    ):
        Frame.__init__(self, parent)

        self.category = category
        self.parent = parent
        self.root = root
        self.page = page

        if overrideName:
            nameLabel = ttk.Label(self, text=overrideName)
            nameLabel.pack(side=LEFT)
        else:
            nameLabel = ttk.Label(self, text=self.category["name"])

        nameLabel.pack(side=LEFT)

        if self.category:
            self.parentCategory = DietPlanner.getCategoryFromId(
                categories, self.category["parent_id"]
            )

        if overrideParent:
            parentNameLabel = ttk.Label(self, text=overrideParent)
        elif self.parentCategory:
            parentNameLabel = ttk.Label(self, text=self.parentCategory["name"])
        else:
            parentNameLabel = ttk.Label(self, text="None")
        parentNameLabel.pack(side=LEFT)

        editButton = ttk.Button(
            self,
            text="edit",
            command=lambda: [
                self.page.refresh(),
                self.update(),
                # self.root.pages["AddEditFood"].show(),
                # self.root.pages["AddEditFood"].setItemToEdit(item),
            ],
        )

        editButton.pack(side=RIGHT)

        if self.parentCategory:
            trashButton = ttk.Button(
                self,
                text="trash",
                command=lambda: [
                    self.page.refresh(),
                    self.update(),
                    # self.root.pages["DeleteItem"].show(),
                    # self.root.pages["DeleteItem"].setItemToDelete(item),
                    # self.root.pages["DeleteItem"].refresh(),
                ],
            )
            trashButton.pack(side=RIGHT)


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
            categoryHeaderFrame = CategoryFrame(
                self.categoryListFrame,
                None,
                self.categories,
                self.root,
                self,
                overrideName="Category Name",
                overrideParent="Parent Category",
            )
            categoryHeaderFrame.pack(side=TOP, expand=True, fill="x")
            self.categoryWidgets.append(categoryHeaderFrame)

            for category in self.categories:
                categoryFrame = CategoryFrame(
                    self.categoryListFrame, category, self.categories, self.root, self
                )
                categoryFrame.pack(side=TOP, expand=True, fill="x")
                self.categoryWidgets.append(categoryFrame)

    def refresh(self):
        self.categories = DietPlanner.getCategories()

        for widget in self.categoryListFrame.winfo_children():
            widget.destroy()

        self.categoryWidgets = []
        categoryHeaderFrame = CategoryFrame(
            self.categoryListFrame,
            None,
            self.categories,
            self.root,
            self,
            overrideName="Category Name",
            overrideParent="Parent Category",
        )
        categoryHeaderFrame.pack(side=TOP, expand=True, fill="x")

        for category in self.categories:
            categoryFrame = CategoryFrame(
                self.categoryListFrame, category, self.categories, self.root, self
            )
            categoryFrame.pack(side=TOP, expand=True, fill="x")
            self.categoryWidgets.append(categoryFrame)

        self.root.update()
