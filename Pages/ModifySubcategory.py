from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page


class ModifySubcategory(Page):

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        self.label = Label(self.frame, text="WIP: ADD/EDIT Subcategories")
        self.label.pack(side="top", fill="both", expand=True)

    def refresh(self):
        self.root.update()
