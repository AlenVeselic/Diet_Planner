from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page
import dietPlanner


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
                self.root.dietPlannerListPage.show(),
                self.root.dietPlannerListPage.setItemToEdit(item),
            ],
        )

        editButton.pack(side=RIGHT)

        trashButton = ttk.Button(
            self,
            text="trash",
            command=lambda: [
                #                dietPlanner.modifyShelve(
                #                    "del", self.curMainCat.get(), self.curSubCat.get(), inputVar.get()
                #                ),
                self.page.refresh(),
                # self.getItems(),
                self.update(),
                self.root.deleteItemPage.show(),
                self.root.deleteItemPage.setItemToDelete(item),
            ],
        )
        trashButton.pack(side=RIGHT)


class FoodListPage(Page):
    foodData = None
    currentFrames = None

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        self.foodData = dietPlanner.getShelve()

        foodFrame = ttk.Frame(self, padding="5")
        foodFrame.pack(side="top", fill="both", expand=True)

        self.allFoodList = ttk.Frame(foodFrame, padding="5")
        self.allFoodList.pack(side="top", fill="both", expand=True)

        label = ttk.Label(self.allFoodList, text="All food items")
        label.pack(side="top")
        self.currentFrames = []
        for item in self.foodData["items"]:

            itemFrame = ItemFrame(self.allFoodList, item, self.root, self)
            itemFrame.pack(fill="x", expand=True)

            self.currentFrames.append(itemFrame)

    def refresh(self):
        self.foodData = dietPlanner.getShelve()

        for frame in self.currentFrames:
            frame.pack_forget()

        self.currentFrames = []
        for item in self.foodData["items"]:

            itemFrame = ItemFrame(self.allFoodList, item, self.root, self)
            itemFrame.pack(fill="x", expand=True)

            self.currentFrames.append(itemFrame)
