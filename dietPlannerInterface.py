#! python3

# dietPlannerInterface.py - simple tkinter interface made to put the functions in dietPlanner.py to use in a visual manner

# import all needed things: tkinter for gui generation
from tkinter import *
from tkinter import ttk

import dietPlanner, logging

logging.basicConfig(level= logging.DEBUG, format=(" %(levelname)s - %(asctime)s - %(message)s"))

foodData = dietPlanner.getShelve()

root = Tk()

def getSubcategories(*args):

    ttk.Label(foodFrame, text = "Subcategories").grid(column = 1, row = 0)

    chosenCategory =  mainCategoryBox.get(mainCategoryBox.curselection())
    subcategories = list(foodData[chosenCategory].keys())
    subcategoryVar = StringVar(value = subcategories)
    subcategoryBox = Listbox(foodFrame, listvariable = subcategoryVar, height = 5)
    subcategoryBox.grid(column = 1, row = 1)
    subcategoryBox.bind('<<ListboxSelect>>', lambda chosenCategory: getItems(chosenCategory))

def getItems(currentCategory):
    ttk.Label(foodFrame, text = "Items").grid(column = 2, row = 0)
    
    information = subcategoryBox.curselection()

    logging.debug("\n" + str(list(selectedSubcategory)) + str(currentCategory) + str(currentSubcategory) + "\n")

    chosenSubcategory = foodData[currentCategory][selectedSubcategory]
    items = list(chosenSubcategory)
    itemVar = StringVar(value = items)
    itemBox = Listbox(foodFrame, listvariable = itemVar, height = 5)
    itemBox.grid(column = 2, row = 1)



foodFrame = ttk.Frame(root, padding = "5" )
foodFrame.grid(column = 0, row = 0, sticky = (N, W, E, S))


ttk.Label(foodFrame,text = "Main categories").grid(column = 0, row = 0)

categories = list(foodData.keys())
categoryVar = StringVar(value = categories)
mainCategoryBox = Listbox(foodFrame, listvariable = categoryVar, height = 5)
mainCategoryBox.grid(column = 0, row = 1)

mainCategoryBox.bind('<<ListboxSelect>>', getSubcategories)

root.mainloop()
