from tkinter import *
import ttkbootstrap as ttk
import logging

from Pages.Page_Class import Page
import dietPlanner


class AddEditFoodItem(Page):
    mainCategoryBox: Listbox = None
    subcategoryBox: Listbox = None
    curMainCat: StringVar = None
    categoryVar: StringVar = None
    subcategoryVar: StringVar = None
    curSubCat: StringVar = None
    itemVar: StringVar = None
    inputVar: StringVar = None

    foodData = None

    item = None

    actionButton = None
    foodFrame = None

    def setItemToEdit(self, item):

        self.item = item

        subCategory = dietPlanner.getCategoryFromId(
            self.foodData["categories"], item["subcategory_id"]
        )

        self.curSubCat.set(subCategory["name"])
        self.subcategoryVar.set(subCategory["name"])

        self.getItems(subCategory=subCategory["name"])

        self.inputVar.set(item["name"])

        self.refresh()

    def reset(self):
        self.item = None

        self.curMainCat.set("")
        self.categoryVar.set("")
        self.curSubCat.set("")
        self.subcategoryVar.set("")
        self.inputVar.set("")

    def getSubcategories(self, *args, mainCategory=None):

        logging.debug("\n Get subcategories \n ")
        self.refresh()  # refreshes the displayed dictionary

        if not mainCategory:
            currentlySelected = (
                self.mainCategoryBox.selection_get()
            )  # gets the currently selected category
        else:
            currentlySelected = mainCategory
        if currentlySelected:
            nextCategory = currentlySelected
            # gets the newly selected category
            if nextCategory:
                if mainCategory:
                    nextCategory = mainCategory
                self.curMainCat.set(nextCategory)  # sets the new main chosen category
                nextCategoryObject = dietPlanner.getCategoryFromName(
                    self.foodData["categories"], nextCategory
                )
                self.subcategoryBox["values"] = list(
                    dietPlanner.getSubcategoriesFromCategories(
                        self.foodData["categories"], nextCategoryObject
                    )
                )  # freshly sets the subcategory display

                self.root.update()

    # retrieves the items for the currently selected category and subcategory
    def getItems(self, *args, subCategory=None):

        logging.debug("\n Get items \n ")

        if not subCategory:
            currentlySelected = self.subcategoryBox.selection_get()
        else:
            currentlySelected = subCategory
        if currentlySelected:
            nextSubCategory = currentlySelected
            if nextSubCategory:
                # sets the newly choosen subcategory
                if subCategory:
                    nextSubCategory = subCategory
                self.curSubCat.set(nextSubCategory)

                logging.debug("\n" + str(self.curMainCat.get()) + "\n ")

                logging.debug("\n" + str(self.curSubCat.get()) + "\n")
                # sets the items the item listbox needs to display
                allItems = self.foodData["items"]
                selectedSubCategory = dietPlanner.getCategoryFromName(
                    self.foodData["categories"], self.curSubCat.get()
                )
                filteredItems = (
                    item
                    for item in allItems
                    if item["subcategory_id"] == selectedSubCategory["category_id"]
                )
                filteredItemNames = [item["name"] for item in filteredItems]
                # self.itemVar.set(filteredItemNames)

                if not self.curMainCat.get():
                    mainCategoryOfSubcategory = dietPlanner.getCategoryFromId(
                        self.foodData["categories"],
                        selectedSubCategory["parent_id"],
                    )

                    self.curMainCat.set(mainCategoryOfSubcategory["name"])
                    self.categoryVar.set(self.curMainCat.get())

                    self.getSubcategories(mainCategory=self.categoryVar.get())
                    # self.subcategoryBox.select_set(self.curMainCat.get())

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        self.foodData = dietPlanner.getShelve()

        # variables which will store the currently selected category and subcategory since listboxes do not save selected items when out of focus
        self.curMainCat = StringVar()
        self.curSubCat = StringVar()

        test = ttk.Style()
        test.configure("TestFrame", background="light-gray")

        # frame that will hold then food input programs
        self.foodFrame = ttk.Frame(self, padding="5")
        self.foodFrame.grid(column=1, row=1, sticky=(N, W, E, S))

        # main category select section
        ttk.Label(self.foodFrame, text="Main category: ").grid(column=1, row=2)

        categories = list(
            dietPlanner.getMainCategoriesFromCategories(self.foodData["categories"])
        )
        self.categoryVar = StringVar()
        self.mainCategoryBox = ttk.Combobox(
            self.foodFrame, textvariable=self.categoryVar, values=categories
        )
        # mainCategoryBox.pack(fill=BOTH, expand = True)
        self.mainCategoryBox.grid(column=2, row=2, sticky=(N, W, E, S))

        # mainCategoryBox["bg"] = "white"

        self.foodFrame.grid_columnconfigure(1, weight=1)
        self.foodFrame.grid_rowconfigure(2, weight=0)

        self.foodFrame.grid_columnconfigure(2, weight=1)
        self.foodFrame.grid_columnconfigure(3, weight=1)

        # subcategory selection section
        ttk.Label(self.foodFrame, text="Subcategory: ").grid(column=1, row=3)

        subcategories = list(
            dietPlanner.getAllSubcategoriesFromCategories(self.foodData["categories"])
        )
        self.subcategoryVar = StringVar()
        self.subcategoryBox = ttk.Combobox(
            self.foodFrame, textvariable=self.subcategoryVar, values=subcategories
        )
        self.subcategoryBox.grid(column=2, row=3, sticky=(N, W, E, S))

        # item display section
        # ttk.Label(foodFrame, text="Items").grid(column=3, row=1)

        # self.itemVar = StringVar()
        # itemBox = Listbox(foodFrame, listvariable=self.itemVar)
        # itemBox.grid(column=3, row=2, rowspan=2, sticky=(N, W, E, S))

        # item entry section
        ttk.Label(self.foodFrame, text="Item Name: ").grid(column=1, row=1)
        self.inputVar = StringVar()
        inputEntry = ttk.Entry(self.foodFrame, textvariable=self.inputVar)
        inputEntry.grid(column=2, row=1, sticky=(N, W, E, S))

        if not self.item:
            # addition button
            self.actionButton = ttk.Button(
                self.foodFrame,
                text="Add Item",
                command=lambda: [
                    dietPlanner.addFoodItem(
                        self.curMainCat.get(),
                        self.curSubCat.get(),
                        self.inputVar.get(),
                    ),
                    self.reset(),
                    self.refresh(),
                    self.root.foodList.refresh(),
                    self.root.foodList.show(),
                    self.root.update(),
                ],
            )
            self.actionButton.grid(column=3, row=4, sticky=E)
        else:
            # edit button
            self.actionButton = ttk.Button(
                self.foodFrame,
                text="Edit Item",
                command=lambda: [
                    dietPlanner.editItem(
                        self.curMainCat.get(),
                        self.curSubCat.get(),
                        self.inputVar.get(),
                        itemId=self.item["item_id"],
                    ),
                    self.reset(),
                    self.refresh(),
                    self.root.foodList.refresh(),
                    self.root.foodList.show(),
                    self.root.update(),
                ],
            )
            self.actionButton.grid(column=3, row=4, sticky=E)

        cancelButton = ttk.Button(
            self.foodFrame,
            text="Cancel",
            command=lambda: [
                self.reset(),
                self.root.foodList.refresh(),
                self.root.foodList.show(),
                self.update(),
            ],
        )
        cancelButton.grid(column=1, row=4, sticky=W)

        self.foodFrame.grid_rowconfigure(0, weight=1)
        self.foodFrame.grid_columnconfigure(0, weight=1)
        self.foodFrame.grid_rowconfigure(4, weight=1)
        self.foodFrame.grid_columnconfigure(6, weight=1)

        # combobox selection bindings

        self.mainCategoryBox.bind("<<ComboboxSelected>>", self.getSubcategories)

        self.subcategoryBox.bind("<<ComboboxSelected>>", self.getItems)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(1, weight=2)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def refresh(self):

        self.actionButton.grid_forget()

        if not self.item:
            # addition button
            self.actionButton = ttk.Button(
                self.foodFrame,
                text="Add Item",
                command=lambda: [
                    dietPlanner.addFoodItem(
                        self.curMainCat.get(),
                        self.curSubCat.get(),
                        self.inputVar.get(),
                    ),
                    self.reset(),
                    self.refresh(),
                    self.root.foodList.refresh(),
                    self.root.foodList.show(),
                    self.root.update(),
                ],
            )
            self.actionButton.grid(column=3, row=4, sticky=E)
        else:
            # edit button
            self.actionButton = ttk.Button(
                self.foodFrame,
                text="Edit Item",
                command=lambda: [
                    dietPlanner.editItem(
                        self.curMainCat.get(),
                        self.curSubCat.get(),
                        self.inputVar.get(),
                        itemId=self.item["item_id"],
                    ),
                    self.reset(),
                    self.refresh(),
                    self.root.foodList.refresh(),
                    self.root.foodList.show(),
                    self.root.update(),
                ],
            )
            self.actionButton.grid(column=3, row=4, sticky=E)

        self.foodData = dietPlanner.getShelve()
        self.root.update()
        # self.reset()
