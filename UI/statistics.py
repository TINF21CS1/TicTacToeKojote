#import tkinter as tk
from .lib import tttk_tk as tk

from .base_frame import base_frame
from Server.player import Player

class Statistics_data(tk.Container):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)

    def _update_statistics(self, queue):
        heading = {Player('Player', 0): {'wins': 'Wins', 'losses': 'Losses', 'draws': 'Draws', 'moves': 'Moves', 'emojis': 'Emojis'}}
        for i, (player, values) in enumerate((heading | queue['statistics']).items()):
            tk.Label(self, text=player.display_name).grid(sticky=tk.E+tk.W+tk.N+tk.S, column=0, row=i)
            for j, (headline, value) in enumerate(values.items()):
                tk.Label(self, text=value).grid(sticky=tk.E+tk.W+tk.N+tk.S, column=j+1, row=i)

class Statistics(base_frame):
    def __init__(self, master, return_to, *args, **kwargs):
        super().__init__(master)
        self.return_to = return_to
        self._create_widgets()
        self._display_widgets()
        self.master.network_events['statistics/statistics'] = self.data._update_statistics
        self.bind('<Destroy>', lambda *args: self._on_destroy())
        list(self.master.out_queue.values())[0].put({'message_type': 'statistics/statistics', 'args': {}})

    def _create_widgets(self):
        self.lblTitle = tk.Label(self, text='TicTacToe-Kojote', font=self.master.title_font)
        self.btnBack = tk.Button(self, text='Back', command=lambda *args: self._back())
        self.data = Statistics_data(self)

    def _back(self):
        self.master.show(self.return_to)
        self.master.remove_cached_frame(self.return_to)

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
        self.btnBack.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=5, row=1)
        self.data.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=4, columnspan=3)

    def _on_destroy(self):
        del self.master.network_events['statistics/statistics']