
import shelve, pprint
from pathlib import Path

def getShelve():

    Path("dietData").mkdir(parents = True, exist_ok = True)

    data = shelve.open("dietData\\dietPlannerData")
    try:
        dataVar = data["foods"]
    except KeyError:
        data["foods"] = initShelve()
        dataVar = data["foods"]

    data.close()


    return dataVar

def initShelve():
    emptyDict = {}

    mainCategories = {"takeOut":["McDonalds", "Mango", "Astoria", "Takos"],
                      "recipes":["simple Roast", "Pork, Tallegio and Broccoli Lasagne",
                                 "Pork Sarnie", "Hot and Sour Chicken Broth"],
                      "readyMade":["Lidl", "Hofer", "Spar", "Tus"],
                      "sAddition":["Fruit", "Veggies", "Sauces", "Dairy"]
                    }
    recipeItemCats = ["preparationType", "ingredients", "instructions", "timeToPrepare"]

    for cat in mainCategories.keys():
        emptyDict[cat] = {}
        for subCat in mainCategories[cat]:
            if cat == "recipes":
                emptyDict[cat][subCat] = {}
                
                for itemCat in recipeItemCats:
                    emptyDict[cat][subCat][itemCat] = ""
            else:
               emptyDict[cat][subCat] = [] 

            
    emptyDict['readyMade']['Hofer'].append("Pizza(Salami)")


    return emptyDict

def modifyShelve(mode, categoryList, itemList):

    foods = getShelve()
    if foods == {}:
        print("no foods in database")
    else:
        pprint.pprint(dict(foods))

    listCats = {}
    
    for category in foods.keys():

        subcategories = list(foods[category].keys())
        if type(foods[category][subcategories[0]]) is list:
            listCats[category.lower()] = category
    
    

    if mode == "add":

        if categoryList[0].lower() in listCats.keys():

            loweredSubcats = {}
            for item in foods[listCats[categoryList[0].lower()]].keys():
                loweredSubcats[item.lower()] = item

            if categoryList[1].lower() in loweredSubcats:
                subCategory = loweredSubcats[categoryList[1].lower()]
                if itemList in foods[listCats[categoryList[0].lower()]][subCategory]:
                    print('item already exists')
                else:
                    foods[listCats[categoryList[0].lower()]][subCategory].append(itemList)


        elif categoryList == "recipes":

            loweredRecipes = []
            for item in foods[categoryList].keys():
                loweredRecipes.append(item.lower())

            if itemList[0].lower() in loweredRecipes:
                print("Recipe already exists")
            else:
                foods[categoryList][itemList[0]] = {
                    "preparationType": itemList[1],
                    "ingredients": itemList[2],
                    "instructions": itemList[3],
                    "timeToPrepare": itemList[4]
                }

        else:
            print("Not a category")

    elif mode == "del":
        if categoryList[0].lower() in listCats:

            loweredSubcats = []
            for item in foods[categoryList[0]].keys():
                loweredSubcats.append(item.lower())

            if categoryList[1].lower() in loweredSubcats:
                if itemList in foods[categoryList[0]][categoryList[1]]:
                    foods[categoryList[0]][categoryList[1]].remove(itemList)
                    print("Item removed.")
                else:
                    print("item doesn't exist")
                    

        elif categoryList == "recipes":
            loweredRecipes = []
            for item in foods[categoryList].keys():
                loweredRecipes.append(item.lower())

            if itemList.lower() in loweredRecipes:
                foods[categoryList].pop(itemList)
                print("Recipe removed.")
            else:
                print("Recipe doesn't exist")

    data = shelve.open("dietData\\dietPlannerData")
    data["foods"] = foods
    data.close()

                


def createPlan():
    print()


modifyShelve("add", ("takeout", "mango"), ('Meat platter'))

data = shelve.open("dietData\\dietPlannerData")

print()

pprint.pprint(data['foods'])

