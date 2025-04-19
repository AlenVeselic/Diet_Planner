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

    actionButtons: list[Widget] = []

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        self.label = Label(self.frame, text="No diet plan generated yet.")
        self.label.pack(side="top", fill="both", expand=True)

        self.dietPlanFrame = ttk.Frame(self.frame)
        self.dietPlanFrame.pack(side="top", fill="both", expand=True)

        self.removeActionButtons()
        self.generateActionButtons()

    def updateLabelWithDietPlanObject(self):
        self.label["text"] = "\n".join(
            "{}\n {}\n".format(k, d)
            for k, d in (DietPlanner.createPlan(5, 2, 2)).items()
        ).replace(",", ",\n")

    def createDietPlan(self):
        self.plan = DietPlanner.createPlan(5, 2, 2)

    def discardDietPlan(self):
        self.plan = None

    def saveDietPlan(self):
        DietPlanner.saveDietPlan(self.plan)

        self.plan = None

    def refresh(self):
        self.label["text"] = "No diet plan generated yet."
        for widget in self.dietPlanFrame.winfo_children():
            widget.destroy()
        self.dietPlanFrame.pack_forget()
        self.dietPlanFrame = ttk.Frame(self.frame)
        self.dietPlanFrame.pack(side="top", fill="both", expand=True)

        self.removeActionButtons()
        self.generateActionButtons()

        if self.plan:
            self.label["text"] = "Diet plan generated:"

            for index, day in enumerate(self.plan["Days"]):
                dayLabel = Label(
                    self.dietPlanFrame,
                    text=f"Day {index + 1}",
                    justify="left",
                    anchor=W,
                )
                dayLabel.pack(side=("top"), fill="x")

                for index, meal in enumerate(day["Meals"]):
                    mealLabel = Label(
                        self.dietPlanFrame,
                        text=f" Meal {index + 1}",
                        justify="left",
                        anchor=W,
                    )
                    mealLabel.pack(side="top", fill="x")

                    foodItemFrame = ttk.Frame(self.dietPlanFrame)

                    if isinstance(meal, dict):
                        foodLabel = Label(
                            foodItemFrame,
                            text=f"  Recipe: {list(meal.keys())[0]}",
                            justify="left",
                            anchor=W,
                        )
                    else:
                        foodLabel = Label(
                            foodItemFrame,
                            text=f"  {meal}",
                            justify="left",
                            anchor=W,
                        )

                    foodLabel.pack(side=LEFT)

                    replaceButton = ttk.Button(
                        foodItemFrame, text="Replace", command=lambda: print("test")
                    )
                    replaceButton.pack(side=RIGHT)

                    foodItemFrame.pack(side=TOP, fill=X)

    def generateActionButtons(self):
        buttonframe = ttk.Frame(self.frame)

        if not self.plan:
            settingsLabel = ttk.Label(
                buttonframe, text="Diet plan settings"
            )  # TODO: Add ability to set Diet plan parameters from DietPlanner here
            settingsLabel.pack()
            createDietPlanButton = ttk.Button(
                buttonframe,
                text="Generate Diet Plan",
                command=lambda: [self.createDietPlan(), self.refresh()],
            )

            createDietPlanButton.pack()
            self.actionButtons.append([settingsLabel, createDietPlanButton])
        else:
            acceptButton = ttk.Button(
                buttonframe,
                text="Accept",
                command=lambda: [
                    self.saveDietPlan(),
                    self.root.pages["DietPlanArchive"].show(),
                ],
            )

            acceptButton.pack(side="right")
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

            discardButton.pack(side="left")
            self.actionButtons.append(discardButton)

        buttonframe.pack(side="top", fill="both", expand=True)

        self.actionButtons.append(buttonframe)

    def removeActionButtons(self):
        for button in self.actionButtons:
            button.pack_forget()
        self.actionButtons = []
