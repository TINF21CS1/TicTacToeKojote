#import tkinter as tk
from .lib import tttk_tk as tk
from threading import Thread
from queue import Queue
from sys import exit

from .base_frame import base_frame
from .field_frame import Field
from .profile import Profile
from Client.ui_client import client_thread
from .field_frame import player_type
from Server.main import server_thread
from AI.ai_context import AIContext
from AI.ai_strategy import WeakAIStrategy, AdvancedAIStrategy
from .autodiscovery import discover_games

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
        if opponent in [player_type.ai_strong, player_type.ai_weak]:
            ai_context = AIContext(AdvancedAIStrategy() if opponent == player_type.ai_strong else WeakAIStrategy())
            self.master.ai = ai_context.run_strategy()

    def _create_widgets(self, opponent):
        title = 'Waiting for players to join' if opponent in [player_type.network, player_type.unknown] else 'Play local game against AI' if opponent in [player_type.ai_weak, player_type.ai_strong] else 'Play local game against a friend'
        self.lblTitle = tk.Label(self, text=title, font=self.master.title_font)
        self.btnRdy = tk.Button(self, text='Start', command=lambda *args: self.master.out_queue.put({'message_type': 'lobby/ready', 'args' : {'ready': not self.ready}}))
        if opponent == player_type.local:
            self.btnRdy2 = tk.Button(self, text='Start', command=lambda *args: self.master.out_queue.put({'message_type': 'lobby/ready', 'args' : {'ready': True}}))
        self.btnExit = tk.Button(self, text='Menu', command=lambda: self._menu())

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

    def _update_lobby(self, queue):
        self.playerlist = []
        for player in queue['player']:
            self.playerlist.append([tk.Label(self, text=player.display_name),
                                    tk.Button(self, text='Kick', command=lambda uuid=player.uuid, *args: self.master.out_queue.put({'message_type': 'lobby/kick', 'args' : {'player_to_kick': uuid}}))])
            if(str(player.uuid) == str(self.master.player.uuid)):
                self.ready = player.ready
                if(player.ready):
                    self.btnRdy.config(text="Ready")
                else:
                    self.btnRdy.config(text="Start")
        for i, player in enumerate(self.playerlist):
            player[0].grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=4+i, columnspan=2)
            player[1].grid(sticky=tk.E+tk.W+tk.N+tk.S, column=4, row=4+i)
        

    def _start_game(self, queue):
        print(queue)
        self.master.show(Field, **queue)

    def on_destroy(self):
        del self.master.network_events['lobby/status']
        del self.master.network_events['game/start']

    def _menu(self):
        self.master.out_queue.put({'message_type': 'server/terminate', 'args': {}})
        self.master.show_menu()


def reload(tkinter_obj: tk.Widget, queue: Queue):
    print('hiu')
    for i in range(10):
        servers = discover_games(i+1)
        queue.put(servers)
        tkinter_obj.event_generate('<<lobby/reload>>')
        print(servers)
    tkinter_obj.event_generate('<<thread/exit>>')
    print('dead')
    exit()

class Lobby_Overview(tk.Container):
    def __init__(self, master):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()
        self.queue = Queue()
        self.thread = False
        self.servers = {}
        self.bind('<<lobby/reload>>', lambda *args: self._finish_reload())
        self.bind('<<thread/exit>>', lambda *args: self._thread_reset())
        self._start_reload()

    def _create_widgets(self):
        self.frame = tk.Frame(self)
        self.innerframe = self.frame.widget
        self.lblHeading = tk.Label(self.innerframe, text="Join public lobbies", font=self.master.master.title_font)
        self.btnReload = tk.Button(self.innerframe, text="\u21BB", command=lambda *args: self._start_reload(), border=0)
        self.wrapper = tk.Container(self.innerframe)
        self.btnManual = tk.Button(self.innerframe, text="Join by address", command=lambda *args: self._manually())
        self.etrAddress = tk.Entry(self.innerframe)
        self.btnConnect = tk.Button(self.innerframe, text="Connect", command=lambda ip=self.etrAddress.get(), *args: self._connect(ip))

    def _display_widgets(self):
        self.frame.pack(expand=True, fill=tk.BOTH)
        self.innerframe.columnconfigure([0, 2, 4, 5], weight=1)
        self.innerframe.columnconfigure([1, 3], weight=5)
        self.innerframe.rowconfigure([0, 4], weight=2)
        self.innerframe.rowconfigure([1, 3], weight=1)
        self.innerframe.rowconfigure([2], weight=40)
        self.lblHeading.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=1, row=0, columnspan=3)
        self.btnReload.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=4, row=0)
        self.btnManual.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=1, row=4, columnspan=4)

    def _manually(self):
        self.btnManual.grid_forget()
        self.etrAddress.grid(column=1, row=10, sticky=tk.E+tk.W+tk.N+tk.S)
        self.btnConnect.grid(column=3, row=10, columnspan=2, sticky=tk.E+tk.W+tk.N+tk.S)

    def _connect(self, ip):
        root = self.master.master
        root.network_client = client_thread(root, in_queue=root.out_queue, out_queue=root.in_queue, player=root.player, ip=ip)
        root.show(Join)

    def _start_reload(self):
        if(self.thread):
            return
        Thread(target=reload, args=(self, self.queue), daemon=True).start()
        self.thread = True

    def _finish_reload(self):
        servers = self.queue.get()
        if(servers == self.servers):
            return
        self.servers = servers
        self.wrapper.destroy()
        self.wrapper = tk.Container(self.innerframe)
        self.wrapper.columnconfigure([0], weight=1)
        self.wrapper.columnconfigure([1], weight=0)
        for i, (server, ip) in enumerate(self.servers.items()):
            tk.Label(self.wrapper, text=server).grid(column=0, row=i, sticky=tk.W+tk.N+tk.S)
            tk.Button(self.wrapper, text="Join", command=lambda ip=ip, *args: self._connect(ip)).grid(column=1, row=i, sticky=tk.E+tk.W+tk.N+tk.S)
        self.wrapper.grid(column=1, row=2, columnspan=4, sticky=tk.E+tk.W+tk.N+tk.S)

    def _thread_reset(self):
        self.thread = False

class Multiplayer(base_frame):
    def __new__(cls, master, *args, **kwargs):
        if(master.player == None):
            return Profile(master, *args, return_to=Multiplayer, **kwargs)
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, master, *args):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()


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