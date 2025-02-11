#! python3

# dietPlannerInterface.py - simple tkinter interface made to put the functions in dietPlanner.py to use in a visual manner

# import all needed things: tkinter for gui generationm, dietPlanner for backend operations, logginf for debug
from tkinter import *
from tkinter import ttk

import dietPlanner, logging

# getSubcategories - refreshes data and retrieves subcategories for the currently selected category

def getSubcategories(*args):

    refreshData() # refreshes the displayed dictionary

    if root.focus_get() == mainCategoryBox: # checks wether the correct listbox is in focus

        subcategoryVar.set("") # clears the displayed subcategory listbox
        curMainCat.set(mainCategoryBox.get(mainCategoryBox.curselection()))  # sets the new main chosen category
        subcategoryVar.set(list(foodData[curMainCat.get()].keys())) # freshly sets the subcategory display
        # clears the preceeding listboxes
        curSubCat.set("") 
        itemVar.set("")

        root.update()
        
# refreshes the global food database  
def refreshData(*args):
    global foodData
    foodData = dietPlanner.getShelve()
    
# retrieves the items for the currently selected category and subcategory
def getItems(*args):

    if root.focus_get() == subcategoryBox:
        # sets the newly choosen subcategory
        curSubCat.set(subcategoryBox.get(subcategoryBox.curselection()))

        logging.debug("\n" + str(curMainCat.get()) + "\n ")

        logging.debug("\n" + str(curSubCat.get()) + "\n")    
        # sets the items the item listbox needs to display
        itemVar.set(foodData[curMainCat.get()][curSubCat.get()])

if __name__ == "__main__":

    # logging basic configuration initialization

    logging.basicConfig(level= logging.DEBUG, format=(" %(levelname)s - %(asctime)s - %(message)s"))

    # initial food retrieval

    foodData = dietPlanner.getShelve()

    # gui initialization

    root = Tk()

    # variables which will store the currently selected category and subcategory since listboxes do not save selected items when out of focus    
    curMainCat = StringVar()
    curSubCat = StringVar()

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    test = ttk.Style()
    test.configure("TFrame", background = "orange")

    # frame that will hold then food input programs 
    foodFrame = ttk.Frame(root, padding = "5", style="TFrame")
    foodFrame.grid(column = 1, row = 1, sticky = (N, W, E, S))

    

    # main category select section
    ttk.Label(foodFrame,text = "Main categories").grid(column = 1, row = 1)

    categories = list(foodData.keys())
    categoryVar = StringVar(value = categories)
    mainCategoryBox = Listbox(foodFrame, listvariable = categoryVar)
    # mainCategoryBox.pack(fill=BOTH, expand = True)
    mainCategoryBox.grid(column = 1, row = 2, rowspan = 2, sticky=(N, W, E, S))
    
    mainCategoryBox["bg"] = "white"

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
    addButton = ttk.Button(foodFrame, text = "+", command = lambda: dietPlanner.modifyShelve("add", (curMainCat.get(), curSubCat.get()), inputVar.get()))
    addButton.grid(column = 5, row = 2, sticky = S)

    removeButton = ttk.Button(foodFrame, text = "-", command = lambda: dietPlanner.modifyShelve("del", (curMainCat.get(), curSubCat.get()), inputVar.get()))
    removeButton.grid(column = 5, row = 3, sticky = N)

    
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
