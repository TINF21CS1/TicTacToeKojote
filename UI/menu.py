import tkinter as tk

from .base_frame import base_frame
from .field_frame import Field
from .lobby import Lobby

class Menu(base_frame):
    def __init__(self, master, *args):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()
        self.address_toogle = False

    def _create_widgets(self):
        
        self.btnField = tk.Button(self, width=20, height=5, text='Play / Start Lobby', command=self._start)
        self.btnMulti = tk.Button(self, width=20, height=5, text='Connect to Lobby', command=lambda: self._toogle_address(state=True))
        self.btnStats = tk.Button(self, width=20, height=5, text='Statistics')#, command=lambda: self.master.show(Statistics))
        self.btnExit = tk.Button(self, width=20, height=5, text='Exit', command=lambda: self.master.destroy())

        self.lblAddr = tk.Label(self, text="Address")
        self.inputLobby =  tk.Entry(self)
        self.btnConnect = tk.Button(self, text="Connect", command=self._start)
        

    def _display_widgets(self):

        self.columnconfigure([0,10], weight=1)
        # display the buttons created in the _create_widgets method
        self.btnField.grid(sticky=tk.E+tk.W, column=3, row=0, columnspan=5)
        self.btnMulti.grid(sticky=tk.E+tk.W, column=3, row=1, columnspan=5)
        self.btnStats.grid(sticky=tk.E+tk.W, column=3, row=3, columnspan=5)
        self.btnExit.grid(sticky=tk.E+tk.W, column=3, row=4, columnspan=5)

    def _toogle_address(self, state=None):
        if state == None:
            state = not self.address_toogle
        if state != self.address_toogle:
            if state:
                self.lblAddr.grid(sticky=tk.E+tk.W, column=4, row=2)
                self.inputLobby.grid(sticky=tk.E+tk.W, column=5, row=2)
                self.btnConnect.grid(sticky=tk.E+tk.W, column=6, row=2)
            else:
                self.lblAddr.grid_forget()
                self.inputLobby.grid_forget()
                self.btnConnect.grid_forget()
            self.address_toogle = state

    def _start(self):
        if((address:=self.inputLobby.get())==""):
            self.master.start_server()
            self.master.show(Lobby, "localhost")
        else:
            self.master.show(Lobby, address)