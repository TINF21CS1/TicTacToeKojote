import tkinter as tk

from .base_frame import base_frame

class Field(base_frame):
    def __init__(self, master):
        super().__init__(master)
        self._create_widgets()
        self._display_widgets()

    def _create_widgets(self):
        self.button = tk.Button(self, text="close", command=self.master.show_menu)

    def _display_widgets(self):
        self.button.pack(fill="both", expand=True)