from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page
import dietPlanner


class DietPlanArchive(Page):

    planWidgets: list[Widget] = []
    label = None

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        self.label = Label(self.frame, text="Accepted Diet Plans")
        self.label.pack(side="top", fill=BOTH, expand=True)
        self.planList = ttk.Frame(self.frame)
        self.planList.pack(side=TOP, fill=BOTH, expand=True)

    def refresh(self):
        self.plans = dietPlanner.getDietPlans()

        for widget in self.planWidgets:
            widget.pack_forget()

        for plan in self.plans:
            planLabel = Label(self.planList, text=plan["Name"])
            planLabel.pack(side=TOP, fill="x", expand=False)
            self.planWidgets.append(planLabel)

        self.root.update()
