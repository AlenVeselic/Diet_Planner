#! python3

# dietPlannerInterface.py - simple tkinter interface made to put the functions in dietPlanner.py to use in a visual manner

# import all needed things: tkinter for gui generationm, dietPlanner for backend operations, logginf for debug
from tkinter import *
from tkinter import ttk

import dietPlanner, logging

# logging basic configuration initialization

logging.basicConfig(level= logging.DEBUG, format=(" %(levelname)s - %(asctime)s - %(message)s"))

# initial food retrieval

foodData = dietPlanner.getShelve()

# gui initialization

root = Tk()

# getSubcategories - refreshes data and retrieves subcategories for the currently selected category

def getSubcategories(*args):

    refreshData()

    if root.focus_get() == mainCategoryBox: # checks wether the correct listbox is in focus

        subcategoryVar.set("")
        curMainCat.set(mainCategoryBox.get(mainCategoryBox.curselection())) 
        subcategoryVar.set(list(foodData[curMainCat.get()].keys()))
        curSubCat.set("")
        itemVar.set("")
        
# refreshes the global food database  
def refreshData(*args):
    global foodData
    foodData = dietPlanner.getShelve()
    
# retrieves the items for the currently selected category and subcategory
def getItems(*args):

    if root.focus_get() == subcategoryBox:
        print(curMainCat.get())
        curSubCat.set(subcategoryBox.get(subcategoryBox.curselection()))

        logging.debug("\n" + str(curMainCat.get()) + "\n ")

        logging.debug("\n" + str(curSubCat.get()) + "\n")    

        itemVar.set(foodData[curMainCat.get()][curSubCat.get()])

# variables which will store the currently selected category and subcategory since listboxes do not save selected items when out of focus    
curMainCat = StringVar()
curSubCat = StringVar()

# frame that will hold then food input programs 
foodFrame = ttk.Frame(root, padding = "5" )
foodFrame.grid(column = 0, row = 0, sticky = (N, W, E, S))

# main category select section
ttk.Label(foodFrame,text = "Main categories").grid(column = 0, row = 0)

categories = list(foodData.keys())
categoryVar = StringVar(value = categories)
mainCategoryBox = Listbox(foodFrame, listvariable = categoryVar, height = 5)
mainCategoryBox.grid(column = 0, row = 1, rowspan = 2)

# subcategory selection section
ttk.Label(foodFrame, text = "Subcategories").grid(column = 1, row = 0)

subcategoryVar = StringVar()
subcategoryBox = Listbox(foodFrame, listvariable = subcategoryVar, height = 5)
subcategoryBox.grid(column = 1, row = 1, rowspan = 2)


# item display section
ttk.Label(foodFrame, text = "Items").grid(column = 2, row = 0)
    
itemVar = StringVar()
itemBox = Listbox(foodFrame, listvariable = itemVar, height = 5)
itemBox.grid(column = 2, row = 1, rowspan = 2)

# item entry section
ttk.Label(foodFrame, text = "Item name entry").grid(column = 3, row = 0)
inputVar = StringVar()
inputEntry = ttk.Entry(foodFrame, textvariable = inputVar)
inputEntry.grid(column = 3, row = 1)

# addition and removal button 
addButton = ttk.Button(foodFrame, text = "+", command = lambda: dietPlanner.modifyShelve("add", (curMainCat.get(), curSubCat.get()), inputVar.get()))
addButton.grid(column = 4, row = 1, sticky = S)

removeButton = ttk.Button(foodFrame, text = "-", command = lambda: dietPlanner.modifyShelve("del", (curMainCat.get(), curSubCat.get()), inputVar.get()))
removeButton.grid(column = 4, row = 2, sticky = N)

# listbox selection bindings
mainCategoryBox.bind('<<ListboxSelect>>', getSubcategories)

subcategoryBox.bind('<<ListboxSelect>>', getItems)

#  mainloop initiation
root.mainloop()
