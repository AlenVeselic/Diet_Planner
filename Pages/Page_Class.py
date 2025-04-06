from tkinter import *

import ttkbootstrap as ttk


class Page(ttk.Frame):
    root: ttk.Window = None
    frame: ttk.Frame = None

    def __init__(self, root, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.root = root

        self.canvas = Canvas(self, borderwidth=0, background="white")

        self.frame = ttk.Frame(self.canvas, padding="5")
        # self.foodFrame.pack(side="top", fill="both", expand=True)

        self.verticalScrollBar = Scrollbar(
            self, orient=VERTICAL, command=self.canvas.yview
        )

        self.canvas.configure(yscrollcommand=self.verticalScrollBar.set)

        self.verticalScrollBar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas.create_window(
            (4, 4), window=self.frame, anchor=NW, tags="self.foodFrame"
        )

        self.frame.bind("<Configure>", self.onFrameConfigure)

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

    def show(self):
        self.lift()
        self.root.update()
