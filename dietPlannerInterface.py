#! python3

# dietPlannerInterface.py - simple tkinter interface made to put the functions in dietPlanner.py to use in a visual manner

# import all needed things: tkinter for gui generationm, dietPlanner for backend operations, logginf for debug
from tkinter import *
#from tkinter import ttk
import ttkbootstrap as ttk

import dietPlanner, logging

# getSubcategories - refreshes data and retrieves subcategories for the currently selected category

def getSubcategories(*args):

    logging.debug("\n Get subcategories \n ")
    refreshData() # refreshes the displayed dictionary

    #if root.focus_get() == mainCategoryBox: # checks wether the correct listbox is in focus

    #subcategoryVar.set("") # clears the displayed subcategory listbox
    currentlySelected = mainCategoryBox.curselection() # gets the currently selected category
    if currentlySelected:
        nextCategory = mainCategoryBox.get(mainCategoryBox.curselection()) # gets the newly selected category
        if nextCategory:
            curMainCat.set(nextCategory)  # sets the new main chosen category
            nextCategoryObject = dietPlanner.getCategoryFromName(foodData["categories"], nextCategory)
            # subcategoryVar.set(list(foodData[curMainCat.get()].keys())) # freshly sets the subcategory display
            subcategoryVar.set(list(getSubcategoriesFromCategories(foodData["categories"], nextCategoryObject))) # freshly sets the subcategory display
            # clears the preceeding listboxes
            curSubCat.set(0)
            #curSubCat.set("") 
            itemVar.set(0)

            root.update()
        
# refreshes the global food database  
def refreshData(*args):
    global foodData
    foodData = dietPlanner.getShelve()
    
# retrieves the items for the currently selected category and subcategory
def getItems(*args):

    logging.debug("\n Get items \n ")

    currentlySelected = subcategoryBox.curselection()
    if currentlySelected:
        nextSubCategory = subcategoryBox.get(subcategoryBox.curselection())
        if nextSubCategory:
            # sets the newly choosen subcategory
            if nextSubCategory:
                curSubCat.set(nextSubCategory)

                logging.debug("\n" + str(curMainCat.get()) + "\n ")

                logging.debug("\n" + str(curSubCat.get()) + "\n")    
                # sets the items the item listbox needs to display
                allItems = foodData['items']
                selectedSubCategory = dietPlanner.getCategoryFromName(foodData["categories"], curSubCat.get())
                filteredItems = (item for item in allItems if item["subcategory_id"] == selectedSubCategory["category_id"])
                filteredItemNames = [item["name"] for item in filteredItems]
                itemVar.set(filteredItemNames)

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

if __name__ == "__main__":

    # logging basic configuration initialization

    logging.basicConfig(level= logging.DEBUG, format=(" %(levelname)s - %(asctime)s - %(message)s"))

    # initial food retrieval

    foodData = dietPlanner.getShelve()

    # gui initialization

    root = ttk.Window( themename="journal")

    # variables which will store the currently selected category and subcategory since listboxes do not save selected items when out of focus    
    curMainCat = StringVar()
    curSubCat = StringVar()

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    test = ttk.Style()
    test.configure("TestFrame", background = "light-gray")

    # frame that will hold then food input programs 
    foodFrame = ttk.Frame(root, padding = "5")
    foodFrame.grid(column = 1, row = 1, sticky = (N, W, E, S))

    # main category select section
    ttk.Label(foodFrame,text = "Main categories").grid(column = 1, row = 1)

    categories = list(getMainCategoriesFromCategories(foodData["categories"]))
    categoryVar = StringVar(value = categories)
    mainCategoryBox = Listbox(foodFrame, listvariable = categoryVar)
    # mainCategoryBox.pack(fill=BOTH, expand = True)
    mainCategoryBox.grid(column = 1, row = 2, rowspan = 2, sticky=(N, W, E, S))
    
    #mainCategoryBox["bg"] = "white"

    foodFrame.grid_columnconfigure(1, weight=1)
    foodFrame.grid_rowconfigure(2, weight=1)

    foodFrame.grid_columnconfigure(2, weight=1)
    foodFrame.grid_columnconfigure(3, weight=1)

    # subcategory selection section
    ttk.Label(foodFrame, text = "Subcategories").grid(column = 2, row = 1)

    subcategoryVar = StringVar()
    subcategoryBox = Listbox(foodFrame, listvariable = subcategoryVar)
    subcategoryBox.grid(column = 2, row = 2, rowspan = 2, sticky=(N, W, E, S))


    # item display section
    ttk.Label(foodFrame, text = "Items").grid(column = 3, row = 1)
        
    itemVar = StringVar()
    itemBox = Listbox(foodFrame, listvariable = itemVar)
    itemBox.grid(column = 3, row = 2, rowspan = 2, sticky=(N, W, E, S))

    # item entry section
    ttk.Label(foodFrame, text = "Item name entry").grid(column = 4, row = 1)
    inputVar = StringVar()
    inputEntry = ttk.Entry(foodFrame, textvariable = inputVar)
    inputEntry.grid(column = 4, row = 2)

    # addition and removal button 
    addButton = ttk.Button(foodFrame, text = "+", command = lambda: [dietPlanner.modifyShelve("add", curMainCat.get(), curSubCat.get(), inputVar.get()), refreshData(), getItems(), root.update()])
    addButton.grid(column = 5, row = 2, sticky = S)

    removeButton = ttk.Button(foodFrame, text = "-", command = lambda: [dietPlanner.modifyShelve("del", curMainCat.get(), curSubCat.get(), inputVar.get()), refreshData(), getItems(), root.update()])
    removeButton.grid(column = 5, row = 3, sticky = N)

    allFoodList = ttk.Frame(foodFrame, padding = "5")
    allFoodList.grid(column = 1, row = 4, rowspan = 4, sticky = (N, W, E, S))

    
    ttk.Label(allFoodList, text = "All food items").pack()


    for item in foodData["items"]:
        ttk.Label(allFoodList, text = item["name"]).pack()


    
    foodFrame.grid_rowconfigure(0, weight=1)
    foodFrame.grid_columnconfigure(0, weight=1)
    foodFrame.grid_rowconfigure(4, weight=1)
    foodFrame.grid_columnconfigure(6, weight=1)

    root.grid_rowconfigure(1, weight=2)
    root.grid_columnconfigure(1, weight=1)

    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(2, weight=1)

    # listbox selection bindings
    mainCategoryBox.bind('<<ListboxSelect>>', getSubcategories)

    subcategoryBox.bind('<<ListboxSelect>>', getItems)

    #  mainloop initiation
    root.mainloop()
