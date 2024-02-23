import tkinter as tk

from .endscreen import WinScreen, LooseScreen
from .network import game_input

class gamefield(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self.fields = {}
        for i in range(3):
            for j in range(3):
                self.fields[(i, j)] = tk.Button(self, text="")

    def _display_widgets(self):
        self.columnconfigure(tuple(range(3)), weight=1)
        self.rowconfigure(tuple(range(3)), weight=1)
        for position, field in self.fields.items():
            field.grid(sticky=tk.N+tk.S+tk.E+tk.W, row=position[0], column=position[1])

class gamefield_controller:
    def __init__(self, view: gamefield):
        self.view = view
        self._bind()
    
    def _bind(self):
        for position, button in self.view.fields.items():
            button.config(command=lambda e=position: game_input(self, e))

    def draw_field(self, matrix=None, position=None, value=None): #either matrix as a 3x3 list or position and value need to be provided
        if matrix != None:
            for i, row in enumerate(matrix):
                for j, e in enumerate(row):
                    self.view.fields[(i, j)].config(text=e)
        else:
            self.view.fields[position].config(text=value)

    def trigger_end(self, win: bool = True):
        if win:
            self.view.master.master.show(WinScreen)
        else:
            self.view.master.master.show(LooseScreen)

    def change_active_player(self, player_id: int):
        for i, player in enumerate(self.view.master.player):
            player.highlight(i == player_id)