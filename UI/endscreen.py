#import tkinter as tk
from .lib import tttk_tk as tk
from .base_frame import base_frame
#from .field_frame import Field

class EndScreen(base_frame):
    def __init__(self, master, win:bool, *args, **kwargs):
        super().__init__(master)
        self._create_widgets(win)
        self._display_widgets()

    def _create_widgets(self, win:bool):
        message = "You won the game!" if win else "You lost the game!"
        self.lblWinner = tk.Label(self, width=20, height=5, bg="white", text=message)
        #self.btnPlayAgain = tk.Button(self, width=20, height=5, text="Play Again", command=lambda: self.master.show(Field))
        self.btnMainMenu = tk.Button(self, text="Main Menu", width=20, height=5, command=lambda: self.master.show_menu())

    def _display_widgets(self):
        self.lblWinner.pack()
        #self.btnPlayAgain.pack()
        self.btnMainMenu.pack()