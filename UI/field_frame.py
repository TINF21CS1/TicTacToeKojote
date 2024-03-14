#import tkinter as tk
from .lib import tttk_tk as tk
from enum import Enum, auto

from .base_frame import base_frame
from .gamefield import gamefield, gamefield_controller
from .endscreen import EndScreen
from .messages import messages
from .chat import Chat

class player_type(Enum):
    local = auto()
    ai_weak = auto()
    ai_strong = auto()
    network = auto()
    unknown = auto()

class player(tk.Container):
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
            case player_type.ai_strong, player_type.ai_weak:
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
    def __init__(self, view, players):
        self.view = view
        self.sub_controller = gamefield_controller(self.view.gamefield)
        for player_lbl, player in zip(self.view.player, players):
            player_lbl.set(player.display_name, player_type.unknown)
        self._bind()

    def _bind(self):
        self.view.close.config(command=self.view.master.show_menu)

    def end(self, queue, *args):
        root = self.view.master
        root.show(EndScreen, queue['win'])

    def error(self, queue, *args):
        root = self.view.master
        msg = messages(type='move', message=queue['error_message'])
        msg.display()

class Field(base_frame):
    def __init__(self, master, chat, *args, starting_player, starting_player_symbol, opponent, opponent_symbol, **kwargs):
        super().__init__(master)
        self._create_widgets(chat)
        self.controller = field_controller(self, [starting_player, opponent])
        self._display_widgets()
        #self.bind("<<game/turn>>", self.controller.sub_controller.turn)
        #self.bind("<<game/end>>", self.controller.end)
        #self.bind("<<game/error>>", self.controller.error)
        self.master.network_events['game/turn'] = self.controller.sub_controller.turn
        self.master.network_events['game/end'] = self.controller.end
        self.master.network_events['game/error'] = self.controller.error
        self.master.out_queue.put({'message_type': 'game/gamestate', 'args' :{} })

    def _create_widgets(self, chat):
        self.heading = tk.Label(self, text="Tic Tac Toe Kojote", font=self.master.title_font)
        self.player = []
        self.player.append(player(self, 1))
        self.player.append(player(self, 2))
        self.gamefield = gamefield(self)
        self.chat = Chat(self, self.master, chat)
        self.close = tk.Button(self, text="close")

    def _display_widgets(self):
        self.columnconfigure([1,3], weight=1)
        self.rowconfigure(2, weight=1)

        self.heading.grid(row=0, column=0, columnspan=3)
        self.player[0].grid(row=1, column=0)
        self.player[1].grid(row=1, column=2)
        self.gamefield.grid(sticky=tk.N+tk.S+tk.E+tk.W, row=2, column=1)
        self.chat.grid(sticky=tk.N+tk.S+tk.E+tk.W, row=1, column=3, rowspan=3)
        self.close.grid(row=3, column=2)

    def on_destroy(self):
        del self.master.network_events['game/turn']
        del self.master.network_events['game/end']
        del self.master.network_events['game/error']