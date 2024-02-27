import tkinter as tk

from .base_frame import base_frame
from .customLobby import CustomLobby
from .single import Singleplayer
from .multi import Multiplayer
from .profile import Profile
from .credits import Credits

class Menu(base_frame):
    def __init__(self, master, *args):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()
        self.address_toogle = False

    def _create_widgets(self):
        self.lblTitle = tk.Label(self, text='TicTacToe-Kojote', font=self.master.title_font)
        self.btnSingle = tk.Button(self, text='Singleplayer', command=lambda *args: self.master.show(Singleplayer))
        self.btnMulti = tk.Button(self, text='Multiplayer', command=lambda*args : self.master.show(Multiplayer))
        self.btnCustom = tk.Button(self, text='Custom Game', command=lambda *args: self.master.show(CustomLobby))
        self.btnProfile = tk.Button(self, text='Profile', command=lambda *args: self.master.show(Profile))
        self.btnCredits = tk.Button(self, text='Credits', command=lambda *args: self.master.show(Credits))
        self.btnExit = tk.Button(self, text='Exit', command=lambda: self.master.destroy())

    def _display_widgets(self):
        self.columnconfigure([0, 6], weight=1)
        self.columnconfigure([1, 5], weight=2)
        self.columnconfigure([2, 4], weight=4)
        self.columnconfigure([3], weight=2)
        self.rowconfigure([0, 11], weight=1)
        self.rowconfigure([2], weight=2)
        self.rowconfigure([4, 6, 10, 12], weight=4)
        self.rowconfigure([3, 5, 7, 11, 13], weight=2)
        # display the buttons created in the _create_widgets method
        self.lblTitle.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=2, columnspan=3)
        self.btnSingle.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=4, columnspan=3)
        self.btnMulti.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=6, columnspan=3)
        self.btnProfile.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=10, columnspan=3)
        self.btnCredits.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=12, columnspan=3)
        self.btnExit.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=5, row=1)

        if(self.master.devOptions):
            self.rowconfigure([8], weight=4)
            self.rowconfigure([9], weight=2)
            self.btnCustom.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=8, columnspan=3)