import tkinter as tk
from enum import Enum, auto
from uuid import UUID

class input_methods(Enum):
    mouse = auto()
    qeyc = auto()
    uom= auto()

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
    def __init__(self, view: gamefield, starting_uuid: UUID, **kwargs):
        self.view = view
        self.currentplayer = starting_uuid
        self.input_methods = {input_methods.mouse: [], input_methods.qeyc: [], input_methods.uom: []}
        for uuid, input_method in kwargs.items():
            print(uuid, input_method)
            self.input_methods[input_method].append(UUID(uuid))
        self._bind()
    
    def _bind(self):
        for position, button in self.view.fields.items():
            button.config(command=lambda e=position: self._game_input(e, input_methods.mouse))
        for position, button in zip(self.view.fields.keys(),['q', 'w', 'e', 'a', 's', 'd', 'y', 'x', 'c']):
            self.view.bind(f'<KeyPress-{button}>', lambda e=position: self._game_input(e, input_methods.qeyc))
        for position, button in zip(self.view.fields.keys(),['u', 'i', 'o', 'j', 'k', 'l', 'm', ',', '.']):
            self.view.bind(f'<KeyPress-{button}>', lambda e=position: self._game_input(e, input_methods.uom))

    def draw_field(self, matrix=None, position=None, value=None): #either matrix as a 3x3 list or position and value need to be provided
        if matrix != None:
            for i, row in enumerate(matrix):
                for j, e in enumerate(row):
                    self.view.fields[(i, j)].config(text=e)
        else:
            self.view.fields[position].config(text=value)

    def change_active_player(self, player_id: int):
        self.currentplayer = player_id
        for player in self.view.master.player:
            player.highlight(highlight=(self.currentplayer == player.uuid))

    def turn(self, queue, *args):
        root = self.view.master.master
        self.draw_field(matrix=queue['playfield'])
        self.change_active_player(queue['next_player'])

    def _game_input(self, position, type: input_methods):
        root = self.view.master.master
        match(len(self.input_methods[type])):
            case 1:
                root.out_queue[self.input_methods[type][0]].put({'message_type': 'game/make_move', 'args': {'x': position[0], 'y': position[1]}})
            case 2:
                if(self.currentplayer in self.input_methods[type]):
                    root.out_queue[self.currentplayer].put({'message_type': 'game/make_move', 'args': {'x': position[0], 'y': position[1]}})
                else:
                    pass
            case _:
                pass