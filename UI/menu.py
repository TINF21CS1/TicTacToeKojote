import tkinter as tk

from .base_frame import base_frame
from .field_frame import Field

class Menu(base_frame):
    def __init__(self, master):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self.button = tk.Button(self, text='Play', command=lambda: self.master.show(Field))

    def _display_widgets(self):
        self.button.pack(fill="both", expand=True)