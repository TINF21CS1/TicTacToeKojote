import tkinter as tk
from enum import Enum, auto

from .base_frame import base_frame
from .gamefield import gamefield, gamefield_controller
from .network import get_player

class player_type(Enum):
    local = auto()
    ai = auto()
    network = auto()
    unknown = auto()

class player(tk.Frame):
    def __init__(self, master, number):
        super().__init__(master)
        self._create_widgets(number)
        self._display_widgets()

    def _create_widgets(self, number):
        
        self.heading = tk.Label(self, text=f'Player {number}', font=self.master.master.title_font)
        self.name = tk.Label(self, text=f'Player {number}')
        self.symbol = tk.Label(self, text="unknown")
            
    def highlight(self, highlight=True):
        if(highlight):
            pass
        else:
            pass

    def set(self, name, type):
        self.name.config(text=name)
        match type:
            case player_type.local:
                self.symbol.config(text="Lokal")
            case player_type.ai:
                self.symbol.config( text="Computer")
            case player_type.network:
                self.symbol.config(text="Online")
            case player_type.unknown:
                self.symbol.config(text="unkown")
            #durch pictogramme ersetzen

    def _display_widgets(self):
        self.heading.grid(row=0, column=0, columnspan=2)
        self.name.grid(row=1, column=0)
        self.symbol.grid(row=1, column=1)

class field_controller():
    def __init__(self, view):
        self.view = view
        sub_controller = gamefield_controller(self.view.gamefield)
        for i, player in enumerate(self.view.player):
            player.set(**get_player(i))
        self._bind()

    def _bind(self):
        self.view.close.config(command=self.view.master.show_menu)

class Field(base_frame):
    def __init__(self, master, *args):
        super().__init__(master)
        self._create_widgets()
        self.controller = field_controller(self)
        self._display_widgets()

    def _create_widgets(self):
        self.heading = tk.Label(self, text="Tic Tac Toe Kojote", font=self.master.title_font)
        self.player = []
        self.player.append(player(self, 1))
        self.player.append(player(self, 2))
        self.gamefield = gamefield(self)
        self.close = tk.Button(self, text="close")

    def _display_widgets(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.heading.grid(row=0, column=0, columnspan=3)
        self.player[0].grid(row=1, column=0)
        self.player[1].grid(row=1, column=2)
        self.gamefield.grid(sticky=tk.N+tk.S+tk.E+tk.W, row=2, column=1)
        self.close.grid(row=3, column=2)