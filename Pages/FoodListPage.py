from tkinter import *
from tkinter import messagebox
import ttkbootstrap as ttk

from Pages.Page_Class import Page
import DietPlanner


class ItemFrame(Frame):
    item = None
    parent = None
    root = None
    page = None

    def __init__(self, parent, item, root, page):
        Frame.__init__(self, parent)

        self.item = item
        self.parent = parent
        self.root = root
        self.page = page

        label = ttk.Label(self, text=self.item["name"])
        label.pack(side=LEFT)

        editButton = ttk.Button(
            self,
            text="edit",
            command=lambda: [
                self.page.refresh(),
                self.update(),
                self.root.pages["AddEditFood"].show(),
                self.root.pages["AddEditFood"].setItemToEdit(item),
            ],
        )

        editButton.pack(side=RIGHT)

        trashButton = ttk.Button(
            self,
            text="trash",
            command=lambda: [
                self.delete(),
                self.update(),
                self.page.refresh(),
            ],
        )
        trashButton.pack(side=RIGHT)

    def delete(self):

        confirmed = messagebox.askyesno(
            title="Are you sure?",
            message=f"Are you sure you want to delete {self.item['name']}?",
        )

        if confirmed:

            DietPlanner.removeItem(
                self.item["category_id"],
                self.item["subcategory_id"],
                self.item["name"],
            )


class FoodListPage(Page):
    foodData = None
    currentFrames = None
    canvas = None

    verticalScrollBar = None
    addFoodButton = None

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        self.foodData = DietPlanner.getShelve()

        self.addFoodButton = ttk.Button(
            self.frame,
            text="Add food",
            command=lambda: [self.update(), self.root.pages["AddEditFood"].show()],
        )

        self.addFoodButton.pack(side="top", fill="both", expand=True)

        self.allFoodList = ttk.Frame(self.frame, padding="5")
        self.allFoodList.pack(side="top", fill="both", expand=True)

        label = ttk.Label(self.allFoodList, text="All food items")
        label.pack(side="top")
        self.currentFrames = []
        for item in self.foodData["items"]:

            itemFrame = ItemFrame(self.allFoodList, item, self.root, self)
            itemFrame.pack(fill="x", expand=True)

            self.currentFrames.append(itemFrame)

    def refresh(self):
        self.foodData = DietPlanner.getShelve()

        for frame in self.currentFrames:
            frame.pack_forget()

        self.currentFrames = []
        for item in self.foodData["items"]:

            itemFrame = ItemFrame(self.allFoodList, item, self.root, self)
            itemFrame.pack(fill="x", expand=True)

            self.currentFrames.append(itemFrame)
