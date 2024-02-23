import tkinter as tk
from tkinter import _tkinter
from tkinter import font as tkfont
import sys

from .menu import Menu
from.endscreen import WinScreen

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        start_width = 500
        min_width = 400
        start_height = 300
        min_height = 250

        self.geometry(f"{start_width}x{start_height}")
        self.minsize(width=min_width, height=min_height)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Tic Tac Toe Kojote")
        self.geometry("700x500")
        self.frames = {}
        self.current_frame = None

        self.show(Menu, True)

    def show(self, Frame, cache=False):
        if(self.current_frame != None):
            try:
                self.current_frame.grid_forget()
                self.current_frame.destroy()
            except _tkinter.TclError:
                pass
        if(cache):
            if(Frame.__name__ not in self.frames):
                self.add_frame(Frame)
            frame = self.frames[Frame.__name__]
        else:
            frame = Frame(self)
            frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = frame
        return frame
        
    def add_frame(self, Frame):
        self.frames[Frame.__name__] = Frame(self)
        self.frames[Frame.__name__].grid(row=0, column=0, sticky="nsew")

    def show_menu(self):
        self.show(Menu)

    def start_mainloop(self):
        self.mainloop()

def main():
    app = Root()
    app.start_mainloop()