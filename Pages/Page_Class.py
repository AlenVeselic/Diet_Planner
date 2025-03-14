from tkinter import *


class Page(Frame):
    root = None

    def __init__(self, root, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.root = root

    def show(self):
        self.lift()
        self.root.update()
