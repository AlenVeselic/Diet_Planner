#! python3

# Diet Planner - A program that generates a diet plan from all your favorite foods!


# Import all the necessities. Shelve for data storage, pprint for printing messier strings(dictionaries most of all),
#  random for choosing foods, logging for debugging
import shelve, pprint, random, logging
from pathlib import Path

logging.basicConfig(level = logging.DEBUG, format = ' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')

# getShelve - Create or open the local shelve holding all foods, categorized in subgroups and return it's contents
def getShelve():

    Path("dietData").mkdir(parents = True, exist_ok = True) # Create data directory if it don't exist, if it does, skip this line

    data = shelve.open("dietData\\dietPlannerData") # Open/Create shelve files

    # try allocating all foods into variable, if that doesn't exist, initialize a fresh shelve with all basic categories and save it into the variable
    try:
        dataVar = data["foods"]
    except KeyError:
        data["foods"] = initShelve()
        dataVar = data["foods"]
    data.close()    # close the shelve file, we got from it what we needed

                
    return dataVar  # return the data gotten from the shelve

# initShelve - Initializes a fresh food data shelve file, with all the needed categories and their respective subcategories

def initShelve():

    emptyDict = {} # reserves the dictionary we are about to fill out

    # the maincategories gives you an example of the categories used in this script:
    #   "takeOut": would hold each restaurant you have ordered from and each item you liked from said restaurant
    #   "recipes": would hold recipes that you can prepare, each recipe its attributes,
    #           these being: "preparationType", "ingredients", "instructions" and "timeToPrepare". 
    #           These are subject to change since I haven't gotten any testing done on this yet.
    #           The point of this is to give you all the information you need in order to prepare said recipe.
    #   "readyMade": would hold prepared, usually frozen, instant, or just readily eatable refrigeratable items that can be bought in stores
    #   "sAddition": are minor additions to a meal, this one is very experimental and subject to change.

    mainCategories = {"takeOut":["McDonalds", "Mango", "Astoria", "Takos"],
                      "recipes":["simple Roast", "Pork, Tallegio and Broccoli Lasagne",
                                 "Pork Sarnie", "Hot and Sour Chicken Broth"],
                      "readyMade":["Lidl", "Hofer", "Spar", "Tus"],
                      "sAddition":["Fruit", "Veggies", "Sauces", "Dairy"]
                    }
                
    recipeItemCats = ["preparationType", "ingredients", "instructions", "timeToPrepare"] # a list of attributes for the recipe item dictionaries
                                                                                         # TODO: have all items have at least some attributes (prices, timeworth, foodType)?


    # Generates the structure of the main dictionary, with the recipe category as an exception, because it's not a list
    for cat in mainCategories.keys():
        emptyDict[cat] = {}
        for subCat in mainCategories[cat]:
            if cat == "recipes":
                emptyDict[cat][subCat] = {}
                
                for itemCat in recipeItemCats:
                    emptyDict[cat][subCat][itemCat] = ""
            else:
               emptyDict[cat][subCat] = [] 


    return emptyDict

# modifyShelve - modifies the data in the shelve file, only removal and addition of items is available at this point
                 # TODO: main category addition and removal, with input validation and security
                 # TODO: Add item attribute modification
    # Call example modifyShelve(
    #                           mode - action(add or del)
    #                           categoryList - list of categories in which to append or remove the given item
    #                           itemList - the first value is the items name while the remaining values are the item's attribute values
    #                           )

def modifyShelve(mode, categoryList, itemList):

    # gets all of the currently stored food data

    foods = getShelve() 

    # Conditional statement which checks wether the shelve contains the structure, if it does not something has gone terribly wrong

    if foods == {}:
        print("no foods in database")
    else:
        logging.debug(pprint.pformat(dict(foods)))

    # This part takes every category that has list type items and saves their lowered key values for easier comparation purposes

    listCats = {}
    
    for category in foods.keys():

        subcategories = list(foods[category].keys())
        if type(foods[category][subcategories[0]]) is list:
            listCats[category.lower()] = category
    

    if mode == "add":

        # This mode goes category by category and if they all align and the item doesn't exist yet, a new item is created
        # The comparation is all done with lowered values while the value later saved is in normal caps,
        # this nullifies people mistyping capital letters and duplicating values by accident

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
            else:
                foods[listCats[categoryList[0].lower()]][categoryList[1]] = []
                foods[listCats[categoryList[0].lower()]][categoryList[1]].append(itemList)

        # "recipes" has a different approach since it's only one category and going by indexes would only return a letter from the word,
        #  eventually causing bugs if a letter type workaround was made with the advent of other main categories starting with the letter r. 
        #  Its itemList variable holds more than one value, having its name in the first spot and sharing the rest of the space with attribute values
        elif categoryList == "recipes":

            # same as list categories we lower recipe names in order to avoid duplicates
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
            # in case someone puts in an invalid main category, they are greeted with this message
            print("Not a category")

    elif mode == "del":
        # deletion goes through the same motions as addition only that instead of adding it deletes the given item
        # for deletion we only take the item's name

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

    # in the end whatever changes have been made are saved to the shelve
    # TODO: check whether any values have actually changed to decide if it's even worth saving 

    data = shelve.open("dietData\\dietPlannerData")
    data["foods"] = foods
    data.close()

# createPlan(length, recipeNum, takeOutNum) - this is the meal plan generation script,
#  it takes all the foods from the database and assembles them into meal plan 
# so that you have to be indecisive with your eating habits NO MORE
#   Variables:
#       length - the number of days to plan out
#       recipeNum - how many of these days can contain recipes
#       takeOutNum - how many of these days can contain take out
#   #TODO: Make recipe generation more refined and flexible.
def createPlan(length, recipeNum, takeOutNum):
    # empty plan creation, food database procurement, recipe and take out counter initialization
    plan = {}
    food = getShelve()
    recipeCount = 0
    takeOutCount = 0

    # The generational process goes through each day's every meal and
    #  for that meal decides a random category, of that a random subcategory and
    #  of that a random item to eat.
    #  TODO: give each item subjective "nutritional" that determines the fullness of a meal
    #  After looping through all the days it returns a dictionary representing a meal plan.

    for day in range(length): # Day loop, generates a dictionary with the current day's value as its key
        plan["Day " + str(day)] = {}
        for meal in range(3): # Meal loop, generates a dictionary with the current meal's value, also chooses the meal's food

            while True: # this loop chooses current meal's food category,
                        # if it chooses one of the categories that have expended their appearance numbers it loops again until it chooses an available category
                category = random.choice(list(food.keys()))
                if category.lower() == 'takeout' and takeOutCount > takeOutNum or category.lower() == 'recipes' and recipeCount > recipeNum:
                    continue
                else:
                    break
            if category == "recipes":   # this conditional statement chooses the meal's food item, recipes have a different approach to them adding their attributes to the end
                plan["Day " + str(day)]["Meal " + str(meal)] = {}
                foodChoice = random.choice(list(food[category].keys()))
                plan["Day " + str(day)]["Meal " + str(meal)][foodChoice] = food[category][foodChoice]
                recipeCount += 1 # with the addition of a recipe we add a notch to the recipe count
            else:
                subcategory = random.choice(list(food[category].keys()))
                foodChoice = random.choice(list(food[category][subcategory]))
                if category.lower() == 'saddition':
                    plan["Day " + str(day)]["Meal " + str(meal)] = category + "\\" + foodChoice
                else:
                    plan["Day " + str(day)]["Meal " + str(meal)] = subcategory + "\\" + foodChoice
                    if category.lower() == 'takeout':
                        takeOutCount += 1 # with the addition of a takeout variant we add a notch to the takeout count

    return plan


