from pprint import pprint
from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page
import DietPlanner


class DietPlanPage(Page):
    label = None
    canvas = None
    verticalScrollbar = None
    frame = None
    plan = None
    planLengthVariable = None
    recipeAmountVariable = None
    takeoutAmountVariable = None

    actionButtons: list[Widget] = []

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        self.label = Label(self.frame, text="No diet plan generated yet.")
        self.label.pack(side=TOP, fill=BOTH, expand=True)

        self.dietPlanFrame = ttk.Frame(self.frame)
        self.dietPlanFrame.pack(side=TOP, fill=BOTH, expand=True)

        self.removeActionButtons()
        self.generateActionButtons()

    def updateLabelWithDietPlanObject(self):
        self.label["text"] = "\n".join(
            "{}\n {}\n".format(k, d)
            for k, d in (DietPlanner.createPlan(5, 2, 2)).items()
        ).replace(",", ",\n")

    def createDietPlan(self):
        if (
            self.planLengthVariable
            and self.recipeAmountVariable
            and self.takeoutAmountVariable
            and not self.planLengthVariable.get() <= 0
            and not self.recipeAmountVariable.get() > self.planLengthVariable.get()
            and not self.takeoutAmountVariable.get() > self.planLengthVariable.get()
        ):
            self.plan = DietPlanner.createPlan(
                self.planLengthVariable.get(),
                self.recipeAmountVariable.get(),
                self.takeoutAmountVariable.get(),
            )
        else:
            print("Diet plan settings invalid or not set!")

    def discardDietPlan(self):
        self.plan = None

    def saveDietPlan(self):
        DietPlanner.saveDietPlan(self.plan)

        self.plan = None

    def refresh(self):
        self.label["text"] = "No diet plan generated yet."
        for widget in self.dietPlanFrame.winfo_children():
            widget.destroy()

        self.removeActionButtons()
        self.generateActionButtons()

        if self.plan:
            self.label["text"] = "Diet plan generated:"

            for index, day in enumerate(self.plan["Days"]):
                dayLabel = ttk.Label(
                    self.dietPlanFrame,
                    bootstyle="inverse-primary",
                    text=f"Day {index + 1}",
                    justify=CENTER,
                    anchor=CENTER,
                )
                dayLabel.pack(side=TOP, fill=X, pady=(5, 2))

                for index, meal in enumerate(day["Meals"]):
                    mealLabel = ttk.Label(
                        self.dietPlanFrame,
                        text=f"Meal {index + 1}",
                        justify=CENTER,
                        anchor=CENTER,
                    )
                    mealLabel.pack(side=TOP, fill=X)

                    foodItemFrame = ttk.Frame(self.dietPlanFrame)

                    if isinstance(meal, dict):
                        foodLabel = Label(
                            foodItemFrame,
                            text=f"Recipe: {list(meal.keys())[0]}",
                            justify=CENTER,
                            anchor=CENTER,
                        )
                    else:
                        foodLabel = Label(
                            foodItemFrame,
                            text=f"{meal}",
                            justify=CENTER,
                            anchor=CENTER,
                        )

                    foodLabel.pack(side=LEFT, expand=True)

                    replaceButton = ttk.Button(
                        foodItemFrame,
                        text="Replace",
                        command=lambda: print(
                            "test"
                        ),  # TODO: Implement food item replacement logic
                    )
                    replaceButton.pack(side=LEFT)

                    foodItemFrame.pack(side=TOP, fill=X, expand=True)

    def generateActionButtons(self):
        buttonframe = ttk.Frame(self.frame)

        if not self.plan:
            settingsFrame = ttk.Frame(buttonframe)
            settingsFrame.pack(side=TOP, pady=5)
            settingsLabel = ttk.Label(
                settingsFrame, text="Diet plan settings"
            )  # TODO: Add ability to set Diet plan parameters from DietPlanner here
            settingsLabel.pack(pady=(5, 0))

            planLengthFrame = ttk.Frame(settingsFrame)
            planLengthFrame.pack(side=TOP, pady=2)

            planLengthLabel = ttk.Label(planLengthFrame, text="Length in days")
            planLengthLabel.pack(side=TOP)
            self.planLengthVariable = IntVar()
            planLengthEntry = ttk.Entry(
                planLengthFrame, textvariable=self.planLengthVariable
            )
            planLengthEntry.pack(side=TOP)

            recipeAmountFrame = ttk.Frame(settingsFrame)
            recipeAmountFrame.pack(side=TOP, pady=2)

            recipeAmountLabel = ttk.Label(recipeAmountFrame, text="Recipe amount")
            recipeAmountLabel.pack(side=TOP)
            self.recipeAmountVariable = IntVar()
            recipeAmountEntry = ttk.Entry(
                recipeAmountFrame, textvariable=self.recipeAmountVariable
            )
            recipeAmountEntry.pack(side=TOP)

            takeoutAmountFrame = ttk.Frame(settingsFrame)
            takeoutAmountFrame.pack(side=TOP, pady=2)

            takeoutAmountLabel = ttk.Label(takeoutAmountFrame, text="Take Out amount")
            takeoutAmountLabel.pack(side=TOP)
            self.takeoutAmountVariable = IntVar()
            takeoutAmountEntry = ttk.Entry(
                takeoutAmountFrame, textvariable=self.takeoutAmountVariable
            )
            takeoutAmountEntry.pack(side=TOP)

            createDietPlanButton = ttk.Button(
                buttonframe,
                text="Generate Diet Plan",
                command=lambda: [
                    self.createDietPlan(),
                    self.refresh(),
                    self.update(),
                    self.canvas.configure(scrollregion=self.canvas.bbox(ALL)),
                ],
            )

            createDietPlanButton.pack(side=BOTTOM)
            self.actionButtons.extend(
                [
                    settingsFrame,
                    createDietPlanButton,
                ]
            )
        else:
            acceptButton = ttk.Button(
                buttonframe,
                text="Accept",
                command=lambda: [
                    self.saveDietPlan(),
                    self.root.pages["DietPlanArchive"].show(),
                ],
            )

            acceptButton.pack(side=RIGHT)
            self.actionButtons.append(acceptButton)

            discardButton = ttk.Button(
                buttonframe,
                text="Discard",
                command=lambda: [
                    self.discardDietPlan(),
                    self.refresh(),
                    self.root.update(),
                ],
            )

            discardButton.pack(side=LEFT)
            self.actionButtons.append(discardButton)

        buttonframe.pack(side=TOP, fill=BOTH, expand=True, pady=10, padx=10)

        self.actionButtons.append(buttonframe)

    def removeActionButtons(self):
        for button in self.actionButtons:
            button.pack_forget()
        self.actionButtons = []
