#import tkinter as tk
from .lib import tttk_tk as tk
from threading import Thread
from queue import Queue
from sys import exit
from .base_frame import base_frame
from .field_frame import Field
from .profile import Profile, NewProfile
from Client.ui_client import client_thread
from .field_frame import player_type
from Server.main import server_thread
from AI.ai_context import AIContext
from AI.ai_strategy import WeakAIStrategy, AdvancedAIStrategy
from .autodiscovery import discover_games
from .chat import Chat
from .messages import messages
from .gamefield import input_methods
from .statistics import Statistics

class Join(base_frame):
    """
    Class for the join screen. This screen is used to join a lobby and to display the players in the lobby.
    """
    def __init__(self, master, *args, opponent=player_type.unknown, local_players, quiet=False, **kwargs):
        super().__init__(master)
        self.quiet = quiet
        self._create_widgets(opponent)
        if(not quiet):
            self._display_widgets()
        self.playerlist = []
        self.local_players = local_players
        self.ai_players = []
        self.master.network_events['lobby/status'] = self._update_lobby
        self.master.network_events['game/start'] = self._start_game
        self.master.network_events['lobby/kick'] = self._lobby_kick
        self.master.network_events['lobby/connect_error'] = lambda *args: self._connect_error() #error is thrown when the server is not reachable anymore
        self.bind('<Destroy>', lambda *args: self.on_destroy())
        self.ready = False
        if opponent not in [player_type.unknown, player_type.local]:
            server_thread(self.master.players[self.master.player])
        if opponent in [player_type.ai_strong, player_type.ai_weak]:
            ai_context = AIContext(AdvancedAIStrategy() if opponent == player_type.ai_strong else WeakAIStrategy())
            self.ai_players.append(ai_context.get_uuid())
            self.master.ai = ai_context.run_strategy()

    def _create_widgets(self, opponent):
        title = 'Waiting for players to join' if opponent in [player_type.network, player_type.unknown] else 'Play local game against AI' if opponent in [player_type.ai_weak, player_type.ai_strong] else 'Play local game against a friend'
        self.lblTitle = tk.Label(self, text=title, font=self.master.title_font)
        self.btnRdy = tk.Button(self, text='Start', command=lambda *args: list(self.master.out_queue.values())[0].put({'message_type': 'lobby/ready', 'args' : {'ready': not self.ready}}))
        self.btnExit = tk.Button(self, text='Menu', command=lambda *args: self._menu())
        self.chat = Chat(self, self.master)
        self.btnStatistics = tk.Button(self, text='Statistics', command=lambda *args: self._show_statistics())

    def _display_widgets(self):
        self.columnconfigure([0, 6], weight=1)
        self.columnconfigure([1, 5], weight=2)
        self.columnconfigure([2, 4], weight=4)
        self.columnconfigure([3], weight=2)
        self.rowconfigure([0, 11], weight=1)
        self.rowconfigure([2], weight=2)
        self.rowconfigure([4, 6, 8, 10], weight=4)
        self.rowconfigure([3, 5, 7, 9, 11], weight=2)
        self.grid_configure()
        # display the buttons created in the _create_widgets method
        self.lblTitle.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=2, columnspan=3)
        self.btnRdy.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=10)
        self.chat.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=4, row=4, columnspan=2, rowspan=7)
        self.btnExit.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=5, row=1)
        self.btnStatistics.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=5, row=2)

    def _connect_error(self):
        self.master.show_menu()
        msg = messages(type='info', message=f'Connection to the server was lost!')
        msg.display()

    def _menu(self):
        list(self.master.out_queue.values())[0].put({'message_type': 'server/terminate', 'args' :{} })
        self.master.show_menu()

    def _update_lobby(self, queue):
        if(len(self.playerlist) > 0):
            for player in self.playerlist:
                for object in player:
                    object.grid_forget()
                    object.destroy()
        self.playerlist = []
        for player in queue['player']:
            rdy = '\u2611' if player.ready else ''
            buffer = []
            buffer.append(tk.Label(self, text=rdy + ' ' + player.display_name))
            if(player.uuid not in (self.local_players + self.ai_players)):
                buffer.append(tk.Button(self, text='Kick', command=lambda uuid=player.uuid, *args: list(self.master.out_queue.values())[0].put({'message_type': 'lobby/kick', 'args' : {'player_to_kick': uuid}})))
            self.playerlist.append(buffer)
            if(str(player.uuid) == str(self.master.players[self.master.player].uuid)):
                self.ready = player.ready
                if(player.ready):
                    self.btnRdy.config(text="not Ready")
                else:
                    self.btnRdy.config(text="Ready")
        if(not self.quiet):
            for i, player in enumerate(self.playerlist):
                for j, object in enumerate(player):
                    object.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2+j, row=4+i)
        

    def _start_game(self, queue):
        self.master.show(Field, self.chat.txtChat.get("1.0", tk.END+"-1c")+"Game starting\n", **queue, **{str(p): input_methods.mouse for p in self.local_players})

    def on_destroy(self):
        del self.master.network_events['lobby/status']
        del self.master.network_events['game/start']
        del self.master.network_events['lobby/kick']
        del self.master.network_events['lobby/connect_error']

    def _lobby_kick(self, queue):
        self._menu()
        msg = messages(type='info', message=f'You have been kicked from the lobby by the host')
        msg.display()

    def _show_statistics(self):
        self.master.cache_current_frame()
        self.master.show(Statistics, return_to=Join)

class LocalProfileSelection(base_frame):
    """
    Class for the local profile selection screen. This screen is used to select the local profiles for the game.
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self.lblTitle = tk.Label(self, text='Select your profiles', font=self.master.title_font)
        self.lblPlayer1 = tk.Label(self, text='Player 1')
        self.lblPlayer2 = tk.Label(self, text='Player 2')
        self.varPlayer1 = tk.StringVar(self, value='Select')
        self.varPlayer2 = tk.StringVar(self, value='Select')
        self.varPlayer1.trace_add('write', lambda *args: self._dropdown_changed(1))
        self.varPlayer2.trace_add('write', lambda *args: self._dropdown_changed(2))
        self.drpPlayer1 = tk.OptionMenu(self, self.varPlayer1, *[o.display_name for o in self.master.players])
        self.drpPlayer2 = tk.OptionMenu(self, self.varPlayer2, *[o.display_name for o in self.master.players])
        self.lblColor1 = tk.Label(self)
        self.lblColor2 = tk.Label(self)
        self.btnnew = tk.Button(self, text='New Profile', command=lambda *args: self.master.show(NewProfile, return_to=LocalProfileSelection))
        self.btnStart = tk.Button(self, text='Start', command=lambda *args: self._start_game())
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
        self.lblTitle.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=2, columnspan=3)
        self.lblPlayer1.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=4)
        self.lblPlayer2.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=6)
        self.drpPlayer1.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=3, row=4, columnspan=2)
        self.drpPlayer2.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=3, row=6, columnspan=2)
        self.lblColor1.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=5, row=4)
        self.lblColor2.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=5, row=6)
        self.btnnew.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=8)
        self.btnStart.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=4, row=8, columnspan=2)
        self.btnMenu.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=5, row=1)

    def _dropdown_changed(self, player):
        if(player == 1):
            for profile in self.master.players:
                if(profile.display_name == self.varPlayer1.get()):
                    self.lblColor1.config(bg=profile.color_str)
        else:
            for profile in self.master.players:
                if(profile.display_name == self.varPlayer2.get()):
                    self.lblColor2.config(bg=profile.color_str)

    def _start_game(self):
        if(self.varPlayer1.get() == 'Select' or self.varPlayer2.get() == 'Select' or self.varPlayer1.get() == self.varPlayer2.get()):
            msg = messages(type='info', message='Please select two different players')
            msg.display()
            return
        for player in self.master.players:
            if player.display_name == self.varPlayer1.get():
                player1 = player
            if player.display_name == self.varPlayer2.get():
                player2 = player
        self.master.out_queue = {player1.uuid: Queue(), player2.uuid: Queue()}
        server_thread(player1)
        self.master.network_thread = client_thread(self.master, in_queue=self.master.out_queue[player1.uuid], out_queue=self.master.in_queue, player=player1, ip='localhost')
        client_thread(self.master.dummy, in_queue=self.master.out_queue[player2.uuid], out_queue=Queue(), player=player2, ip='localhost')
        self.master.out_queue[player1.uuid].put({'message_type': 'lobby/ready', 'args' : {'ready': True}})
        self.master.out_queue[player2.uuid].put({'message_type': 'lobby/ready', 'args' : {'ready': True}})
        self.master.show(Join, display=False, opponent=player_type.local, local_players=[player1.uuid, player2.uuid],quiet=True)


def reload(tkinter_obj: tk.Widget, queue: Queue):
    for i in range(10):
        servers = discover_games(i+1)
        queue.put(servers)
        try:
            tkinter_obj.event_generate('<<lobby/reload>>')
        except tk.TclError:
            pass
    try:
        tkinter_obj.event_generate('<<thread/exit>>')
    except tk.TclError:
        pass
    exit()

class Lobby_Overview(tk.Container):
    """
    Class for the lobby overview. This screen is part of the multiplayer screen and used to display the available lobbies and to join them.
    """
    def __init__(self, master):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()
        self.queue = Queue()
        self.thread = False
        self.servers = {}
        self.master.master.network_events['lobby/connect'] = self._lobby_connect
        self.master.master.network_events['lobby/connect_error'] = self._connect_error
        self.bind('<<lobby/reload>>', lambda *args: self._finish_reload())
        self.bind('<<thread/exit>>', lambda *args: self._thread_reset())
        self.bind('<Destroy>', lambda *args: self.on_destroy())
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
        self.master.master.bind('<Return>', lambda *args: self._enter())

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
        self.etrAddress.focus_set()

    def _enter(self):
        if(self.focus_get() == self.etrAddress.widget):
            self._connect()

    def _connect(self, ip):
        root = self.master.master
        root.out_queue = {root.players[root.player].uuid: Queue()}
        root.network_client = client_thread(root, in_queue=list(root.out_queue.values())[0], out_queue=root.in_queue, player=root.players[root.player], ip=ip)
        self.etrAddress.config(state=tk.DISABLED)
        self.btnConnect.config(text="Connecting...", state=tk.DISABLED)

    def _connect_error(self, queue):
        msg = messages(type='info', message=f'Could not connect to the server "{self.etrAddress.get()}"')
        self.etrAddress.config(state=tk.NORMAL)
        self.btnConnect.config(text="Connect", state=tk.NORMAL)
        msg.display()

    def _lobby_connect(self, queue):
        root = self.master.master
        root.show(Join, local_players=[root.players[root.player].uuid])

    def on_destroy(self):
        del self.master.master.network_events['lobby/connect']
        del self.master.master.network_events['lobby/connect_error']

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
    """
    Class for the multiplayer screen. This screen is used to select the multiplayer mode and to create or join lobbies.
    It houses the lobby overview.
    """
    def __new__(cls, master, *args, **kwargs):
        if(len(master.players) == 0 or master.player == None):
            return Profile(master, *args, return_to=Multiplayer, **kwargs)
        return super().__new__(cls)

    def __init__(self, master, *args):
        super().__init__(master)
        self.master.out_queue = {}
        self._create_widgets()
        self._display_widgets()


    def _create_widgets(self):
        self.lblTitle = tk.Label(self, text='Multiplayer', font=self.master.title_font)
        self.btnNew = tk.Button(self, text='Create a new online game', command=lambda *args: self._create_online_game())
        self.btnLocal = tk.Button(self, text='Create local Game', command=lambda*args : self._create_local_game())
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
        self.master.out_queue = {self.master.players[self.master.player].uuid: Queue()}
        self.master.network_thread = client_thread(self.master, in_queue=list(self.master.out_queue.values())[0], out_queue=self.master.in_queue, player=self.master.players[self.master.player], ip='localhost')
        self.master.show(Join, opponent=player_type.network, local_players=[self.master.players[self.master.player].uuid])

    def _create_local_game(self):
        self.master.show(LocalProfileSelection, opponent=player_type.local)