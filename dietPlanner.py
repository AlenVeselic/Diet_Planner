#! python3

# Diet Planner - A program that generates a diet plan from all your favorite foods!

# TODO:Review the following comments

# The Main Categories give you an example of the categories used in this script:
#   "takeOut": Subcategories - restaurants, FoodItems - favorite items to order,
#   "recipes": would hold a person's favorite recipes. For each recipe the following attributes would have to be filled in:
#           "preparationType", "ingredients", "instructions" and "timeToPrepare".
#   This is so that the user can be ensured that they will be able to prepare the recipe using only the app.
#       # TODO: A recipe ingredient can be an item from any other main category, even takeout. This relationship is optional. It can also just be a string.
#
#   "readyMade": would hold prepared, usually frozen, instant, or just ready for consumption refrigeratable items that can be bought in stores and prepared in a short amount of time.
#   Subcategories - Grocery store, Items -
#               # TODO: Evaluate which foods would really fit in Ready Made and which in recipes.
#   "smallAddition": are minor additions to a meal, like a fruit, vegetable, dairy products. They can usually be consumed by themselves.
#   TODO: "ingredient": New category for items that can only be ingredients in food synergies/recipes that cannot be consumed by themselves. For example: herbs and spices, oils, foods that need to be precooked before consumption


# TODO: have all items have at least some attributes (prices, timeworth, foodType)? - LATER NOTE: rather than that just have the same attributes for all item types so that there is a consistent structure.

# Import all the necessities. Shelve for data storage, pprint for printing messier strings(dictionaries most of all),
#  random for choosing foods, logging for debugging

import shelve, pprint, random, logging
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG, format=" %(asctime)s - %(levelname)s - %(message)s"
)
logging.debug("Start of program")


class Category:
    def __init__(self, category_id, name, parent_id, time_weight):
        self.category_id = category_id
        self.name = name
        self.parent_id = parent_id
        self.time_weight = time_weight


# Main categories will currently be hardcoded, but in the future they could be added through the GUI
# A main category is a category with no parent_id, it's the highest level of categorization


category: Category = Category(0, "", 0, 0)


class FoodItem:
    def __init__(
        self,
        item_id,
        name,
        category_id,
        subcategory_id,
        preparationType,
        ingredients,
        instructions,
        timeToPrepare,
        # TODO: Implement
        # satiation_weight, - determines the estimated amount of satiation an item may provide,
        # url, - optional - provides the url for the food item - this can be the link to the original recipe, article url to buy in an online grocery store or link to the restaurant the item is getting ordered from
    ):
        self.item_id = item_id
        self.name = name
        self.category_id = category_id
        self.subcategory_id = subcategory_id
        self.preparationType = preparationType
        self.ingredients = ingredients
        self.instructions = instructions
        self.timeToPrepare = timeToPrepare
        # self.satiation_weight = satiation_weight
        # self.url = url


itemExample = FoodItem(0, "", 0, 0, "", "", "", "")


# TODO: Rename to getFoods
# getShelve - Create or open the local shelve holding all foods, categorized in subgroups and return it's contents
def getShelve():

    Path("dietData").mkdir(
        parents=True, exist_ok=True
    )  # Create data directory if it don't exist, if it does, skip this line

    data = shelve.open("dietData\\dietPlannerData")  # Open/Create shelve files

    # try allocating all foods into variable, if that doesn't exist, initialize a fresh shelve with all basic categories and save it into the variable
    try:
        dataVar = data["foods"]
    except KeyError:
        data["foods"] = initShelve()
        dataVar = data["foods"]
    data.close()  # close the shelve file, we got from it what we needed

    return dataVar  # return the data gotten from the shelve


# TODO: Implement
def getDietPlan():
    print("WIP")


def getDietPlans():
    print("WIP")


def initDietPlans():
    # Add to initShelve
    print("WIP")


def getActiveDietPlan():
    print("WIP")


def editDietPlan(id, modifiedDietPlan):
    print("WIP")


def deleteDietPlan(id):
    print("WIP")


def saveDietPlan(plan):
    print("WIP")


# initShelve - Initializes a fresh food data shelve file, with all the needed categories and their respective subcategories
def initShelve():

    seededDictionary = {}  # reserves the dictionary we are about to fill out

    categories = getInitialCategorySeeds()

    items = getInitialItemSeeds()

    seededDictionary["categories"] = categories
    seededDictionary["items"] = items

    return seededDictionary


def getCategoryFromName(allCategories, categoryName):
    for category in allCategories:
        if category["name"] == categoryName:
            return category


def getCategoryFromId(allCategories, id):
    for category in allCategories:
        if category["category_id"] == id:
            return category


# modifyShelve - modifies the data in the shelve file, only removal and addition of items is available at this point
# TODO: main category addition and removal, with input validation and security
# TODO: Add item attribute modification
# Call example modifyShelve(
#                           mode - action(add or del)
#                           categoryList - list of categories in which to append or remove the given item
#                           itemList - the first value is the items name while the remaining values are the item's attribute values
#                           )
# TODO: Splinter this into separate functions
def modifyShelve(updatedFoods):

    data = shelve.open("dietData\\dietPlannerData")
    data["foods"] = updatedFoods
    data.close()


def addFoodItem(selectedCategoryName, selectedSubCategoryName, itemList):
    foods = getShelve()

    latestItemId = 0

    items = foods["items"]
    latestItemId = items[-1]["item_id"]

    selectedCategory = getCategoryFromName(foods["categories"], selectedCategoryName)

    selectedSubcategory = getCategoryFromName(
        foods["categories"], selectedSubCategoryName
    )

    foundItem = next(
        (item for item in foods["items"] if item["name"] == itemList), None
    )

    if foundItem:
        print("Item already exists")
        return
    else:
        foods["items"].append(
            {
                "item_id": latestItemId + 1,
                "name": itemList,
                "category_id": selectedCategory["category_id"],
                "subcategory_id": selectedSubcategory["category_id"],
                "preparationType": "",
                "ingredients": "",
                "instructions": "",
                "timeToPrepare": "",
            }
        )
    modifyShelve(foods)


def removeItem(selectedCategoryName, selectedSubCategoryName, itemList):
    foods = getShelve()

    foundItem = next(
        (item for item in foods["items"] if item["name"] == itemList), None
    )
    # deletion goes through the same motions as addition only that instead of adding it deletes the given item
    # for deletion we only take the item's name

    if not foundItem:
        print("Item doesn't exist")
        return
    else:
        foods["items"].remove(foundItem)
    # in the end whatever changes have been made are saved to the shelve
    # TODO: check whether any values have actually changed to decide if it's even worth saving

    modifyShelve(foods)

    return


def editItem(selectedCategoryName, selectedSubCategoryName, itemList, itemId):
    foods = getShelve()

    selectedCategory = getCategoryFromName(foods["categories"], selectedCategoryName)

    selectedSubcategory = getCategoryFromName(
        foods["categories"], selectedSubCategoryName
    )

    foundItem = next(
        (item for item in foods["items"] if item["item_id"] == itemId), None
    )

    if not foundItem:
        print("Item doesn't exist")
        return
    else:
        foundItem["name"] = itemList
        foundItem["category_id"] = selectedCategory["category_id"]
        foundItem["subcategory_id"] = selectedSubcategory["category_id"]

    # in the end whatever changes have been made are saved to the shelve
    # TODO: check whether any values have actually changed to decide if it's even worth saving

    modifyShelve(foods)

    return


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

    categories = [
        category for category in food["categories"] if category["parent_id"] == None
    ]

    plan["Days"] = []

    for day in range(
        length
    ):  # Day loop, generates a dictionary with the current day's value as its key
        plan["Days"].append([])
        plan["Days"][day] = {}
        plan["Days"][day]["Meals"] = []
        for meal in range(
            3
        ):  # Meal loop, generates a dictionary with the current meal's value, also chooses the meal's food
            while True:  # this loop chooses current meal's food category,
                # if it chooses one of the categories that have expended their occurence numbers it loops again until it chooses an available category
                category = random.choice(categories)
                if (
                    category["name"].lower() == "takeout"
                    and takeOutCount > takeOutNum
                    or category["name"].lower() == "recipes"
                    and recipeCount > recipeNum
                ):
                    continue
                else:
                    break
            plan["Days"][day]["Meals"].append({})
            if (
                category["name"] == "recipes"
            ):  # this conditional statement chooses the meal's food item, recipes have a different approach to them adding their attributes to the end

                categoryFood = [
                    item
                    for item in food["items"]
                    if item["category_id"] == category["category_id"]
                ]

                foodChoice = random.choice(categoryFood)

                plan["Days"][day]["Meals"][meal][foodChoice["name"]] = foodChoice
                recipeCount += 1  # with the addition of a recipe we add a notch to the recipe count
            else:

                items = []

                while len(items) < 1:

                    subcategories = [
                        subcategory
                        for subcategory in food["categories"]
                        if subcategory["parent_id"] == category["category_id"]
                    ]
                    subcategory = random.choice(subcategories)

                    items = [
                        item
                        for item in food["items"]
                        if item["subcategory_id"] == subcategory["category_id"]
                    ]

                foodChoice = random.choice(items)

                if category["name"].lower() == "smallAddition":
                    plan["Days"][day]["Meals"][meal] = (
                        category["name"] + "\\" + foodChoice["name"]
                    )
                else:
                    plan["Days"][day]["Meals"][meal] = (
                        subcategory["name"] + "\\" + foodChoice["name"]
                    )
                    if category["name"].lower() == "takeout":
                        takeOutCount += 1  # with the addition of a takeout variant we add a notch to the takeout count

    return plan


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


def getAllSubcategoriesFromCategories(allCategories):
    subCategories = []
    for category in allCategories:
        if category["parent_id"] != None:
            subCategories.append(category["name"])
    return subCategories


def getInitialCategorySeeds():
    return [
        {"category_id": 0, "name": "takeOut", "parent_id": None, "time_weight": 1},
        {"category_id": 1, "name": "recipes", "parent_id": None, "time_weight": 3},
        {"category_id": 2, "name": "readyMade", "parent_id": None, "time_weight": 2},
        {
            "category_id": 3,
            "name": "smallAddition",
            "parent_id": None,
            "time_weight": 1,
        },
        {"category_id": 4, "name": "McDonalds", "parent_id": 0, "time_weight": 1},
        {"category_id": 5, "name": "Mango", "parent_id": 0, "time_weight": 1},
        {"category_id": 6, "name": "Astoria", "parent_id": 0, "time_weight": 1},
        {"category_id": 7, "name": "Takos", "parent_id": 0, "time_weight": 1},
        {
            "category_id": 8,
            "name": "Quick",
            "parent_id": 1,
            "time_weight": 1,
        },
        {"category_id": 9, "name": "Low", "parent_id": 1, "time_weight": 2},
        {"category_id": 10, "name": "Medium", "parent_id": 1, "time_weight": 3},
        {"category_id": 11, "name": "Hard", "parent_id": 1, "time_weight": 4},
        {"category_id": 12, "name": "Lidl", "parent_id": 2, "time_weight": 1},
        {
            "category_id": 13,
            "name": "Hofer",
            "parent_id": 2,
            "time_weight": 1,
        },
        {
            "category_id": 14,
            "name": "Spar",
            "parent_id": 2,
            "time_weight": 1,
        },
        {
            "category_id": 15,
            "name": "Tuš",
            "parent_id": 2,
            "time_weight": 1,
        },
        {"category_id": 16, "name": "Fruit", "parent_id": 3, "time_weight": 1},
        {"category_id": 17, "name": "Veggies", "parent_id": 3, "time_weight": 1},
        {
            "category_id": 18,
            "name": "Sauces",
            "parent_id": 3,
            "time_weight": 1,
        },
        {"category_id": 19, "name": "Dairy", "parent_id": 3, "time_weight": 1},
        {"category_id": 20, "name": "Bootl's", "parent_id": 0, "time_weight": 1},
    ]


def getInitialItemSeeds():
    return [
        {
            "item_id": 0,
            "name": "BigMac",
            "category_id": 4,
            "subcategory_id": 8,
            "preparationType": "Quick",
            "ingredients": "Bread, Meat, Cheese, Lettuce, Sauce",
            "instructions": "Put the meat in the bread, add cheese, lettuce and sauce",
            "timeToPrepare": "15",
        },
        {
            "item_id": 1,
            "name": "Cheeseburger",
            "category_id": 4,
            "subcategory_id": 8,
            "preparationType": "Quick",
            "ingredients": "Bread, Meat, Cheese, Sauce",
            "instructions": "Put the meat in the bread, add cheese and sauce",
            "timeToPrepare": "10",
        },
        {
            "item_id": 2,
            "name": "Chicken Nuggets",
            "category_id": 4,
            "subcategory_id": 8,
            "preparationType": "Quick",
            "ingredients": "Chicken, Breading, Sauce",
            "instructions": "Fry the chicken, add breading and sauce",
            "timeToPrepare": "20",
        },
        {
            "item_id": 3,
            "name": "Vegetarian Burger",
            "category_id": 4,
            "subcategory_id": 8,
            "preparationType": "Quick",
            "ingredients": "Bread, Vegetables, Cheese, Sauce",
            "instructions": "Put the vegetables in the bread, add cheese and sauce",
            "timeToPrepare": "10",
        },
        {
            "item_id": 4,
            "name": "Pasta",
            "category_id": 5,
            "subcategory_id": 8,
            "preparationType": "Quick",
            "ingredients": "Pasta, Sauce, Cheese",
            "instructions": "Boil the pasta, add sauce and cheese",
            "timeToPrepare": "15",
        },
        {
            "item_id": 5,
            "name": "Pizza",
            "category_id": 5,
            "subcategory_id": 8,
            "preparationType": "Quick",
            "ingredients": "Dough, Sauce, Cheese, Toppings",
            "instructions": "Put the sauce on the dough, add cheese and toppings",
            "timeToPrepare": "20",
        },
        {
            "item_id": 6,
            "name": "Pasta Carbonara",
            "category_id": 5,
            "subcategory_id": 8,
            "preparationType": "Quick",
            "ingredients": "Pasta, Eggs, Cheese, Bacon",
            "instructions": "Boil the pasta, add eggs, cheese and bacon",
            "timeToPrepare": "15",
        },
        {
            "item_id": 7,
            "name": "Pasta Bolognese",
            "category_id": 5,
            "subcategory_id": 8,
            "preparationType": "Quick",
            "ingredients": "Pasta, Meat, Sauce, Cheese",
            "instructions": "Boil the pasta, add meat, sauce and cheese",
            "timeToPrepare": "15",
        },
    ]
