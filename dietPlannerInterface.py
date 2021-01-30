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

    if root.focus_get() == mainCategoryBox:

        subcategoryVar.set("")
        curMainCat.set(mainCategoryBox.get(mainCategoryBox.curselection())) 
        subcategoryVar.set(list(foodData[curMainCat.get()].keys()))
        curSubCat.set("")
        itemVar.set("")
            

    

def getItems(*args):

    if root.focus_get() == subcategoryBox:
        print(curMainCat.get())
        curSubCat.set(subcategoryBox.get(subcategoryBox.curselection()))

        logging.debug("\n" + str(curMainCat.get()) + "\n ")

        logging.debug("\n" + str(curSubCat.get()) + "\n")    

        itemVar.set(foodData[curMainCat.get()][curSubCat.get()])
    
curMainCat = StringVar()
curSubCat = StringVar()


foodFrame = ttk.Frame(root, padding = "5" )
foodFrame.grid(column = 0, row = 0, sticky = (N, W, E, S))


ttk.Label(foodFrame,text = "Main categories").grid(column = 0, row = 0)

categories = list(foodData.keys())
categoryVar = StringVar(value = categories)
mainCategoryBox = Listbox(foodFrame, listvariable = categoryVar, height = 5)
mainCategoryBox.grid(column = 0, row = 1)

ttk.Label(foodFrame, text = "Subcategories").grid(column = 1, row = 0)

subcategoryVar = StringVar()
subcategoryBox = Listbox(foodFrame, listvariable = subcategoryVar, height = 5)
subcategoryBox.grid(column = 1, row = 1)


ttk.Label(foodFrame, text = "Items").grid(column = 2, row = 0)
    
itemVar = StringVar()
itemBox = Listbox(foodFrame, listvariable = itemVar, height = 5)
itemBox.grid(column = 2, row = 1)

addButton = ttk.Button()

removeButton = ttk.Button()


mainCategoryBox.bind('<<ListboxSelect>>', getSubcategories)

subcategoryBox.bind('<<ListboxSelect>>', getItems)



root.mainloop()
