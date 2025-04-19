from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page


class Profile(Page):

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        self.label = Label(self.frame, text="WIP: User Profile")
        self.label.pack(side="top", fill="both", expand=True)

        self.weightLabel = Label(self.frame, text="Weight")
        self.weightLabel.pack(side=LEFT, fill="x", expand=True)
        self.weightValueLabel = Label(self.frame, text="9000 KG")
        self.weightValueLabel.pack(side=RIGHT, fill="x", expand=True)

    def refresh(self):
        self.root.update()
