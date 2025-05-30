from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page
import DietPlanner


class DeleteItemPage(Page):
    item = None
    label = None
    actionButtons: list[Widget] = []

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        self.label = Label(self.frame, text="No item selected for deletion")
        self.label.pack(side="top", fill="both", expand=True)

        self.removeActionButtons()
        if self.item:
            self.generateActionButtons()

    def generateActionButtons(self):
        cancelButton = ttk.Button(
            self.frame,
            text="Cancel",
            command=lambda: [
                self.resetItem(),
                self.refresh(),
                self.update(),
                self.root.pages["FoodList"].show(),
            ],
        )

        cancelButton.pack(side=LEFT)

        self.actionButtons.append(cancelButton)

        deleteButton = ttk.Button(
            self.frame,
            text="Delete",
            command=lambda: [
                DietPlanner.removeItem(
                    self.item["category_id"],
                    self.item["subcategory_id"],
                    self.item["name"],
                ),
                self.resetItem(),
                self.refresh(),
                self.update(),
                self.root.pages["FoodList"].show(),
                self.root.pages["FoodList"].refresh(),
            ],
        )
        deleteButton.pack(side=RIGHT)

        self.actionButtons.append(deleteButton)

    def removeActionButtons(self):
        for button in self.actionButtons:
            button.pack_forget()
        self.actionButtons = []

    def refresh(self):
        self.foodData = DietPlanner.getShelve()
        self.label["text"] = "No item selected for deletion"
        self.removeActionButtons()

        if self.item:
            self.label["text"] = (
                f"Are you sure you want to delete { self.item['name'] } ?"
            )

            self.generateActionButtons()

        self.root.update()

    def setItemToDelete(self, item):
        self.item = item

    def resetItem(self):
        self.item = None
