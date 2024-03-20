#import tkinter as tk
from .lib import tttk_tk as tk
from queue import Queue

from .base_frame import base_frame
from .multi import Join
from .field_frame import player_type
from Client.ui_client import client_thread
from .profile import Profile

class Singleplayer(base_frame):
    """
    The singleplayer menu. This screen is used to choose the opponent for a singleplayer game.
    """
    def __new__(cls, master, *args, **kwargs):
        if(len(master.players) == 0 or master.player == None):
            return Profile(master, *args, return_to=Singleplayer, **kwargs)
        return super().__new__(cls)
    
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.master.out_queue = {}
        self._create_widgets()
        self._display_widgets()
        self.address_toogle = False

    def _create_widgets(self):
        self.lblTitle = tk.Label(self, text='Choose your opponent', font=self.master.title_font)
        self.btnStrong = tk.Button(self, text='Strong AI', command=lambda *args: self.join_ai(True))
        self.btnWeak = tk.Button(self, text='Weak AI', command=lambda *args: self.join_ai(False))
        self.btnExit = tk.Button(self, text='Menu', command=lambda *args: self.master.show_menu())

    def _display_widgets(self):
        self.columnconfigure([0, 6], weight=1)
        self.columnconfigure([1, 5], weight=2)
        self.columnconfigure([2, 4], weight=4)
        self.columnconfigure([3], weight=2)
        self.rowconfigure([0, 11], weight=1)
        self.rowconfigure([2], weight=2)
        self.rowconfigure([4, 6, 8, 10], weight=4)
        self.rowconfigure([3, 5, 7, 9, 11], weight=2)
        # display the buttons created in the _create_widgets method
        self.lblTitle.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=2, columnspan=3)
        self.btnStrong.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=4, rowspan=7)
        self.btnWeak.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=4, row=4, rowspan=7)
        self.btnExit.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=5, row=1)

    def join_ai(self, strong: bool):
        self.master.out_queue = {self.master.players[self.master.player].uuid: Queue()}
        test = list(self.master.out_queue.values())[0]
        self.master.network_thread = client_thread(self.master, in_queue=list(self.master.out_queue.values())[0], out_queue=self.master.in_queue, player=self.master.players[self.master.player], ip='localhost')
        if strong:
            ai = player_type.ai_strong
        else:
            ai = player_type.ai_weak
        self.master.show(Join, opponent=ai, local_players=[self.master.players[self.master.player].uuid])
