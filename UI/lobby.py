import tkinter as tk

from .base_frame import base_frame
from .field_frame import Field
from .network import get_connected_player

class playerFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self._create_base_widgets()
        self._display_base_widgets()
        self._start(set=False)

    def _create_base_widgets(self):
        self.btnStart = tk.Button(self, text="Start", command=self._start)
    
    def _display_base_widgets(self):
        self.btnStart.grid(column=1, row=100, sticky=tk.E+tk.W)

    def _start(self, set=None):
        if(set != None):
            new_state = self.master.master.start(self.master.player_id, set)
        else:
            new_state = self.master.master.start(self.master.player_id)
        if(new_state == True):
            self.btnStart.config(text="Ready!")
        else:
            self.btnStart.config(text="Start")

class localPlayerFrame(playerFrame):
    def __init__(self, master):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()
        self._check_valid_selection()

    def _create_widgets(self):
        self.lblControl = tk.Label(self, text="Control")
        self.varControl = tk.StringVar(self, value="Select")
        self.varControl.trace_add("write", lambda *args: self._control_change())
        self.optControl = tk.OptionMenu(self, self.varControl, "Mouse", "QEYC", "IP,-")
        self.lblProfile = tk.Label(self, text="Profile")
        self.varProfile = tk.StringVar(self, value="Select")
        self.varProfile.trace_add("write", lambda *args: self._profile_change())
        self.optProfile = tk.OptionMenu(self, self.varProfile, "Profile 1", "Profile 2", "Profile 3")

    def _display_widgets(self):
        #self.columnconfigure([0,1], weight=1)
        self.lblControl.grid(column=0, row=10, sticky=tk.E+tk.W)
        self.optControl.grid(column=1, row=10, sticky=tk.E+tk.W)
        self.lblProfile.grid(column=0, row=11, sticky=tk.E+tk.W)
        self.optProfile.grid(column=1, row=11, sticky=tk.E+tk.W)

    def _control_change(self):
        self._check_valid_selection()

    def _profile_change(self):
        self._check_valid_selection()

    def _check_valid_selection(self):
        if(self.varControl.get() == "Select" or self.varProfile.get() == "Select"):
            self.btnStart.config(state=tk.DISABLED)
        else:
            self.btnStart.config(state=tk.NORMAL)

class AIPlayerFrame(playerFrame):
    def __init__(self, master):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self.lblStrength = tk.Label(self, text="Strength")
        self.varStrength = tk.StringVar(self, value="Select")
        self.varStrength.trace_add("write", lambda *args: self._strength_change())
        self.optStrength = tk.OptionMenu(self, self.varStrength, "Easy", "Medium", "Expert")

    def _display_widgets(self):
        #self.columnconfigure([0,1], weight=1)
        self.lblStrength.grid(column=0, row=1, sticky=tk.E+tk.W)
        self.optStrength.grid(column=1, row=1, sticky=tk.E+tk.W)
        self.btnStart.grid_forget()

    def _strength_change(self):
        if(self.varStrength.get() == "Select"):
            self._start(False)
        else:
            self._start(True)

class NetworkPlayerFrame(playerFrame):
    def __init__(self, master):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()
        self.btnStart.config(state=tk.DISABLED)

    def _create_widgets(self):
        self.lblWait = tk.Label(self, text="Waiting for Player to join")

    def _display_widgets(self):
        #self.columnconfigure([0,1], weight=1)
        self.lblWait.grid(column=0, row=1, sticky=tk.E+tk.W, columnspan=2)

class playerdisplay(tk.Frame):
    def __init__(self, master, player):
        super().__init__(master)
        self.player_id = player
        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self.lblPlayer = tk.Label(self, text=f'Player {self.player_id+1}')
        self.option = tk.StringVar()
        self.option.trace_add("write", lambda *args: self.type_change())
        self.option.set("Please select")
        self.lblType = tk.OptionMenu(self, self.option, "Local", "AI", "Network")
        self.playerOptions = tk.Frame(self)

    def _display_widgets(self):
        self.columnconfigure(0, weight=1)
        self.lblPlayer.grid(column=0, row=0, sticky=tk.E+tk.W)
        self.lblType.grid(column=0, row=1, sticky=tk.E+tk.W)
        self.playerOptions.grid(column=0, row=2, sticky=tk.E+tk.W)

    def type_change(self):
        try:self.playerOptions.destroy()
        except:pass
        match self.option.get():
            case "Local":
                self.playerOptions = localPlayerFrame(self)
            case "AI":
                self.playerOptions = AIPlayerFrame(self)
            case "Network":
                self.playerOptions = NetworkPlayerFrame(self)
            case _:
                self.playerOptions = tk.Frame(self)
        self.playerOptions.grid(column=0, row=2, sticky=tk.E+tk.W)

class Lobby(base_frame):
    def __init__(self, master, address, *args):
        super().__init__(master)
        self.address = address
        self.player = list()
        self.player_ready = [False]*2
        self.ready = tk.BooleanVar(self, value=False)
        self.after_handles = list()
        self.ready.trace_add("write", lambda *args: self._timer_trigger())
        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self.lblheading = tk.Label(self, width=20, height=5, bg="white", text="Lobby")
        self.lbllocation = tk.Label(self, text=f"at {self.address}")
        self.playerType = [None]*2
        self.playerType[0] = playerdisplay(self, 0)
        self.playerType[1] = playerdisplay(self, 1)
        self.lblTimer = tk.Label(self, text="")
        self.btnBack = tk.Button(self, text="Back", command=lambda: self.master.show_menu())

    def _display_widgets(self):
        self.columnconfigure([1,9], weight=10)
        self.columnconfigure(5, weight=1)
        self.lblheading.grid(column=0, row=0, columnspan=11, sticky=tk.E+tk.W)
        self.lbllocation.grid(column=0, row=1, columnspan=11, sticky=tk.E+tk.W)
        self.playerType[0].grid(column=0, row=2, sticky=tk.N+tk.E+tk.W, columnspan=2)
        self.playerType[1].grid(column=9, row=2, sticky=tk.N+tk.E+tk.W, columnspan=2)
        self.lblTimer.grid(column=0, row=100, columnspan=11, sticky=tk.E+tk.W)
        self.btnBack.grid(column=10, row=101, sticky=tk.E+tk.W)

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