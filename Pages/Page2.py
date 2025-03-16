from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page
import dietPlanner


class Page2(Page):
    label = None

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        self.label = Label(self, text="No diet plan generated yet.")
        self.label.pack(side="top", fill="both", expand=True)

        frame = ttk.Frame(self)

        createDietPlanButton = ttk.Button(
            frame,
            text="Create Diet Plan",
            command=self.updateLabelWithDietPlan,
        )

        createDietPlanButton.pack()
        frame.pack(side="top", fill="both", expand=True)

    def updateLabelWithDietPlan(self):
        self.label["text"] = "\n".join(
            "{}\n {}\n".format(k, d)
            for k, d in (dietPlanner.createPlan(5, 2, 2)).items()
        ).replace(",", ",\n")
