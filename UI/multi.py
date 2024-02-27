import tkinter as tk

from .base_frame import base_frame
from .field_frame import Field

class Join(base_frame):
    def __init__(self, master, *args):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()
        self.address_toogle = False

    def _create_widgets(self):
        self.lblTitle = tk.Label(self, text='Waiting for players to join', font=self.master.title_font)
        self.btnExit = tk.Button(self, text='Menu', command=lambda: self.master.show_menu())

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
        self.btnExit.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=5, row=1)

class Lobby_Overview(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self.lblHeading = tk.Label(self, text="Join public lobbies", font=self.master.master.title_font)

        self.btnManual = tk.Button(self, text="Join by address", command=lambda *args: self.manually())
        self.etrAddress = tk.Entry(self)
        self.btnConnect = tk.Button(self, text="Connect", command=lambda *args: self.master.master.show(Join))

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

class Multiplayer(base_frame):
    def __init__(self, master, *args):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()
        self.address_toogle = False

    def _create_widgets(self):
        self.lblTitle = tk.Label(self, text='Multiplayer', font=self.master.title_font)
        self.btnNew = tk.Button(self, text='Create a new online game', command=lambda *args: self.master.show(Join))
        self.btnLocal = tk.Button(self, text='Create local Game', command=lambda*args : self.master.show(Field))
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