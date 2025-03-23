from tkinter import *
import ttkbootstrap as ttk

from Pages.Page_Class import Page
import dietPlanner


class DietPlanPage(Page):
    label = None
    canvas = None
    verticalScrollbar = None
    frame = None

    def __init__(self, root, *args, **kwargs):
        Page.__init__(self, root, *args, **kwargs)

        self.canvas = Canvas(self, borderwidth=0, background="white")

        self.frame = ttk.Frame(self)

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

        self.label = Label(self.frame, text="No diet plan generated yet.")
        self.label.pack(side="top", fill="both", expand=True)

        buttonframe = ttk.Frame(self.frame)

        createDietPlanButton = ttk.Button(
            buttonframe,
            text="Create Diet Plan",
            command=self.updateLabelWithDietPlan,
        )

        createDietPlanButton.pack()
        buttonframe.pack(side="top", fill="both", expand=True)

    def updateLabelWithDietPlan(self):
        self.label["text"] = "\n".join(
            "{}\n {}\n".format(k, d)
            for k, d in (dietPlanner.createPlan(5, 2, 2)).items()
        ).replace(",", ",\n")

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))
