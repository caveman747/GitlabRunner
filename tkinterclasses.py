
#GUI related libraries
import tkinter as tk
from tkinter.ttk import Progressbar

#OS interaction libraries
import subprocess
from tkinter.ttk import Progressbar
#the skeleton of this is ripped directly from the answer to this stack overflow question
#https://stackoverflow.com/questions/63017238/how-to-switch-between-different-tkinter-canvases-from-a-start-up-page-and-return

class AdJoiner(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._mainCanvas = None
        self.title("AdJoiner")
        # The dictionary to hold the class type to switch to
        # Each new class passed here, will only have instance or object associated with it (i.e the result of the Key)
        self._allCanvases = dict()
        # Switch (and create) the single instance of StartUpPage
        self.switch_Canvas(StartUpPage)

    def switch_Canvas(self, Canvas_class):

        # Unless the dictionary is empty, hide the current Frame (_mainCanvas is a frame)
        if self._mainCanvas:
            self._mainCanvas.pack_forget()

        # is the Class type passed one we have seen before?
        canvas = self._allCanvases.get(Canvas_class, False)

        # if Canvas_class is a new class type, canvas is False
        if not canvas:
            # Instantiate the new class
            canvas = Canvas_class(self)
            # Store it's type in the dictionary
            self._allCanvases[Canvas_class] = canvas

            # Pack the canvas or self._mainCanvas (these are all frames)
        canvas.pack(pady=60)
        # and make it the 'default' or current one.
        self._mainCanvas = canvas


class StartUpPage(tk.Canvas):
    def __init__(self, master, *args, **kwargs):
        tk.Canvas.__init__(self, master, *args, **kwargs)
        tk.Frame(self)  # Here the parent of the frame is the self instance of type tk.Canvas
        tk.Label(self, text="Welcome to StartingBlock! \n This program was made to help setting up a Gitlab Runner that much easier \n Click Get Started to download dependencies"
                 ).grid(column=0, row=0)
        tk.Label(self, text="This program was made to help setting up a Gitlab Runner that much easier")

        def DownloadDeps():

            list = ["git", "curl"]
            for i in list:
                subprocess.run(["sudo", "apt", "install", i])
                self.canvas.update_idletasks()
                pb["value"] += 50
                txt["text"] = pb['value'], '%'

        pb = Progressbar(self.canvas, orient=tk.HORIZONTAL, length=100, mode="determinate")
        pb.pack()


        tk.Button(self, text="Download and install dependencies",
                  command=lambda: master.switch_Canvas(DownloadDeps())).grid(column=0, row=1)

