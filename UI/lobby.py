import tkinter as tk
from .base_frame import base_frame
from .field_frame import Field
from .network import get_connected_player

class Lobby(base_frame):
    def __init__(self, master):
        super().__init__(master)
        self.player = list()
        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self.lblheading = tk.Label(self, width=20, height=5, bg="white", text="Lobby")
        self.btnJoin = tk.Button(self, width=20, height=5, text="Join Lobby", command=self.select_join)
        self.lblAddrHeading = tk.Label(self, text="Address")
        self.inputLobby =  tk.Entry(self)
        self.btnConnect = tk.Button(self, text="Connect", command=self.connect)
        self.btnCreate = tk.Button(self, width=20, height=5, text="Create Lobby", command=self.select_create)
        self.lblAddr = tk.Label(self, text="Connect to your local address")
        self.btnBack = tk.Button(self, text="Back", width=20, height=5, command=self.master.show_menu)

    def _display_widgets(self):
        self.lblheading.grid(column=0, row=0, columnspan=3)
        self.btnJoin.grid(column=0, row=1, columnspan=3)
        self.btnCreate.grid(column=0, row=30, columnspan=3)

        self.btnBack.grid(column=0, row=50, columnspan=3)

    def select_join(self):
        self.lblAddr.grid_forget()
        for e in self.player:
            e[0].grid_forget()
            e[1].grid_forget()
        self.player = []

        self.lblAddrHeading.grid(column=0, row=2)
        self.inputLobby.grid(column=1, row=2)
        self.btnConnect.grid(column=2, row=2)

    def select_create(self):
        self.lblAddrHeading.grid_forget()
        self.inputLobby.grid_forget()
        self.btnConnect.grid_forget()

        for e in self.player:
            e[0].grid_forget()
            e[1].grid_forget()
        self.player = []

        self.lblAddr.grid(column=0, row=31, columnspan=3)
        for e in get_connected_player():
            self.player.append([tk.Label(self, text=e), tk.Button(self, text="Start", command=lambda f=e: self.start(f))])
        self.player = self.player[0:10]
        for i, e in enumerate(self.player):
            e[0].grid(column=0, row=32+i, columnspan=2)
            e[1].grid(column=2, row=32+i)

    def connect(self):
        #do some network shit
        self.master.show(Field)

    def start(self, player):
        #do some network shit
        self.master.show(Field)