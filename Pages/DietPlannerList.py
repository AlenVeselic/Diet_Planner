from tkinter import *
import ttkbootstrap as ttk
import logging

from Pages.Page_Class import Page
import dietPlanner


class DietPlannerList(Page):
    mainCategoryBox: Listbox = None
    subcategoryBox: Listbox = None
    curMainCat: StringVar = None
    categoryVar: StringVar = None
    subcategoryVar: StringVar = None
    curSubCat: StringVar = None
    itemVar: StringVar = None

    foodData = None

    def getSubcategories(self, *args, mainCategory=None):

        logging.debug("\n Get subcategories \n ")
        self.refresh()  # refreshes the displayed dictionary

        # if root.focus_get() == mainCategoryBox: # checks wether the correct listbox is in focus

        # subcategoryVar.set("") # clears the displayed subcategory listbox
        currentlySelected = (
            self.mainCategoryBox.selection_get()
        )  # gets the currently selected category
        if currentlySelected:
            nextCategory = self.mainCategoryBox.selection_get()
            # gets the newly selected category
            if nextCategory:
                if mainCategory:
                    nextCategory = mainCategory
                self.curMainCat.set(nextCategory)  # sets the new main chosen category
                nextCategoryObject = dietPlanner.getCategoryFromName(
                    self.foodData["categories"], nextCategory
                )
                # subcategoryVar.set(list(foodData[curMainCat.get()].keys())) # freshly sets the subcategory display
                self.subcategoryBox["values"] = list(
                    dietPlanner.getSubcategoriesFromCategories(
                        self.foodData["categories"], nextCategoryObject
                    )
                )  # freshly sets the subcategory display
                # clears the preceeding listboxes
                # self.curSubCat.set(0)
                # curSubCat.set("")
                # self.itemVar.set(0)

                self.root.update()

    # retrieves the items for the currently selected category and subcategory
    def getItems(self, *args):

        logging.debug("\n Get items \n ")

        currentlySelected = self.subcategoryBox.selection_get()
        if currentlySelected:
            nextSubCategory = self.subcategoryBox.selection_get()
            if nextSubCategory:
                # sets the newly choosen subcategory
                if nextSubCategory:
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

                        self.getSubcategories(self.categoryVar.get())
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
        foodFrame = ttk.Frame(self, padding="5")
        foodFrame.grid(column=1, row=1, sticky=(N, W, E, S))

        # main category select section
        ttk.Label(foodFrame, text="Main categories").grid(column=1, row=1)

        categories = list(
            dietPlanner.getMainCategoriesFromCategories(self.foodData["categories"])
        )
        self.categoryVar = StringVar()
        self.mainCategoryBox = ttk.Combobox(
            foodFrame, textvariable=self.categoryVar, values=categories
        )
        # mainCategoryBox.pack(fill=BOTH, expand = True)
        self.mainCategoryBox.grid(column=1, row=2, sticky=(N, W, E, S))

        # mainCategoryBox["bg"] = "white"

        foodFrame.grid_columnconfigure(1, weight=1)
        foodFrame.grid_rowconfigure(2, weight=0)

        foodFrame.grid_columnconfigure(2, weight=1)
        foodFrame.grid_columnconfigure(3, weight=1)

        # subcategory selection section
        ttk.Label(foodFrame, text="Subcategories").grid(column=2, row=1)

        subcategories = list(
            dietPlanner.getAllSubcategoriesFromCategories(self.foodData["categories"])
        )
        self.subcategoryVar = StringVar()
        self.subcategoryBox = ttk.Combobox(
            foodFrame, textvariable=self.subcategoryVar, values=subcategories
        )
        self.subcategoryBox.grid(column=2, row=2, sticky=(N, W, E, S))

        # item display section
        # ttk.Label(foodFrame, text="Items").grid(column=3, row=1)

        # self.itemVar = StringVar()
        # itemBox = Listbox(foodFrame, listvariable=self.itemVar)
        # itemBox.grid(column=3, row=2, rowspan=2, sticky=(N, W, E, S))

        # item entry section
        ttk.Label(foodFrame, text="Item name entry").grid(column=3, row=1)
        inputVar = StringVar()
        inputEntry = ttk.Entry(foodFrame, textvariable=inputVar)
        inputEntry.grid(column=3, row=2, sticky=(N, W, E, S))

        # addition and removal button
        addButton = ttk.Button(
            foodFrame,
            text="Add Item",
            command=lambda: [
                dietPlanner.modifyShelve(
                    "add", self.curMainCat.get(), self.curSubCat.get(), inputVar.get()
                ),
                self.refresh(),
                # self.getItems(),
                self.root.update(),
            ],
        )
        addButton.grid(column=3, row=4, sticky=E)

        removeButton = ttk.Button(
            foodFrame,
            text="Cancel",
            command=lambda: [
                #                dietPlanner.modifyShelve(
                #                    "del", self.curMainCat.get(), self.curSubCat.get(), inputVar.get()
                #                ),
                self.refresh(),
                # self.getItems(),
                self.update(),
                self.root.p3.show(),
            ],
        )
        removeButton.grid(column=1, row=4, sticky=W)

        # allFoodList = ttk.Frame(foodFrame, padding="5")
        # allFoodList.grid(column=1, row=4, rowspan=4, sticky=(N, W, E, S))

        # ttk.Label(allFoodList, text="All food items").pack()

        # for item in foodData["items"]:
        #     ttk.Label(allFoodList, text=item["name"]).pack()

        foodFrame.grid_rowconfigure(0, weight=1)
        foodFrame.grid_columnconfigure(0, weight=1)
        foodFrame.grid_rowconfigure(4, weight=1)
        foodFrame.grid_columnconfigure(6, weight=1)

        # listbox selection bindings

        self.mainCategoryBox.bind("<<ComboboxSelected>>", self.getSubcategories)

        self.subcategoryBox.bind("<<ComboboxSelected>>", self.getItems)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(1, weight=2)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def refresh(self):
        self.foodData = dietPlanner.getShelve()
        self.root.update()
