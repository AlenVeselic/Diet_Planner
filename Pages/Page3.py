from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page
import dietPlanner


class Page3(Page):
    foodData = None
    currentFrames = None

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
        self.currentFrames = []
        for item in self.foodData["items"]:

            itemFrame = ttk.Frame(self.allFoodList)
            itemFrame.pack()

            label = ttk.Label(itemFrame, text=item["name"])
            label.pack()

            trashButton = ttk.Button(
                itemFrame,
                text="trash",
                command=lambda: [
                    #                dietPlanner.modifyShelve(
                    #                    "del", self.curMainCat.get(), self.curSubCat.get(), inputVar.get()
                    #                ),
                    self.refresh(),
                    # self.getItems(),
                    self.update(),
                    self.root.p1.show(),
                    self.root.p1.setItemToDelete(item),
                ],
            )
            trashButton.pack()

            self.currentFrames.append(itemFrame)

        foodFrame.grid_rowconfigure(0, weight=1)
        foodFrame.grid_columnconfigure(0, weight=1)
        foodFrame.grid_rowconfigure(4, weight=1)
        foodFrame.grid_columnconfigure(6, weight=1)

    def refresh(self):
        self.foodData = dietPlanner.getShelve()

        for frame in self.currentFrames:
            frame.pack_forget()

        self.currentFrames = []
        for item in self.foodData["items"]:

            itemFrame = ttk.Frame(self.allFoodList)
            itemFrame.pack()

            label = ttk.Label(itemFrame, text=item["name"])
            label.pack()

            trashButton = ttk.Button(
                itemFrame,
                text="trash",
                command=lambda: [
                    #                dietPlanner.modifyShelve(
                    #                    "del", self.curMainCat.get(), self.curSubCat.get(), inputVar.get()
                    #                ),
                    self.refresh(),
                    # self.getItems(),
                    self.update(),
                    self.root.p1.show(),
                    self.root.p1.setItemToDelete(item),
                ],
            )
            trashButton.pack()

            self.currentFrames.append(itemFrame)
