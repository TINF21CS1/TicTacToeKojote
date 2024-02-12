import tkinter as tk
from .base_frame import base_frame
from .field_frame import Field

class EndScreen(base_frame):
    def __init__(self, master, message):
        super().__init__(master)
        self._create_widgets(message)
        self._display_widgets()

    def _create_widgets(self, message):
        from .menu import Menu
        self.lblWinner = tk.Label(self, width=20, height=5, bg="white", text=message)
        self.btnPlayAgain = tk.Button(self, width=20, height=5, text="Play Again", command=lambda: self.master.show(Field))
        self.btnMainMenu = tk.Button(self, text="Main Menu", width=20, height=5, command=lambda: self.master.show(Menu))

    def _display_widgets(self):
        self.lblWinner.pack()
        self.btnPlayAgain.pack()
        self.btnMainMenu.pack()

class WinScreen(EndScreen):
    def __init__(self, master):
        super().__init__(master, "You won the game!")

class LooseScreen(EndScreen):
    def __init__(self, master):
        super().__init__(master, "You lost the game!")