#! python3

# dietPlannerInterface.py - simple tkinter interface made to put the functions in dietPlanner.py to use in a visual manner

# import all needed things: tkinter for gui generationm, dietPlanner for backend operations, logginf for debug
from tkinter import *

# from tkinter import ttk
import ttkbootstrap as ttk

import dietPlanner, logging

# getSubcategories - refreshes data and retrieves subcategories for the currently selected category


def getMainCategoriesFromCategories(allCategories):
    mainCategories = []
    for category in allCategories:
        if category["parent_id"] == None:
            mainCategories.append(category["name"])
    return mainCategories


def getSubcategoriesFromCategories(allCategories, mainCategory):
    subCategories = []
    for category in allCategories:
        if category["parent_id"] == mainCategory["category_id"]:
            subCategories.append(category["name"])
    return subCategories


class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = Label(self, text="This is page 1")
        label.pack(side="top", fill="both", expand=True)


class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = Label(self, text="This is page 2")
        label.pack(side="top", fill="both", expand=True)


class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = Label(self, text="This is page 3")
        label.pack(side="top", fill="both", expand=True)


class DietPlannerList(Page):
    mainCategoryBox = None
    subcategoryBox = None
    curMainCat = None
    subcategoryVar = None
    curSubCat = None
    itemVar = None

    def getSubcategories(self, *args):

        logging.debug("\n Get subcategories \n ")
        self.refreshData()  # refreshes the displayed dictionary

        # if root.focus_get() == mainCategoryBox: # checks wether the correct listbox is in focus

        # subcategoryVar.set("") # clears the displayed subcategory listbox
        currentlySelected = (
            self.mainCategoryBox.curselection()
        )  # gets the currently selected category
        if currentlySelected:
            nextCategory = self.mainCategoryBox.get(
                self.mainCategoryBox.curselection()
            )  # gets the newly selected category
            if nextCategory:
                self.curMainCat.set(nextCategory)  # sets the new main chosen category
                nextCategoryObject = dietPlanner.getCategoryFromName(
                    foodData["categories"], nextCategory
                )
                # subcategoryVar.set(list(foodData[curMainCat.get()].keys())) # freshly sets the subcategory display
                self.subcategoryVar.set(
                    list(
                        getSubcategoriesFromCategories(
                            foodData["categories"], nextCategoryObject
                        )
                    )
                )  # freshly sets the subcategory display
                # clears the preceeding listboxes
                self.curSubCat.set(0)
                # curSubCat.set("")
                self.itemVar.set(0)

                root.update()

    # refreshes the global food database
    def refreshData(self, *args):
        global foodData
        foodData = dietPlanner.getShelve()

    # retrieves the items for the currently selected category and subcategory
    def getItems(self, *args):

        logging.debug("\n Get items \n ")

        currentlySelected = self.subcategoryBox.curselection()
        if currentlySelected:
            nextSubCategory = self.subcategoryBox.get(
                self.subcategoryBox.curselection()
            )
            if nextSubCategory:
                # sets the newly choosen subcategory
                if nextSubCategory:
                    self.curSubCat.set(nextSubCategory)

                    logging.debug("\n" + str(self.curMainCat.get()) + "\n ")

                    logging.debug("\n" + str(self.curSubCat.get()) + "\n")
                    # sets the items the item listbox needs to display
                    allItems = foodData["items"]
                    selectedSubCategory = dietPlanner.getCategoryFromName(
                        foodData["categories"], self.curSubCat.get()
                    )
                    filteredItems = (
                        item
                        for item in allItems
                        if item["subcategory_id"] == selectedSubCategory["category_id"]
                    )
                    filteredItemNames = [item["name"] for item in filteredItems]
                    self.itemVar.set(filteredItemNames)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # variables which will store the currently selected category and subcategory since listboxes do not save selected items when out of focus
        curMainCat = StringVar()
        curSubCat = StringVar()

        test = ttk.Style()
        test.configure("TestFrame", background="light-gray")

        # frame that will hold then food input programs
        foodFrame = ttk.Frame(self, padding="5")
        foodFrame.grid(column=1, row=1, sticky=(N, W, E, S))

        # main category select section
        ttk.Label(foodFrame, text="Main categories").grid(column=1, row=1)

        categories = list(getMainCategoriesFromCategories(foodData["categories"]))
        categoryVar = StringVar(value=categories)
        self.mainCategoryBox = Listbox(foodFrame, listvariable=categoryVar)
        # mainCategoryBox.pack(fill=BOTH, expand = True)
        self.mainCategoryBox.grid(column=1, row=2, rowspan=2, sticky=(N, W, E, S))

        # mainCategoryBox["bg"] = "white"

        foodFrame.grid_columnconfigure(1, weight=1)
        foodFrame.grid_rowconfigure(2, weight=1)

        foodFrame.grid_columnconfigure(2, weight=1)
        foodFrame.grid_columnconfigure(3, weight=1)

        # subcategory selection section
        ttk.Label(foodFrame, text="Subcategories").grid(column=2, row=1)

        subcategoryVar = StringVar()
        self.subcategoryBox = Listbox(foodFrame, listvariable=subcategoryVar)
        self.subcategoryBox.grid(column=2, row=2, rowspan=2, sticky=(N, W, E, S))

        # item display section
        ttk.Label(foodFrame, text="Items").grid(column=3, row=1)

        itemVar = StringVar()
        itemBox = Listbox(foodFrame, listvariable=itemVar)
        itemBox.grid(column=3, row=2, rowspan=2, sticky=(N, W, E, S))

        # item entry section
        ttk.Label(foodFrame, text="Item name entry").grid(column=4, row=1)
        inputVar = StringVar()
        inputEntry = ttk.Entry(foodFrame, textvariable=inputVar)
        inputEntry.grid(column=4, row=2)

        # addition and removal button
        addButton = ttk.Button(
            foodFrame,
            text="+",
            command=lambda: [
                dietPlanner.modifyShelve(
                    "add", curMainCat.get(), curSubCat.get(), inputVar.get()
                ),
                self.refreshData(),
                self.getItems(),
                root.update(),
            ],
        )
        addButton.grid(column=5, row=2, sticky=S)

        removeButton = ttk.Button(
            foodFrame,
            text="-",
            command=lambda: [
                dietPlanner.modifyShelve(
                    "del", curMainCat.get(), curSubCat.get(), inputVar.get()
                ),
                self.refreshData(),
                self.getItems(),
                self.update(),
            ],
        )
        removeButton.grid(column=5, row=3, sticky=N)

        allFoodList = ttk.Frame(foodFrame, padding="5")
        allFoodList.grid(column=1, row=4, rowspan=4, sticky=(N, W, E, S))

        ttk.Label(allFoodList, text="All food items").pack()

        for item in foodData["items"]:
            ttk.Label(allFoodList, text=item["name"]).pack()

        foodFrame.grid_rowconfigure(0, weight=1)
        foodFrame.grid_columnconfigure(0, weight=1)
        foodFrame.grid_rowconfigure(4, weight=1)
        foodFrame.grid_columnconfigure(6, weight=1)

        # listbox selection bindings

        self.mainCategoryBox.bind("<<ListboxSelect>>", self.getSubcategories)

        self.subcategoryBox.bind("<<ListboxSelect>>", self.getItems)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(1, weight=2)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)


class MainView(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        dietPlannerListPage = DietPlannerList(self)

        buttonframe = Frame(self)
        container = Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        dietPlannerListPage.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = Button(buttonframe, text="Page 1", command=p1.show)
        b2 = Button(buttonframe, text="Page 2", command=p2.show)
        b3 = Button(buttonframe, text="Page 3", command=p3.show)
        b4 = Button(buttonframe, text="Diet test", command=dietPlannerListPage.show)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(
            side="left",
        )

        p1.show()


# if __name__ == "__main__":

#     # gui initialization


#     #  mainloop initiation
#     root.mainloop()

if __name__ == "__main__":
    # logging basic configuration initialization

    logging.basicConfig(
        level=logging.DEBUG, format=(" %(levelname)s - %(asctime)s - %(message)s")
    )

    root = ttk.Window(themename="journal")

    # initial food retrieval

    foodData = dietPlanner.getShelve()

    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)

    # root.wm_geometry("400x400")
    root.mainloop()
