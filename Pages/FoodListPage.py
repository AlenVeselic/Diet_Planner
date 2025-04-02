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
    canvas = None

    foodFrame = None
    verticalScrollBar = None
    addFoodButton = None

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        self.foodData = dietPlanner.getShelve()

        self.canvas = Canvas(self, borderwidth=0, background="white")

        self.foodFrame = ttk.Frame(self.canvas, padding="5")
        # self.foodFrame.pack(side="top", fill="both", expand=True)

        self.verticalScrollBar = Scrollbar(
            self, orient=VERTICAL, command=self.canvas.yview
        )

        self.canvas.configure(yscrollcommand=self.verticalScrollBar.set)

        self.verticalScrollBar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas.create_window(
            (4, 4), window=self.foodFrame, anchor=NW, tags="self.foodFrame"
        )

        self.foodFrame.bind("<Configure>", self.onFrameConfigure)

        self.addFoodButton = ttk.Button(
            self.foodFrame,
            text="Add food",
            command=lambda: [self.update(), self.root.dietPlannerListPage.show()],
        )

        self.addFoodButton.pack(side="top", fill="both", expand=True)

        self.allFoodList = ttk.Frame(self.foodFrame, padding="5")
        self.allFoodList.pack(side="top", fill="both", expand=True)

        label = ttk.Label(self.allFoodList, text="All food items")
        label.pack(side="top")
        self.currentFrames = []
        for item in self.foodData["items"]:

            itemFrame = ItemFrame(self.allFoodList, item, self.root, self)
            itemFrame.pack(fill="x", expand=True)

            self.currentFrames.append(itemFrame)

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

    def refresh(self):
        self.foodData = dietPlanner.getShelve()

        for frame in self.currentFrames:
            frame.pack_forget()

        self.currentFrames = []
        for item in self.foodData["items"]:

            itemFrame = ItemFrame(self.allFoodList, item, self.root, self)
            itemFrame.pack(fill="x", expand=True)

            self.currentFrames.append(itemFrame)
