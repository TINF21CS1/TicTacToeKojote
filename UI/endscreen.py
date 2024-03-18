#import tkinter as tk
from .lib import tttk_tk as tk
from .base_frame import base_frame
#from .field_frame import Field

class EndScreen(base_frame):
    def __init__(self, master, win:bool, winner, final_playfield, *args, local_mp=False, **kwargs):
        super().__init__(master)
        self._create_widgets(win, winner, final_playfield, local_mp)
        self._display_widgets()

    def _create_widgets(self, win:bool, winner, fp, local_mp:bool):
        if(not local_mp):
            message = "You won the game!" if win else "It's a draw!\nThat's barely more than a loss." if winner == None else "You lost the game!"
        else:
            message = "It's a draw!" if winner == None else f"{winner.display_name} won the game!"
        self.lblWinner = tk.Label(self, width=20, height=5, bg="white", text=message)
        for i in range(3):
            for j in range(3):
                match fp[i][j]:
                    case 1:
                        fp[i][j] = "X"
                    case 2:
                        fp[i][j] = "O"
                    case _:
                        fp[i][j] = "  "
        self.lblPlayfield = tk.Label(self, width=20, height=5, bg="white", text=f'{fp[0][0]}|{fp[0][1]}|{fp[0][2]}\n_ _ _\n{fp[1][0]}|{fp[1][1]}|{fp[1][2]}\n_ _ _\n{fp[2][0]}|{fp[2][1]}|{fp[2][2]}')
        self.btnMainMenu = tk.Button(self, text="Main Menu", width=20, height=5, command=lambda: self.master.show_menu())

    def _display_widgets(self):
        self.lblWinner.pack(fill=tk.X)
        self.lblPlayfield.pack()
        self.btnMainMenu.pack()