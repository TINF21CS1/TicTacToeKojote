import tkinter as tk
from enum import Enum, auto

from .base_frame import base_frame

class player_type(Enum):
    local = auto()
    ai = auto()
    network = auto()

class gamefield(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self.fields = {}
        for i in range(3):
            for j in range(3):
                self.fields[(i, j)] = tk.Button(self, text="", command=lambda a=i, b=j: self._set_field(self.fields[(a, b)]))

    def _display_widgets(self):
        self.columnconfigure(tuple(range(3)), weight=1)
        self.rowconfigure(tuple(range(3)), weight=1)
        for position, field in self.fields.items():
            field.grid(sticky=tk.N+tk.S+tk.E+tk.W, row=position[0], column=position[1])

    def _set_field(self, button):
        button.config(text="X")

class player_info(tk.Frame):
    def __init__(self, master, number, name, type):
        super().__init__(master)
        self._create_widgets(number, name, type)
        self._display_widgets()

    def _create_widgets(self, number, name, type):
        
        self.heading = tk.Label(self, text=f'Player {number}', font=self.master.master.title_font)
        self.name = tk.Label(self, text=name)
        match type:
            case player_type.local:
                self.symbol = tk.Label(self, text="Lokal")
            case player_type.ai:
                self.symbol = tk.Label(self, text="Computer")
            case player_type.network:
                self.symbol = tk.Label(self, text="Online")
            #durch pictogramme ersetzen

    def _display_widgets(self):
        self.heading.grid(row=0, column=0, columnspan=2)
        self.name.grid(row=1, column=0)
        self.symbol.grid(row=1, column=1)

class Field(base_frame):
    def __init__(self, master):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self.heading = tk.Label(self, text="Tic Tac Toe Kojote", font=self.master.title_font)
        self.player1 = player_info(self, 1, "Alfred", player_type.local)
        self.player2 = player_info(self, 2, "Paul03", player_type.ai)
        self.gamefield = gamefield(self)
        self.close = tk.Button(self, text="close", command=self.master.show_menu)

    def _display_widgets(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.heading.grid(row=0, column=0, columnspan=3)
        self.player1.grid(row=1, column=0)
        self.player2.grid(row=1, column=2)
        self.gamefield.grid(sticky=tk.N+tk.S+tk.E+tk.W, row=2, column=1)
        self.close.grid(row=3, column=2)