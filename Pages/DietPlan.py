from pprint import pprint
from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page
import dietPlanner


class DietPlanPage(Page):
    label = None
    canvas = None
    verticalScrollbar = None
    frame = None
    plan = None

    actionButtons: list[Widget] = []

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        self.canvas = Canvas(self, borderwidth=0, background="white")

        self.frame = ttk.Frame(self)

        self.verticalScrollBar = Scrollbar(
            self, orient=VERTICAL, command=self.canvas.yview
        )

        self.canvas.configure(yscrollcommand=self.verticalScrollBar.set)

        self.verticalScrollBar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas.create_window(
            (4, 4), window=self.frame, anchor=NW, tags="self.foodFrame"
        )

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.label = Label(self.frame, text="No diet plan generated yet.")
        self.label.pack(side="top", fill="both", expand=True)

        self.dietPlanFrame = ttk.Frame(self.frame)
        self.dietPlanFrame.pack(side="top", fill="both", expand=True)

        self.removeActionButtons()
        self.generateActionButtons()

    def updateLabelWithDietPlanObject(self):
        self.label["text"] = "\n".join(
            "{}\n {}\n".format(k, d)
            for k, d in (dietPlanner.createPlan(5, 2, 2)).items()
        ).replace(",", ",\n")

    def createDietPlan(self):
        self.plan = dietPlanner.createPlan(5, 2, 2)

    def discardDietPlan(self):
        self.plan = None

    def saveDietPlan(self):
        dietPlanner.saveDietPlan(self.plan)

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

                    if isinstance(meal, dict):
                        foodLabel = Label(
                            self.dietPlanFrame,
                            text=f"  Recipe: {list(meal.keys())[0]}",
                            justify="left",
                            anchor=W,
                        )
                    else:
                        foodLabel = Label(
                            self.dietPlanFrame,
                            text=f"  {meal}",
                            justify="left",
                            anchor=W,
                        )

                    foodLabel.pack(side="top", fill="x")

    def generateActionButtons(self):
        buttonframe = ttk.Frame(self.frame)

        if not self.plan:
            createDietPlanButton = ttk.Button(
                buttonframe,
                text="Generate Diet Plan",
                command=lambda: [self.createDietPlan(), self.refresh()],
            )

            createDietPlanButton.pack()
            self.actionButtons.append(createDietPlanButton)
        else:
            acceptButton = ttk.Button(
                buttonframe,
                text="Accept",
                command=lambda: [
                    self.saveDietPlan(),
                    self.root.dietPlanArchive.show(),
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

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))
