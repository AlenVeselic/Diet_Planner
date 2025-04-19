from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page
import DietPlanner


class ActiveDietPlan(Page):
    plan = None

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        self.label = Label(self.frame, text="WIP: Active diet plan")
        self.label.pack(side="top", fill="both", expand=True)

        self.dietPlanFrame = ttk.Frame(self.frame)
        self.dietPlanFrame.pack(side="top", fill="both", expand=True)

    def refresh(self):
        for widget in self.dietPlanFrame.winfo_children():
            widget.destroy()
        self.dietPlanFrame.pack_forget()
        self.dietPlanFrame = ttk.Frame(self.frame)
        self.dietPlanFrame.pack(side="top", fill="both", expand=True)
        # DietPlanner.getActiveDietPlan
        self.plan = DietPlanner.getActiveDietPlan()
        if self.plan:
            self.label["text"] = f"Active diet plan: {self.plan['Name']}"

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

        self.verticalScrollBar.update()
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))
        self.root.update()
