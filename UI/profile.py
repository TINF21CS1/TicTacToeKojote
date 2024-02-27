import tkinter as tk
from uuid import UUID, uuid4

from .base_frame import base_frame
from .field_frame import Field

class Player:
    def __init__(self, display_name: str, color: int):
        self.uuid: UUID = uuid4()
        self.display_name = display_name
        self.color = color
        self.ready = False

class NewProfile(base_frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()
        self.address_toogle = False
        self.next = kwargs.pop('return_to', Profile)

    def _create_widgets(self):
        self.lblTitle = tk.Label(self, text='Create profile', font=self.master.title_font)
        self.lblName = tk.Label(self, text='Name')
        self.varName = tk.StringVar(self, value=self.master.player.display_name if self.master.player != None else '')
        self.etrName = tk.Entry(self, textvariable=self.varName)
        self.btnCreate = tk.Button(self, text='Create profile', command=lambda *args: self._create())
        self.btnMenu = tk.Button(self, text='Menu', command=lambda: self.master.show_menu())

    def _display_widgets(self):
        self.columnconfigure([0, 10], weight=1)
        self.columnconfigure([1, 9], weight=2)
        self.columnconfigure([2, 8], weight=1)
        self.columnconfigure([3, 7], weight=2)
        self.columnconfigure([2, 8], weight=2)
        self.columnconfigure([5], weight=2)

        self.rowconfigure([0, 11], weight=1)
        self.rowconfigure([2], weight=2)
        self.rowconfigure([4, 6, 8, 10], weight=4)
        self.rowconfigure([3, 5, 7, 9, 11], weight=2)
        # display the buttons created in the _create_widgets method
        self.lblTitle.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=2, columnspan=7)
        self.lblName.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=4)
        self.etrName.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=4, row=4, columnspan=5)
        self.btnCreate.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=6, row=8, columnspan=3)
        self.btnMenu.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=9, row=1)

    def _create(self):
        self.master.player = Player(self.varName.get(), 0)
        self.master.show(self.next)

class Profile(base_frame):
    def __new__(cls, master, *args, **kwargs):
        if(master.player == None):
            return NewProfile(master, *args, **kwargs)
        return super().__new__(cls, *args, **kwargs)
    
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()
        self.address_toogle = False

    def _create_widgets(self):
        self.lblTitle = tk.Label(self, text='Multiplayer', font=self.master.title_font)
        self.lblName = tk.Label(self, text='Name')
        self.lblNameValue = tk.Label(self, text=self.master.player.display_name)
        self.lblUUDI = tk.Label(self, text='User ID')
        self.lblUUIDValue = tk.Label(self, text=self.master.player.uuid)
        self.btnEdit = tk.Button(self, text='Edit Profile', command=lambda *args: self.master.show(NewProfile, 'edit'))
        self.btnDelete = tk.Button(self, text='Delete profile', command=lambda*args : self.master.show(NewProfile, 'delete'))
        self.btnMenu = tk.Button(self, text='Menu', command=lambda: self.master.show_menu())

    def _display_widgets(self):
        self.columnconfigure([0, 10], weight=1)
        self.columnconfigure([1, 9], weight=2)
        self.columnconfigure([2, 8], weight=1)
        self.columnconfigure([3, 7], weight=2)
        self.columnconfigure([2, 8], weight=2)
        self.columnconfigure([5], weight=2)

        self.rowconfigure([0, 11], weight=1)
        self.rowconfigure([2], weight=2)
        self.rowconfigure([4, 6, 8, 10], weight=4)
        self.rowconfigure([3, 5, 7, 9, 11], weight=2)
        # display the buttons created in the _create_widgets method
        self.lblTitle.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=2, columnspan=7)
        self.lblName.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=4)
        self.lblNameValue.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=4, row=4, columnspan=5)
        self.lblUUDI.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=6)
        self.lblUUIDValue.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=4, row=6, columnspan=5)
        self.btnDelete.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=8, columnspan=3)
        self.btnEdit.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=6, row=8, columnspan=3)
        self.btnMenu.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=9, row=1)