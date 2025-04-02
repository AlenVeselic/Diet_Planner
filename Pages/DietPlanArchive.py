from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page
import dietPlanner


class DietPlanArchive(Page):

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        self.label = Label(self, text="WIP: Diet Plan Archive")
        self.label.pack(side="top", fill="both", expand=True)

    def refresh(self):
        # dietPlanner.getDietPlans()
        self.root.update()
