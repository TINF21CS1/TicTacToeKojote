#import tkinter as tk
from .lib import tttk_tk as tk
from uuid import UUID

from .base_frame import base_frame
from .field_frame import Field
from .profile import Profile
from Client.ui_client import client_thread
from .field_frame import player_type
from Server.main import server_thread

class Join(base_frame):
    def __init__(self, master, *args, opponent=player_type.unknown, **kwargs):
        super().__init__(master)
        self._create_widgets(opponent)
        self._display_widgets()
        self.playerlist = []
        #self.bind('<<lobby/status>>', self._update_lobby)
        #self.bind('<<game/start>>', self._start_game)
        self.master.network_events['lobby/status'] = self._update_lobby
        self.master.network_events['game/start'] = self._start_game
        self.bind('Destroy', lambda *args: self.on_destroy())
        self.ready = False
        if opponent != player_type.unknown:
            server_thread(self.master.player)

    def _create_widgets(self, opponent):
        title = 'Waiting for players to join' if opponent in [player_type.network, player_type.unknown] else 'Play local game against AI' if opponent == player_type.ai else 'Play local game against a friend'
        self.lblTitle = tk.Label(self, text=title, font=self.master.title_font)
        self.btnRdy = tk.Button(self, text='Start', command=lambda *args: self.master.out_queue.put({'message_type': 'lobby/ready', 'args' : {'ready': not self.ready}}))
        if opponent == player_type.local:
            self.btnRdy2 = tk.Button(self, text='Start', command=lambda *args: self.master.out_queue.put({'message_type': 'lobby/ready', 'args' : {'ready': True}}))
        self.btnExit = tk.Button(self, text='Menu', command=lambda: self.master.show_menu())

    def _display_widgets(self,):
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
        self.btnRdy.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=4, row=10)
        if hasattr(self, 'btnRdy2'):
            self.btnRdy2.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=10)
        self.btnExit.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=5, row=1)

    def _update_lobby(self):
        queue = self.master.in_queue.get()
        self.playerlist = []
        for player in queue['player']:
            self.playerlist.append([tk.Label(self, text=player.display_name),
                                    tk.Button(self, text='Kick', command=lambda uuid=player.uuid, *args: self.master.out_queue.put({'message_type': 'lobby/kick', 'args' : {'player_to_kick_index': uuid}}))])
            if(str(player.uuid) == str(self.master.player.uuid)):
                self.ready = player.ready
                if(player.ready):
                    self.btnRdy.config(text="Ready")
                else:
                    self.btnRdy.config(text="Start")
        for i, player in enumerate(self.playerlist):
            player[0].grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=4+i, columnspan=2)
            player[1].grid(sticky=tk.E+tk.W+tk.N+tk.S, column=4, row=4+i)
        

    def _start_game(self):
        queue = self.master.in_queue.get()
        print(queue)
        self.master.show(Field, **queue)

    def on_destroy(self):
        del self.master.network_events['lobby/status']
        del self.master.network_events['game/start']

class Lobby_Overview(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self.lblHeading = tk.Label(self, text="Join public lobbies", font=self.master.master.title_font)

        self.btnManual = tk.Button(self, text="Join by address", command=lambda *args: self.manually())
        self.etrAddress = tk.Entry(self)
        self.btnConnect = tk.Button(self, text="Connect", command=lambda *args: self._connect())

    def _display_widgets(self):
        self.columnconfigure([0, 2, 4], weight=1)
        self.columnconfigure([1, 3], weight=5)
        self.rowconfigure([0, 4], weight=2)
        self.rowconfigure([1, 3], weight=1)
        self.rowconfigure([2], weight=40)
        self.lblHeading.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=1, row=0, columnspan=3)
        self.btnManual.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=1, row=4, columnspan=3)

    def manually(self):
        self.btnManual.grid_forget()
        self.etrAddress.grid(column=1, row=10, sticky=tk.E+tk.W+tk.N+tk.S)
        self.btnConnect.grid(column=3, row=10, sticky=tk.E+tk.W+tk.N+tk.S)

    def _connect(self):
        root = self.master.master
        root.network_client = client_thread(root, in_queue=root.out_queue, out_queue=root.in_queue, player=root.player, ip=self.etrAddress.get())
        root.show(Join)

class Multiplayer(base_frame):
    def __new__(cls, master, *args, **kwargs):
        if(master.player == None):
            return Profile(master, *args, return_to=Multiplayer, **kwargs)
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, master, *args):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()
        self.address_toogle = False

    def _create_widgets(self):
        self.lblTitle = tk.Label(self, text='Multiplayer', font=self.master.title_font)
        self.btnNew = tk.Button(self, text='Create a new online game', command=lambda *args: self._create_online_game())
        self.btnLocal = tk.Button(self, text='Create local Game', command=lambda*args : self.master.show(Join, opponent=player_type.local))
        self.lobbyOverview = Lobby_Overview(self)
        self.btnMenu = tk.Button(self, text='Menu', command=lambda: self.master.show_menu())

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
        self.btnNew.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=4, rowspan=3)
        self.btnLocal.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=8, rowspan=3)
        self.lobbyOverview.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=4, row=4, rowspan=7)
        self.btnMenu.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=5, row=1)

    def _create_online_game(self):
        self.master.network_thread = client_thread(self.master, in_queue=self.master.out_queue, out_queue=self.master.in_queue, player=self.master.player, ip='localhost')
        self.master.show(Join, opponent=player_type.network)