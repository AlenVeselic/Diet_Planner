from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page


class Profile(Page):

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        self.label = Label(self, text="WIP: User Profile")
        self.label.pack(side="top", fill="both", expand=True)

    def refresh(self):
        self.root.update()
