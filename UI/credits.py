#import tkinter as tk
from .lib import tttk_tk as tk

from .base_frame import base_frame

class Credits(base_frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()
        self.address_toogle = False

    def _create_widgets(self):
        self.lblTitle = tk.Label(self, text='TicTacToe-Kojote', font=self.master.title_font)
        self.lblBy = tk.Label(self, text='created by', font=self.master.title_font)
        self.lblNames = tk.Label(self, text='Andrey, Bengt, Hauke, Julian, Timm', font=self.master.title_font)
        self.btnExit = tk.Button(self, text='Menu', command=lambda *args: self.master.show_menu())

        self.lblBy.bind("<Triple-Button-1>", lambda e: self._devOptions())

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
        self.lblBy.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=4, columnspan=3)
        self.lblNames.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=6, columnspan=3)
        self.btnExit.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=5, row=1)

    def _devOptions(self):
        self.master.devOptions = True
        self.master.show_menu()