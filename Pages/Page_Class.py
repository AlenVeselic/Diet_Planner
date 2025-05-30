from tkinter import *

import ttkbootstrap as ttk


class Page(ttk.Frame):
    root: ttk.Window = None
    frame: ttk.Frame = None

    def __init__(self, root: ttk.Window, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        self.root = root

        self.canvas = Canvas(self, borderwidth=0, background="white")

        self.frame = ttk.Frame(self.canvas, padding=5)

        self.verticalScrollBar = Scrollbar(
            self, orient=VERTICAL, command=self.canvas.yview
        )

        self.canvas.configure(yscrollcommand=self.verticalScrollBar.set)

        self.verticalScrollBar.pack(side=RIGHT, fill=Y)

        windowWidth = self.root.winfo_width() - 50
        self.canvas.create_window(
            (4, 4),
            window=self.frame,
            anchor=N,
            tags="self.frame",
        )

        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        self.bind("<Enter>", self.boundToMouseWheel)
        self.bind("<Leave>", self.unboundToMouseWheel)

        self.canvas.pack(side=TOP, fill=BOTH, expand=True)

    def onCanvasConfigure(self, event: Event):
        canvas_frame: Widget = self.canvas.nametowidget(
            self.canvas.itemcget("self.frame", "window")
        )
        min_width = canvas_frame.winfo_reqwidth()
        min_height = canvas_frame.winfo_reqheight()
        if min_width < event.width:
            self.canvas.itemconfigure("self.frame", width=event.width)

        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

    def onMouseWheel(self, event: Event):

        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def boundToMouseWheel(self, event):

        self.bind_all("<MouseWheel>", self.onMouseWheel)

    def unboundToMouseWheel(self, event):

        self.unbind_all("<MouseWheel>")

    def show(self):

        self.lift()
        self.root.update()
