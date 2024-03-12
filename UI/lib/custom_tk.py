import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import font as tkfont
from enum import Enum
import os as os

# custom implementation of a combo box for easy updates to the option list and a search function to filter the oprions by the entry field
class Combobox(tk.Frame):
    def __init__(self, parent, autosearch=False, borderless=False, *args, **kwargs):
        tk.Frame.__init__(self, parent, borderwidth=kwargs.get('borderwidth'))
        self.focus = [False, False]
        self.parent = parent
        self.entry_var = tk.StringVar(value='')
        self.innerFrame = innerframe(self, textvariable = self.entry_var, borderless=borderless, *args, **kwargs)
        self.innerFrame.pack()
        self.values = {}
        self.opened =  False
        self.innerFrame.bind("<FocusOut>", self.lostfocus)
        self.autosearch = False
        self.set_autosearch(autosearch)
        self.update()
        self.mymaster = self
        if(kwargs.pop('embedded', False)):
            while(not hasattr(self.mymaster, 'toplevelwidget') or self.mymaster.toplevelwidget != True):
                self.mymaster = self.mymaster.master
        self.dropdown = Listbox(self.mymaster, selectmode=tk.SINGLE, activestyle='none', height=10, width=self.mymaster.winfo_width(), command=self.selectEntry)

    def buttonpress(self, event=None):
        self.innerFrame.entry.focus_set()
        self.toggledropdown(event)

    def toggledropdown(self, *args):
        if(self.opened):
            self.closedropdown()
        else:
            self.opendropdown()

    def closedropdown(self, *args):
        self.opened = False
        self.parent.focus_set()
        try:
            self.dropdown.place_forget()
        except:
            pass

    def focusin(self, int, event=None):
        self.focus[int] = True
        if(int == 1):
            self.opendropdown()

    def lostfocus(self, event=None):
        self.closedropdown()
        
    def search(self, string=""):
        self.filtered = list()
        for item in self.values:
            if string.casefold() in item.casefold():
                self.filtered.append(item)
        self.dropdown["values"] = self.filtered

    def set_autosearch(self, bool: bool):
        if(self.autosearch != bool):
            self.autosearch = bool
            if(bool):
                self.filtered = list()
                self.entry_var.trace_id = self.entry_var.trace("w", callback = lambda name, index, mode, entry_var=self.entry_var: self.search(entry_var.get()))
            else:
                delattr(self, "filtered")
                try:
                    self.entry_var.trace_vdelete(self.entry_var.trace_id)
                except:
                    pass

    def selectEntry(self, key):
        if hasattr(self, 'filtered') and len(self.filtered) > 0:
            value = self.filtered[key]
        else:
            value = self.values[key]
        self.innerFrame.entry.delete(0,tk.END)
        self.innerFrame.entry.insert(0,value)
        self.closedropdown()
        self.innerFrame.focus_set()

    def opendropdown(self, event=None):
        self.opened = True
        try: 
            #print(self.dropdown["values"])
            self.dropdown.place(x=self.mymaster.winfo_x(), y=self.mymaster.winfo_y() + self.mymaster.winfo_height())
        except AttributeError:
            self.dropdown = Listbox(self.mymaster, selectmode=tk.SINGLE, activestyle='none', height=10, width=self.mymaster.winfo_width(), command=self.selectEntry)
            self.dropdown.place(x=self.winfo_x(), y=self.winfo_y() + self.innerFrame.winfo_height())
        self.dropdown["values"] = self.values
        self.dropdown.config(width=self.innerFrame.winfo_width())
        self.dropdown.lift()

    def __setitem__(self, key, value):
        match key:
            case 'value':
                self.entry_var.set(value)
            case 'values':
                self.values = value
                if(self.opened):
                    self.dropdown["values"] = value
            case 'autosearch':
                self.set_autosearch(key)
            case _:
                return super().__setitem__(key, value)

    def __getitem__(self, key: str):
        match key:
            case 'value':
                return self.entry_var.get()
            case 'values':
                return self.dropdown['values']
            case 'autosearch':
                return self.autosearch
            case _:
                return super().__getitem__(key)

# bundle of an entry field and a button
# used inside the custom combobox
class innerframe(tk.Frame):
    def __init__(self, parent, *args, borderless=False, **kwargs):
        if(borderless): borderthickness=0
        else: borderthickness=1
        tk.Frame.__init__(self, parent, highlightthickness=borderthickness, highlightbackground="grey", highlightcolor="#0076d7")
        self.entry = tk.Entry(self, textvariable=kwargs['textvariable'], font=kwargs.get('font', None))
        self.entry = tk.Entry(self, borderwidth=0, textvariable=kwargs['textvariable'], font=kwargs.get('font', None))
        self.entry.pack(side = tk.LEFT, fill = tk.BOTH)
        self.button = tk.Button(self, text='\u25BC', bg='white', height=1, borderwidth=0, command=parent.buttonpress, font=kwargs.get('font', None))
        self.button.bind("<Enter>", lambda event:[event.widget.config(background='#E5F1FB')])
        self.button.bind("<Leave>", lambda event:[event.widget.config(background='white')])
        self.button.pack(side = tk.RIGHT, fill = tk.BOTH)
        self.entry.bind("<1>", parent.toggledropdown)
            
class Combobox2(tk.Frame):
    def __init__(self, parent, autosearch=False, *args, **kwargs):
        self.focus = [False, False]
        self.parent = parent
        self.entry_var = tk.StringVar(value='')
        self.values = {}
        self.opened =  False
        self.bg=kwargs.pop('bg', 'white')
        self.fg=kwargs.pop('fg', 'black')
        kwargs['bg'] = self.bg
        self.font=kwargs.pop('font', None)
        kwargs['font'] = self.font
        self.offset = kwargs.pop('offset', [0,0])
        #super().__init__(parent, borderwidth=kwargs.get('borderwidth'), textvariable = self.entry_var, borderless=borderless, *args, **kwargs)
        
        if(kwargs.pop('borderless', False)): borderthickness=0
        else: borderthickness=1
        super().__init__(parent, highlightthickness=borderthickness, highlightbackground="grey", highlightcolor="#0076d7")
        self.mymaster = self
        if(kwargs.pop('embedded', False)):
            while(not hasattr(self.mymaster, 'toplevelwidget') or self.mymaster.toplevelwidget != True):
                self.mymaster = self.mymaster.master
        kwargs_entry = kwargs.copy()
        self.entry = tk.Entry(self, borderwidth=kwargs_entry.pop('borderwidth', 1), textvariable=self.entry_var, **kwargs_entry)
        self.entry.pack(side = tk.LEFT, fill = tk.BOTH)
        #font = self.entry['font'].split(' ')
        debug_font = self.entry.cget('font')
        font = self.entry.cget('font').rsplit(' ', 1)
        if(len(font) == 1):
            self.fontsize = tkfont.nametofont(font[0]).actual()['size']
        else: self.fontsize = font[1]
        self.image=tk.PhotoImage(width=1, height=1)
        debug_width=int(self.entry.winfo_height() * self.fontsize) + int(kwargs.get('borderwidth', 0))
        self.button = tk.Button(self, text='\u25BC', bg=self.bg, fg=self.fg, image=self.image, compound="center",height=1, width=int(self.entry.winfo_height() * self.fontsize) + int(kwargs.get('borderwidth', 0)), borderwidth=0, pady=0, command=self.buttonpress, font=kwargs.get('font', None))
        self.button.bind("<Enter>", lambda event:[event.widget.config(bg='#E5F1FB')])
        self.button.bind("<Leave>", lambda event:[event.widget.config(bg=self.bg)])
        self.button.pack(side = tk.RIGHT, fill = tk.BOTH)
        self.entry.bind("<Button-1>", self.toggledropdown)

        self.bind("<FocusOut>", self.lostfocus)
        self.autosearch = False
        self.set_autosearch(autosearch)
        self.update()
        self.dropdown = Listbox(self.mymaster.master, selectmode=tk.SINGLE, activestyle='none', height=10, width=self.mymaster.winfo_width(), command=self.selectEntry)
        #print(self.master.winfo_reqwidth())
        #print(self.mymaster.winfo_reqwidth())
        #self.offset[0] = (self.mymaster.master.winfo_reqwidth() - self.mymaster.winfo_reqwidth())/2
        #print(self.mymaster.master.winfo_reqwidth())
        #print(self.mymaster.winfo_width())
        #print(self.offset)

    def buttonpress(self, event=None):
        self.entry.focus_set()
        self.toggledropdown(event)

    def toggledropdown(self, *args):
        if(self.opened):
            self.closedropdown()
        else:
            self.opendropdown()

    def closedropdown(self, *args):
        self.opened = False
        self.parent.focus_set()
        try:
            self.dropdown.place_forget()
        except:
            pass

    def focusin(self, int, event=None):
        self.focus[int] = True
        if(int == 1):
            self.opendropdown()

    def lostfocus(self, event=None):
        self.closedropdown()
        
    def search(self, string=""):
        self.filtered = list()
        for item in self.values:
            if string.casefold() in item.casefold():
                self.filtered.append(item)
        self.dropdown["values"] = self.filtered

    def set_autosearch(self, bool: bool):
        if(self.autosearch != bool):
            self.autosearch = bool
            if(bool):
                self.filtered = list()
                self.entry_var.trace_id = self.entry_var.trace("w", callback = lambda name, index, mode, entry_var=self.entry_var: self.search(entry_var.get()))
            else:
                delattr(self, "filtered")
                try:
                    self.entry_var.trace_vdelete(self.entry_var.trace_id)
                except:
                    pass

    def selectEntry(self, key):
        if hasattr(self, 'filtered') and len(self.filtered) > 0:
            value = self.filtered[key]
        else:
            value = self.values[key]
        self.entry.delete(0,tk.END)
        self.entry.insert(0,value)
        self.closedropdown()
        self.focus_set()

    def opendropdown(self, event=None):
        self.opened = True
        #try: 
            #print(self.dropdown["values"])
        #print(self.mymaster.winfo_reqwidth())
        #print(self.master.winfo_reqwidth())
        #self.offset[0] = (self.mymaster.winfo_width() - self.master.winfo_width())/2
        try:
            self.offset[0] = self.mymaster.margin.left
            self.offset[1] = (self.mymaster.margin.bottom + self.master.cget('borderwidth')) * -1
        except:
            self.offset[0] = (self.mymaster.winfo_width() - self.master.winfo_width())/2
        
        #print(self.dropdown.cget('borderwidth'))

        self.dropdown.place(x=self.mymaster.winfo_x()+self.offset[0], y=self.mymaster.winfo_y() + self.mymaster.winfo_height()+self.offset[1])
        #self.dropdown.place(x=self.mymaster.winfo_x(), y=self.mymaster.winfo_y() + self.mymaster.winfo_height()+self.offset[1])
        
        #except AttributeError:
        #    self.dropdown = Listbox(self.mymaster, selectmode=tk.SINGLE, activestyle='none', height=10, width=self.mymaster.winfo_width(), command=self.selectEntry)
        #    self.dropdown.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
        self.dropdown["values"] = self.values
        #self.dropdown.config(width=self.winfo_width())
        try:
            self.dropdown.config(width=self.mymaster.winfo_width()-self.mymaster.margin.left-self.mymaster.margin.right)
        except:
            self.dropdown.config(width=self.mymaster.winfo_width())
        self.dropdown.lift()

    def __setitem__(self, key, value):
        match key:
            case 'value':
                self.entry_var.set(value)
            case 'values':
                self.values = value
                if(self.opened):
                    self.dropdown["values"] = value
            case 'autosearch':
                self.set_autosearch(key)
            case _:
                return super().__setitem__(key, value)

    def __getitem__(self, key: str):
        match key:
            case 'value':
                return self.entry_var.get()
            case 'values':
                return self.dropdown['values']
            case 'autosearch':
                return self.autosearch
            case _:
                return super().__getitem__(key)

# custom listbox, automatically adds a scroll bar, when the item count exceeds the height of the list
class Listbox(tk.Frame):
    def __init__(self, master=None, command=None, height=10, width=100, *args, **kwargs):
        super().__init__(master, highlightbackground="black", width=width, highlightthickness=1)
        self.pack_propagate(0)
        self.height = height
        self.width = width
        self.listbox = tk.Listbox(self, height=height, width=1, highlightthickness=0, borderwidth=0, *args, **kwargs)
        if command != None: self.callback = command
        self.placement = None
        self.scrollbar = tk.Scrollbar(self)
        self.listbox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar['command'] = self.listbox.yview

        self.listbox.pack(expand=1, side = tk.LEFT, fill = tk.BOTH)

        self.listbox.bind("<Motion>", self.on_motion)
        self.bind("<Leave>", self.on_leave)
        self.listbox.bind("<Button-1>", self.print)
        self.config(height=self.children_height(self))
        
        
    def children_height(self, frame: tk.Frame):
        children = frame.winfo_children()
        if(len(children) == 0):
            return 0
        return max(map(tk.Widget.winfo_reqheight,children))

    def callback(*args, **kwargs):
        pass

    def print(self, event):
        self.callback(self.listbox.index("@%s,%s" % (event.x, event.y)))

    def on_motion(self, event):
        self.on_leave(event)
        self.listbox.selection_set(self.listbox.index("@%s,%s" % (event.x, event.y)))

    def on_leave(self, event):
        for i in self.listbox.curselection():
            self.listbox.selection_clear(i)

    def __setitem__(self, key: str, value: any) -> None:
        match key:
            case 'values':
                self.listbox.delete(0, tk.END)  #clear listbox
                self.scrollbar.pack_forget()
                for item in value: #populate listbox again
                    self.listbox.insert(tk.END, item)
                if(len(value) > self.height):
                    self.scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH)
                self.config(height=self.children_height(self))
            case _:
                return super().__setitem__(key, value)

    def __getitem__(self, key: str):
        return super().__getitem__(key)

# bundle of a entry field and a button to open a file selector
# filetypes: list of strings with allowed file types
# title: title of the file selector popup
# preselected: path to a preselected file, otherwise None
# initialdir: path to a folder the selection should start in, only applies if preselected is None
class filepicker(tk.Frame):
    def __init__(self, master, height=10, width=100, filetypes=(), title='Select a file', preselected=None, initialdir=os.path.expanduser( '~' ), *args, **kwargs) -> None:
        super().__init__(master, width=width, highlightbackground="black", highlightthickness=0)
        self.pack_propagate(0) # disables the item to shrink to its elements, therefore the width is defined by the frame and the entry widget fills it up
        self.height = height
        self.width = width
        self.filetypes = filetypes
        self.title = title
        self.initialdir = initialdir

        self.textvar = tk.StringVar(value=preselected)
        self.Entry = tk.Entry(self, textvariable=self.textvar)
        self.Button = tk.Button(self, text='...', command=self.pickFile)
        self.Button.pack(side = tk.RIGHT, fill= tk.BOTH)
        self.Entry.pack(expand=1, side = tk.LEFT, fill = tk.BOTH) # expand=1 makes the widget fill out the parent
        self.config(height=self.children_height(self))

    # opens a file picker and writes the selected file into the entry widget
    def pickFile(self):
        if(self.textvar.get() == ''):
            initialdir = self.initialdir
            initialfile = None
        else:
            initialdir = os.path.dirname(self.textvar.get())
            initialfile = os.path.basename(self.textvar.get())
        buffer = fd.askopenfilename(
            title=self.title,
            initialdir=initialdir,
            initialfile=initialfile,
            filetypes=self.filetypes
        )
        if(buffer != None): self.textvar.set(buffer)

    # used to determine the height of the entry widget to apply for the frame as well    
    def children_height(self, frame: tk.Frame):
        children = frame.winfo_children()
        if(len(children) == 0):
            return 0
        return max(map(tk.Widget.winfo_reqheight,children))

    # simple getter for easy retrieval of the selected path
    def get(self) -> str:
        return self.textvar.get()

# standard tk Label, that features an option to hide any input by dots
class Label(tk.Label):
    def __init__(self, *args, password=False, **kwargs) -> None:
        if(password):
            text = kwargs.pop('text', None)
        super().__init__(*args, **kwargs)
        self._password = password
        if(password and text != None):
            self._setText(text)

    def config(self, **kwargs):
        password = kwargs.pop('password', None)
        if(password != None and password != self._password):
            if(password):
                self._setText(self.cget('text'))
            else:
                self.config(text=self._text)
            self._password = password
        if(self._password):
            text = kwargs.pop('text', None)
            if(text != None):
                self._setText(text)
        if(len(kwargs) > 0):
            self.configure(**kwargs)

    # custom setter for text, that replaces text with eight dots and stores the text in a variable
    def _setText(self, text):
        self._text = text
        if(len(text) > 0):
            self.configure(text='\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022')
        else:
            self.configure(text='')

    # custom getter for text, that returns text from variable instead of label when password mode is enabled
    # otherwise use standard getter
    def cget(self, key):
        if(key == 'test' and self._password):
            return self._text
        else:
            return self.tk.call(self._w, 'cget', '-' + key)

    __getitem__ = cget

class OptionMenu(tk.OptionMenu):
    def __init__(self, master, variable, value, *values, **kwargs) -> None:
        filter = ('font', 'bg')
        attributes = dict()
        kwargs_copy = dict(kwargs)
        for key, value in kwargs_copy.items():
            if key in filter:
                attributes[key] = kwargs.pop(key, None)
        super().__init__(master, variable, value, *values, **kwargs)
        for key, value in attributes.items():
            self.config(**{key: value})

class Checkbutton(tk.Frame):
    def __init__(self, master, height=10, width=100, filetypes=(), title='Select a file', preselected=None, initialdir=os.path.expanduser( '~' ), *args, **kwargs) -> None:
        super().__init__(master, width=width, highlightbackground="black", highlightthickness=0)
        self.pack_propagate(0) # disables the item to shrink to its elements, therefore the width is defined by the frame and the entry widget fills it up
        self.height = height
        self.width = width
        self.filetypes = filetypes
        self.title = title
        self.initialdir = initialdir
        self._var = tk.BooleanVar(value=kwargs.pop('value', None))

        self.Entry = tk.Checkbutton(self, variable=self._var, onvalue=kwargs.pop('onvalue', None), offvalue=kwargs.pop('offvalue', None), bg=kwargs.get('bg', None))
        self.Button = tk.Label(self, **kwargs)
        self.Button.pack(side = tk.RIGHT, fill= tk.BOTH)
        self.Entry.pack(expand=1, side = tk.LEFT, fill = tk.BOTH) # expand=1 makes the widget fill out the parent
        self.config(height=self.children_height(self))

    # used to determine the height of the entry widget to apply for the frame as well    
    def children_height(self, frame: tk.Frame):
        children = frame.winfo_children()
        if(len(children) == 0):
            return 0
        return max(map(tk.Widget.winfo_reqheight,children))
    
    @property
    def val(self):
        return self._var.get()
    
    @val.setter
    def val(self, value):
        self._var.set(value)

    @property
    def var(self):
        return self._var
    
class Entry(tk.Entry):
    def __init__(self, master, *args, **kwargs) -> None:
        config = dict()
        if(kwargs.pop('password', False)):
            kwargs['show'] = '\u2022'
        if('state' in kwargs.keys() and kwargs['state'] not in ('normal', 'readonly', 'disabled')):
            match kwargs.pop('state'):
                case 'label':
                    kwargs['state'] = 'disabled'
                case _:
                    pass
        self._val = tk.StringVar(value = kwargs.pop('text', None))
        super().__init__(master, *args, textvariable=self._val, **kwargs)
        
        self.config(disabledbackground=self.cget('bg'))
        self.config(disabledforeground=self.cget('fg'))
         

    @property
    def val(self):
        return self._val.get()
    
    @val.setter
    def val(self, value):
        self._val.set(value)

    @property
    def var(self):
        return self._val

    def config(self, cnf=None, **kw):
        if(cnf==None):
            for key, value in kw.items():
                match(key):
                    case 'command':
                        self.callback = value
                    case 'text':
                        self.val = value
                    case 'password':
                        if(value):
                            self.config(show='\u2022')
                        else:
                            self.config(show='')
                    case 'state':
                        if(value not in ('normal', 'readonly', 'disabled')):
                            match value:
                                case 'label':
                                    super().config(cnf, **{'state': 'disabled'})
                                    super().config(cnf, **{'bg': self.cget('bg')})
                                    super().config(cnf, **{'bd': self.cget('bg')})
                                    print(self.cget('bg'))
                                case _:
                                    pass
                        else:
                            return super().config(cnf, **{key: value})
                    case _:
                        return super().config(cnf, **{key: value})
        else:
            return super().config(cnf, **kw)