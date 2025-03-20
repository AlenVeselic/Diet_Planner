from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page
import dietPlanner


class DeleteItemPage(Page):
    item = None
    label = None

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        self.label = Label(self, text="No item selected for deletion?")
        self.label.pack(side="top", fill="both", expand=True)

        cancelButton = ttk.Button(
            self,
            text="Cancel",
            command=lambda: [
                #                dietPlanner.modifyShelve(
                #                    "del", self.curMainCat.get(), self.curSubCat.get(), inputVar.get()
                #                ),
                self.refresh(),
                # self.getItems(),
                self.update(),
                self.root.foodList.show(),
            ],
        )

        cancelButton.pack()

        deleteButton = ttk.Button(
            self,
            text="Delete",
            command=lambda: [
                dietPlanner.modifyShelve(
                    "del",
                    self.item["category_id"],
                    self.item["subcategory_id"],
                    self.item["name"],
                ),
                self.refresh(),
                # self.getItems(),
                self.update(),
                self.root.foodList.show(),
                self.root.foodList.refresh(),
            ],
        )
        deleteButton.pack()

    def refresh(self):
        self.foodData = dietPlanner.getShelve()
        self.root.update()

    def setItemToDelete(self, item):
        self.item = item

        self.label["text"] = f"Are you sure you want to delete { self.item['name'] } ?"
