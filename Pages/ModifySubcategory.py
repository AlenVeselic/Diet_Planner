from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page


class ModifySubcategory(Page):

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        # self.canvas = Canvas(self, borderwidth=0, background="white")

        # self.frame = ttk.Frame(self)

        # self.verticalScrollBar = Scrollbar(
        #     self, orient=VERTICAL, command=self.canvas.yview
        # )

        # self.canvas.configure(yscrollcommand=self.verticalScrollBar.set)

        # self.verticalScrollBar.pack(side=RIGHT, fill=Y)
        # self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        # self.canvas.create_window(
        #     (4, 4), window=self.frame, anchor=NW, tags="self.foodFrame"
        # )

        # self.frame.bind("<Configure>", self.onFrameConfigure)

        self.label = Label(self.frame, text="WIP: ADD/EDIT Subcategories")
        self.label.pack(side="top", fill="both", expand=True)

    def refresh(self):
        self.root.update()

    # def onFrameConfigure(self, event):
    #     """Reset the scroll region to encompass the inner frame"""
    #     self.canvas.configure(scrollregion=self.canvas.bbox(ALL))
