from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page


class ActiveDietPlan(Page):

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        self.label = Label(self, text="WIP: Active diet plan")
        self.label.pack(side="top", fill="both", expand=True)

    def refresh(self):
        # DietPlanner.getActiveDietPlan
        self.root.update()
