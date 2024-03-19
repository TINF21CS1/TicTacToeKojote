import tkinter as tk

class base_frame(tk.Frame):
    """
    Base class for all frames in the game. This class is used to set the background color of all frames to white.
    """
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='#FFFFFF')