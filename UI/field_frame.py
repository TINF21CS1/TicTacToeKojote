#import tkinter as tk
from .lib import tttk_tk as tk
from enum import Enum, auto

from .base_frame import base_frame
from .gamefield import gamefield, gamefield_controller
from .endscreen import EndScreen
from .messages import messages
from .chat import Chat
from .lib.colors import color
from .statistics import Statistics

class player_type(Enum):
    """
    Enum for the different player types
    """
    local = auto()
    ai_weak = auto()
    ai_strong = auto()
    network = auto()
    unknown = auto()

class player(tk.Container):
    """
    Class for the player labels in the gamefield
    """
    def __init__(self, master, number, uuid=None):
        super().__init__(master)
        self.uuid = uuid
        self._create_widgets(number)
        self._display_widgets()

    def _create_widgets(self, number):
        self.frame = tk.Frame(self)
        self.heading = tk.Label(self.frame.widget, text=f'Player {number}', font=self.master.master.title_font, border=0, margin=0)
        self.name = tk.Label(self.frame.widget, text=f'Player {number}', border=0, margin=0)
        self.symbol = tk.Label(self.frame.widget, text="unknown", border=0, margin=0)
            
    def highlight(self, highlight=True):
        obj = [self.heading, self.name, self.symbol]
        if(highlight):
            self.frame.config(bg=color.green)
            for o in obj:
                o.config(bg=color.green)
                o.config(fg=color.green.complement)
        else:
            self.frame.config(bg=color.white)
            for o in obj:
                o.config(bg=color.white)
                o.config(fg=color.white.complement)

    def set(self, name, symbol, uuid):
        self.name.config(text=name)
        self.uuid = uuid
        match symbol:
            case 0:
                self.symbol.config(text="O")
            case 1:
                self.symbol.config(text="X")

    def _display_widgets(self):
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.heading.grid(row=0, column=0, columnspan=2)
        self.name.grid(row=1, column=0)
        self.symbol.grid(row=1, column=1)

class game_menu(base_frame):
    """
    The game menu can be accessed from the gamefield. It allows the user to return to the main menu, the statistics or to exit the game.
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self.lblTitle = tk.Label(self, text='TicTacToe-Kojote', font=self.master.title_font)
        self.btnBack = tk.Button(self, text='Continue', command=lambda *args: self.master.show(Field))
        self.btnSatistics = tk.Button(self, text='Statistics', command=lambda *args: self.master.show(Statistics, return_to=game_menu))
        self.btnMenu = tk.Button(self, text='Main menu', command=lambda *args: self._menu())
        self.btnExit = tk.Button(self, text='Exit', command=lambda: self.master.destroy())

    def _display_widgets(self):
        self.columnconfigure([0, 6], weight=1)
        self.columnconfigure([1, 5], weight=2)
        self.columnconfigure([2, 4], weight=4)
        self.columnconfigure([3], weight=2)
        self.rowconfigure([0, 11], weight=1)
        self.rowconfigure([2], weight=2)
        self.rowconfigure([4, 6, 8, 10, 12], weight=4)
        self.rowconfigure([3, 5, 7, 11, 13], weight=2)
        # display the buttons created in the _create_widgets method
        self.lblTitle.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=2, columnspan=3)
        self.btnBack.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=4, columnspan=3)
        self.btnSatistics.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=6, columnspan=3)
        self.btnMenu.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=8, columnspan=3)
        self.btnExit.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=5, row=1)

    def _menu(self):
        self.master.remove_cached_frame(Field)
        list(self.master.out_queue.values())[0].put({'message_type': 'server/terminate', 'args' :{} })
        self.master.show_menu()

class field_controller():
    """
    The controller for the gamefield. It is used to control the gamefield and access the game menu.
    """
    def __init__(self, view, players, player_symbols, starting_uuid, local_mp, **kwargs):
        self.view = view
        self.local_mp = local_mp
        symbol_colors = {player_symbols[0]: players[1].color_str, player_symbols[1]: players[0].color_str}
        self.sub_controller = gamefield_controller(self.view.gamefield, starting_uuid, symbol_colors,  **kwargs)
        for player_lbl, player, symbol in zip(self.view.player, players, player_symbols):
            player_lbl.set(player.display_name, symbol, player.uuid)
        self._bind()

    def _bind(self):
        self.view.menu.config(command=lambda *args: self._menu())

    def _menu(self):
        self.view.master.cache_current_frame()
        self.view.master.show(game_menu)

    def end(self, queue, *args):
        root = self.view.master
        root.show(EndScreen, queue['win'], queue['winner'], queue['final_playfield'], local_mp=self.local_mp)

    def error(self, queue, *args):
        root = self.view.master
        msg = messages(type='move', message=queue['error_message'])
        msg.display()

    def _close(self):
        root = self.view.master
        root.out_queue.put({'message_type': 'server/terminate', 'args': {}})
        self.view.master.show_menu()

class Field(base_frame):
    """
    The field frame is used to display the gamefield and the player labels.
    """
    def __init__(self, master, chat, *args, starting_player, player1, player1_symbol, player2, player2_symbol, **kwargs):
        super().__init__(master)
        local_mp = not (len(kwargs)==1)
        self._create_widgets(chat, display_chat=not local_mp)
        self.controller = field_controller(self, [player1, player2], [player1_symbol, player2_symbol], starting_player.uuid, local_mp, **kwargs)
        self._display_widgets()
        self.master.network_events['game/turn'] = self.controller.sub_controller.turn
        self.master.network_events['game/end'] = self.controller.end
        self.master.network_events['game/error'] = self.controller.error
        self.master.out_queue[player1.uuid].put({'message_type': 'game/gamestate', 'args' :{} })
        self.bind('<Destroy>', lambda *args: self.on_destroy())
        self.master.remove_cached_frame(Field)

    def _create_widgets(self, chat, display_chat=True):
        self.heading = tk.Label(self, text="Tic Tac Toe Kojote", font=self.master.title_font)
        self.player = []
        self.player.append(player(self, 1))
        self.player.append(player(self, 2))
        self.gamefield = gamefield(self)
        if(display_chat):
            self.chat = Chat(self, self.master, chat)
        self.menu = tk.Button(self, text="Menu")

    def _display_widgets(self):
        self.columnconfigure([1], weight=1)
        self.rowconfigure(2, weight=1)

        self.heading.grid(row=0, column=0, columnspan=3)
        self.player[0].grid(row=1, column=0)
        self.player[1].grid(row=1, column=2)
        self.gamefield.grid(sticky=tk.N+tk.S+tk.E+tk.W, row=2, column=0, columnspan=3)
        if(hasattr(self, 'chat')):
            self.columnconfigure(3, weight=1)
            self.chat.grid(sticky=tk.N+tk.S+tk.E+tk.W, row=1, column=3, rowspan=3, columnspan=2)
        self.menu.grid(row=0, column=4)

    def on_destroy(self):
        del self.master.network_events['game/turn']
        del self.master.network_events['game/end']
        del self.master.network_events['game/error']