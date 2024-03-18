#import tkinter as tk
from .lib import tttk_tk as tk
from uuid import UUID, uuid4

from .base_frame import base_frame
from .field_frame import Field
from Server.player import Player
from Client.profile_save import Profile as ProfileIO
from .messages import messages

class NewProfile(base_frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.address_toogle = False
        self.next = kwargs.pop('return_to', Profile)
        self.edit = kwargs.pop('edit', False)
        self.id = kwargs.pop('id', None)
        self._create_widgets()
        self._display_widgets()
        self.etrName.focus_set()

    def _create_widgets(self):
        task = 'Edit' if self.edit else 'Create'
        self.lblTitle = tk.Label(self, text=f'{task} profile', font=self.master.title_font)
        self.lblName = tk.Label(self, text='Name')
        self.etrName = tk.Entry(self)
        self.etrName.val = self.master.players[self.master.player].display_name if self.edit else ''
        self.btnCreate = tk.Button(self, text=f'{task} profile', command=lambda *args: self._create())
        self.btnMenu = tk.Button(self, text='Menu', command=lambda: self.master.show_menu())
        self.master.bind('<Return>', lambda *args: self._enter())

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

    def _enter(self):
        if(self.focus_get() == self.etrName.widget):
            self._create()

    def _create(self):
        if(self.etrName.val in [p.display_name for p in self.master.players]): 
            msg = messages(type='info', message='This name is already in use.\nPlease select a differnt name!')
            msg.display()
            return
        if(self.edit):
            for i, player in enumerate(self.master.players):
                if player.uuid == self.master.players[self.master.player].uuid:
                    self.master.players[i] = Player(self.etrName.val, 0)
        else:
            self.master.players.append(Player(self.etrName.val, 0))
        #self.master.player = Player(self.etrName.val, 0)
        print([o.uuid for o in self.master.players])
        ProfileIO.set_profiles(self.master.players, self.master.player)
        self.master.show(self.next)

class Profile(base_frame):
    def __new__(cls, master, *args, **kwargs):
        if len(master.players) == 0:
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
        #self.lblNameValue = tk.Label(self, text=self.master.player.display_name)
        self.lblvar = tk.StringVar(self, self.master.players[self.master.player].display_name)
        self.lblvar.trace_add('write', self._dropdown_changed)
        #print([o.display_name for o in self.master.players])
        self.lblNameValue = tk.OptionMenu(self, self.lblvar, *[o.display_name for o in self.master.players]) #[o.attr for o in objs]
        self.lblUUDI = tk.Label(self, text='User ID')
        self.lblUUIDValue = tk.Label(self, text=self.master.players[self.master.player].uuid)
        self.btnEdit = tk.Button(self, text='Edit Profile', command=lambda *args: self.master.show(NewProfile, edit=True, id=self.master.player))
        self.btnDelete = tk.Button(self, text='Delete profile', command=lambda *args: self._delete())
        self.btnAdd = tk.Button(self, text='Add profile', command=lambda *args: self.master.show(NewProfile))
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
        self.btnAdd.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=2, row=8, columnspan=2)
        self.btnEdit.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=5, row=8, columnspan=3)
        self.btnDelete.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=8, row=8)
        self.btnMenu.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=9, row=1)
    
    def _delete(self):
        del self.master.players[self.master.player]
        self.master.player = 0
        self.master.show(Profile)
        ProfileIO.set_profiles(self.master.players, self.master.player)

    def _dropdown_changed(self, *args):
        for i, player in enumerate(self.master.players):
            if player.display_name == self.lblvar.get():
                self.master.player = i
                break
        ProfileIO.set_profiles(self.master.players, self.master.player)
        self.lblUUIDValue.config(text=self.master.players[self.master.player].uuid)