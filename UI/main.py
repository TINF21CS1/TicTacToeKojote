#import tkinter as tk
from .lib import tttk_tk as tk
from tkinter import _tkinter
from tkinter import font as tkfont
from queue import Queue

from .menu import Menu
from Client.profile_save import Profile as ProfileIO

class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        start_width = 500
        min_width = 400
        start_height = 300
        min_height = 250

        self.devOptions = False
        self.players, self.player = ProfileIO.get_profiles()
        self.ai_thread = None
        self.network_events = {}
        self.out_queue = {}
        self.in_queue = Queue()
        self.dummy = tk.Container()

        self.geometry(f"{start_width}x{start_height}")
        self.minsize(width=min_width, height=min_height)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Tic Tac Toe Kojote")
        self.geometry("700x500")
        self.frames = {}
        self.current_frame = None
        self.bind("<<queue_input>>", lambda *args: self.network_event_handler())
        self.show(Menu, True)

    def show(self, Frame, *args, cache=False, **kwargs):
        if(self.current_frame != None):
            try:
                self.current_frame.grid_forget()
                self.current_frame.destroy()
            except _tkinter.TclError:
                pass
        if(cache):
            if(Frame.__name__ not in self.frames):
                self.add_frame(Frame)
            frame = self.frames[Frame.__name__]
        else:
            frame = Frame(self, *args, **kwargs)
            if(frame != None):
                frame.grid(row=0, column=0, sticky="nsew")
        self.current_frame = frame
        return frame
        
    def add_frame(self, Frame):
        self.frames[Frame.__name__] = Frame(self)
        self.frames[Frame.__name__].grid(row=0, column=0, sticky="nsew")

    def show_menu(self):
        self.show(Menu)

    def start_mainloop(self):
        self.mainloop()

    def start_server(self):
        pass

    def network_event_handler(self):
        queue = self.in_queue.get()
        message_type = queue.pop('message_type', 'message type not found')
        if(message_type == 'python/error'):
            try:
                raise queue['error']
            except ConnectionError:
                message_type = 'lobby/connect_error'
        try:
            function = self.network_events[message_type]
        except KeyError:
            print(f"message type not found {message_type}")
        function(queue)

def main():
    app = Root()
    app.start_mainloop()