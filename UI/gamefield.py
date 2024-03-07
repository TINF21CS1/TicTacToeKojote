import tkinter as tk

from .endscreen import EndScreen

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
            button.config(command=lambda e=position: self._game_input(e))

    def draw_field(self, matrix=None, position=None, value=None): #either matrix as a 3x3 list or position and value need to be provided
        if matrix != None:
            for i, row in enumerate(matrix):
                for j, e in enumerate(row):
                    self.view.fields[(i, j)].config(text=e)
        else:
            self.view.fields[position].config(text=value)

    def change_active_player(self, player_id: int):
        for i, player in enumerate(self.view.master.player):
            player.highlight(i == player_id)

    def turn(self, *args):
        root = self.view.master.master
        queue = root.in_queue.get()
        self.draw_field(matrix=queue['playfield'])
        self.change_active_player(queue['next_player'])

    def _game_input(self, position):
        root = self.view.master.master
        root.out_queue.put({'message_type': 'game/make_move', 'args': {'x': position[0], 'y': position[1]}})