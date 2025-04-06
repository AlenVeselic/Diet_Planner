from tkinter import *

import ttkbootstrap as ttk


class Page(ttk.Frame):
    root: ttk.Window = None

    def __init__(self, root, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.root = root

    def show(self):
        self.lift()
        self.root.update()
