import tkinter as tk

from .base_frame import base_frame
from .field_frame import Field

class availableClients(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master)
        self.ai = ['weak', 'strong']
        self.local = ['local']
        self.network = ['test']
        self.clients = []
        self.widgets = []
        self.columnconfigure(0, weight=8)
        self.columnconfigure([1,2], weight=1)
        self.reload()

    def reload(self):
        for entry in self.widgets:
            for widget in entry:
                widget.forget()
        for i, client in enumerate(self.local + self.ai + self.network):
            name = tk.Label(self, text=client)
            button0 = tk.Button(self, text="Slot1")
            button0.config(command=lambda e=i, b=button0: self._join(0, b, e))
            button1 = tk.Button(self, text="Slot2")
            button1.config(command=lambda e=i, b=button1: self._join(1, b, e))

            name.grid(column=0, row=i, sticky=tk.N+tk.E+tk.S+tk.W)
            button0.grid(column=1, row=i, sticky=tk.N+tk.E+tk.S+tk.W)
            button1.grid(column=2, row=i, sticky=tk.N+tk.E+tk.S+tk.W)

            self.widgets.append([name, button0, button1])

    def _join(self, slot, button, id):
        for b in list(zip(*self.widgets))[slot+1]:
            b.config(state=tk.DISABLED)
            b.config(bg='red')
            b.config(fg='White')
        button.config(bg='green')
        self.master.join(slot, (self.local + self.ai + self.network)[id])

    def clear(self, slot):
        for button in list(zip(*self.widgets))[slot+1]:
            button.config(state=tk.NORMAL)
            button.config(bg='SystemButtonFace')
            button.config(fg='Black')

class slot(tk.Frame):
    def __init__(self, master, slot, title):
        super().__init__(master)
        self.slot = slot
        self.empty = tk.Label(self, text=title)
        self.player = tk.Label(self)
        self.kick = tk.Button(self, text="Remove", command=self.clear)
        self.empty.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W, columnspan=2)
        self.columnconfigure(0, weight=19)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    def fill(self, name):
        self.empty.grid_forget()
        self.player.config(text=name)
        self.player.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.kick.grid(column=1, row=0, sticky=tk.N+tk.E+tk.S+tk.W)

    def clear(self):
        self.player.grid_forget()
        self.kick.grid_forget()
        self.empty.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W, columnspan=2)
        self.master.clear(self.slot)

class CustomLobby(base_frame):
    """
    Custom lobby for the game. This class is used to display the custom lobby window and send messages to the server.
    It is only used for internal testing.
    """
    def __init__(self, master, *args):
        super().__init__(master)
        self.player = list()
        self.player_ready = [False]*2
        self.ready = tk.BooleanVar(self, value=False)
        self.after_handles = list()
        self.ready.trace_add("write", lambda *args: self._timer_trigger())
        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self.lblheading = tk.Label(self, bg="white", text="Custom lobby")
        self.availableClients = availableClients(self)
        self.slot0 = slot(self, 0, "Slot 1")
        self.slot1 = slot(self, 1, "Slot 2")
        self.lblTimer = tk.Label(self, text="")
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
        self.availableClients.grid(column=1, row=3, columnspan=3, rowspan=7, sticky=tk.E+tk.W+tk.N+tk.S)
        self.slot0.grid(column=7, row=3, columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S)
        self.slot1.grid(column=7, row=5, columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S)
        self.lblTimer.grid(column=0, row=100, columnspan=11, sticky=tk.E+tk.W)
        self.btnMenu.grid(sticky=tk.E+tk.W+tk.N+tk.S, column=9, row=1)

    def join(self, slot, player):
        match slot:
            case 0:
                self.slot0.fill(str(player))
            case 1:
                self.slot1.fill(str(player))

    def clear(self, slot):
        self.availableClients.clear(slot)

    def start(self, player, set=None):
        if(set != None):
            self.player_ready[player] = set
        else:
            self.player_ready[player] = not self.player_ready[player]
        if(self.player_ready[0] == self.player_ready[1] == True):
            self.ready.set(True)
        else:
            self.ready.set(False)
        return self.player_ready[player]

    def _timer_trigger(self):
        if(self.ready.get() == True):
            self._timer(5)
        else:
            self.lblTimer.config(text="")
            if(len(self.after_handles) > 0):
                self.after_cancel(self.after_handles.pop())

    def _timer(self, counter):
        self.lblTimer.config(text=f'Game starts in {counter}...')
        if(counter == 0):
            self.master.show(Field)
        elif(counter > 0):
            self.after_handles.append(self.after(1000, self._timer, counter -1))