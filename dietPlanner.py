
import shelve, Path

def getShelve():

    Path("dietData").mkdir(parents = True, exist_ok = True)

    data = shelve.open("dietData\\dietPlannerData")

    return data


def modifyShelve(mode, categoryList, itemList):

    if mode == "add":

        if categoryList[0] == "takeOut":
            if categoryList[1] in  :
                if itemList in 
        elif categoryList[0] == "recipes":

        elif categoryList[0] == "readyMadeFood":

        elif categoryList[0] == "smallAddition":

        else:
            print("Not a category")


def createPlan():
    print()

modifyShelve("add", (), ())

