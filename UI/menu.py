import tkinter as tk

from .base_frame import base_frame
from .field_frame import Field
from .lobby import Lobby

class Menu(base_frame):
    def __init__(self, master):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        
        self.btnField = tk.Button(self, width=20, height=5, text='Play', command=lambda: self.master.show(Field))
        self.btnMulti = tk.Button(self, width=20, height=5, text='Multiplayer', command=lambda: self.master.show(Lobby))
        self.btnStats = tk.Button(self, width=20, height=5, text='Statistics')#, command=lambda: self.master.show(Statistics))
        self.btnExit = tk.Button(self, width=20, height=5, text='Exit', command=lambda: self.master.destroy())
        

    def _display_widgets(self):

        # display the buttons created in the _create_widgets method
        self.btnField.pack(fill=tk.Y, expand=True)
        self.btnMulti.pack(fill=tk.Y, expand=True)
        self.btnStats.pack(fill=tk.Y, expand=True)
        self.btnExit.pack(fill=tk.Y, expand=True)