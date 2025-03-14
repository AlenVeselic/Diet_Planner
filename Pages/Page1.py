from tkinter import *

from Pages.Page_Class import Page


class Page1(Page):
    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)
        label = Label(self, text="This is page 1")
        label.pack(side="top", fill="both", expand=True)
