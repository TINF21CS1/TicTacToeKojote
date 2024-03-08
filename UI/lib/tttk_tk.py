import tkinter as tk

from . import custom_tk as ctk
from .framed_tk import wrapper as ftk_wrapper
#from .framed_tk import Entry as ftk_Entry
from .colors import COLOR, color

N = tk.N
E = tk.E
S = tk.S
W = tk.W
NE = tk.NE
SE = tk.SE
SW = tk.SW
NW = tk.NW

class wrapper(ftk_wrapper):
    def __init__(self, Widget: tk.Widget, master: tk.Misc, *args, **kwargs):
        defaultValues = kwargs.pop('defaultValues', {})
        kwargs['defaultValues'] = {
                'font': ("Arial bold", 12),
                'margin': 5,
                'bg': '#FFFFFF',} | defaultValues
        super().__init__(Widget, master, *args, **kwargs)

class Entry(wrapper):                   
    def __init__(self, master: tk.Misc | None = None, *args, color: color = COLOR.anthracite, inverted: bool = False, **kwargs) -> None:

        self._fg = color if not inverted else color.complement
        self._bg = color.complement if not inverted else color
        self._bd = color if (not inverted) else color.complement


        super().__init__(
            Widget=ctk.Entry, 
            master=master, 
            defaultValues={
                'padding': 5,
                'border': 2,
                'fg': self._fg,
                'bg': self._bg,
                'border_color': self._bd,
                'relief': tk.FLAT,
            },
            *args, 
            **kwargs
        )
        self.main_attributes.extend(('_error', 'error_set', 'error_reset', 'error_get'))
        self._error=False
  
    def error_set(self):
        self._error = True
        self.config(border_color= COLOR.red)
        return self

    def error_reset(self):
        self._error = False
        self.config(border_color= self._bd)
        return self

    def error_get(self):
        return self._error
    
class Label(wrapper):
    def __init__(self, master: tk.Misc | None = None, *args, color: color = COLOR.anthracite, inverted: bool = False, **kwargs) -> None:

        self._fg = color if not inverted else color.complement
        self._bg = color.complement if not inverted else color

        super().__init__(
            Widget=ctk.Label, 
            master=master, 
            defaultValues={
                'fg': self._fg,
                'bg': self._bg,
                'text': None,
            },
            *args, 
            **kwargs
        )

class Button(wrapper):
    def __init__(self, master: tk.Misc | None = None, *args, inverted: bool = False, main: bool = False, **kwargs) -> None:
        config = dict()
        config['command'] = kwargs.pop('command', None)
        if(config['command']==None): config.pop('command')
        if('bg' in kwargs.keys() or 'background' in kwargs.keys()):
            kwargs['border_color'] = kwargs.get('bg', kwargs.get('background'))

        if('color' not in kwargs.keys()):
            if(not main):
                color = COLOR.anthracite
            else:
                color = COLOR.red
        else:
            color = kwargs.pop('color')

        self._fg = color if inverted == main else color.complement
        self._bg = color.complement if inverted == main else color
        self._bd = color if (not inverted) else color.complement

        super().__init__(
            Widget=tk.Label, 
            master=master, 
            defaultValues={
                'fg': self._fg,
                'bg': self._bg,
                'border_color': self._bd,
                #'fg': '#E30613',
                #'bg': '#FFFFFF',
                #'border_color': '#E30613',
                'border': 2,
                'padding': 5,
            },
            *args, 
            **kwargs
        )
        self.main_attributes.extend(['keep_flat', 'pressed', 'released', 'callback'])
        self.bind('<Button-1>', self.pressed)
        self.bind('<ButtonRelease-1>', self.released)

        for key, value in config.items():
            self.config(**{key: value})

    def pressed(self, event):
        self.config(bg=self._fg)
        self.config(fg=self._bg)

    def released(self, event): 
        self.config(bg=self._bg)
        self.config(fg=self._fg)
        self.callback()

    def callback(self):
        pass

    def config(self, cnf=None, **kw):
        if(cnf==None):
            for key, value in kw.items():
                match(key):
                    case 'command':
                        self.callback = value
                    case 'bg' | 'background':
                        #super().config(cnf, border_color= value)
                        return super().config(cnf, bg= value)
                    case _:
                        return super().config(cnf, **{key: value})
        else:
            return super().config(cnf, **kw)

class Combobox(wrapper):

    def __init__(self, master: tk.Misc | None = None, *args, **kwargs) -> None:
        color = kwargs.pop('color', COLOR.anthracite)
        inverted = kwargs.pop('inverted',False)

        self._fg = color if not inverted else color.complement
        self._bg = color.complement if not inverted else color
        self._bd = color if (not inverted) else color.complement
        super().__init__(
            Widget=ctk.Combobox2, 
            master=master, 
            defaultValues={
                'relief': tk.FLAT,
                'embedded': True,
                'borderless': True,
                'fg': self._fg,
                'bg': self._bg,
                'border_color': self._bd,
                'border': 2,
                'padding': 5,
            },
            *args, 
            **kwargs
        )

        #ctk.Combobox2(root, autosearch=True, bg='pink', borderwidth=0, relief= tk.FLAT, borderless=True)

class OptionMenu(wrapper):
    def __init__(self, master: tk.Misc | None, *args, **kwargs) -> None:
        super().__init__(
            ctk.OptionMenu, 
            master, 
            defaultValues={
                'border_color': '#000000',
                'border': 2,
                #'relief': tk.FLAT,
            },
            *args, 
            **kwargs
        )

class Checkbutton(wrapper):
    def __init__(self, master: tk.Misc | None, *args, **kwargs) -> None:
        super().__init__(
            ctk.Checkbutton, 
            master, 
            defaultValues={
                'fg': '#575757',
                'text': None,
            },
            *args, 
            **kwargs
        )

class Frame(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args, 
            bg=kwargs.pop('bg', '#FFFFFF'),
            **kwargs
        )