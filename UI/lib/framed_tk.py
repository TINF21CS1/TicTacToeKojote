import tkinter as tk

from . import custom_tk as ctk

Any = object()

class vector4d():
    def __init__(self, *args):
        if(len(args)==0):
            args=[0,0,0,0]
        self.set(*args)

    @property
    def x(self) -> int | list:
        if(self.right==self.left): return self.left
        else: return [self.right, self.left]

    @x.setter
    def x(self, x: int | list):
        if(type(x) == list):
            self.right=x[0]
            self.left=x[1]
        else:
            self.right=self.left=x

    @property
    def y(self) -> int | list:
        if(self.top==self.bottom): return self.top
        else: return [self.top, self.bottom]

    @y.setter
    def y(self, y: int | list):
        if(type(y) == list):
            self.top=y[0]
            self.bottom=y[1]
        else:
            self.top=self.bottom=y

    def get(self):
        return [self.top, self.right, self.bottom, self.left]
    
    def set(self, *args):
        match(len(args)):
            case 1:
                self.top    = args[0]
                self.right  = args[0]
                self.bottom = args[0]
                self.left   = args[0]
            case 2:
                self.top    = args[0]
                self.right  = args[1]
                self.bottom = args[0]
                self.left   = args[1]
            case 3:
                self.top    = args[0]
                self.right  = args[1]
                self.bottom = args[2]
                self.left   = args[1]
            case 4:
                self.top    = args[0]
                self.right  = args[1]
                self.bottom = args[2]
                self.left   = args[3]
            case _:
                pass

def isorientation(string: str) -> bool:
    return string in ('top', 'right', 'bottom', 'left')

class wrapper(tk.Frame):
    main_attributes = [
        'main_attributes',
        'init',
        'toplevelwidget',
        'padding',
        'border',
        'margin',
        'outerframe',
        'innerframe',
        'widget',
        'name',
        'repack',
        'config',
        'bind',
        #internal calls
        'tk',
        'children',
        'master',
        'event_handler',
    ]
    main_attributes_prefixes = [
        'winfo',
        'pack',
        'grid',
        'place',
    ]
    def __init__(self, Widget: tk.Widget, master, *args, **kwargs):
        """
        padding
        border
        margin
        """
        self.init= True
        self.toplevelwidget = True

        defaultValues = kwargs.pop('defaultValues', None)
        label = True if(kwargs.get('state', '') == 'label') else False

        if(defaultValues != None):
            kwargs = defaultValues | kwargs
        
        self.padding = vector4d(
            kwargs.pop('padding_top', 0),
            kwargs.pop('padding_right', 0),
            kwargs.pop('padding_bottom', 0),
            kwargs.pop('padding_left', 0))
        padding = kwargs.pop('padding', None)
        if(padding != None): self.padding=vector4d(padding)
        
        self.border = vector4d(
            kwargs.pop('border_top', 1),
            kwargs.pop('border_right', 1),
            kwargs.pop('border_bottom', 1),
            kwargs.pop('border_left', 1))
        border = kwargs.pop('border', None)
        if(border != None): self.border=vector4d(border)
        
        self.margin = vector4d(
            kwargs.pop('margin_top', 0),
            kwargs.pop('margin_right', 0),
            kwargs.pop('margin_bottom', 0),
            kwargs.pop('margin_left', 0))
        margin = kwargs.pop('margin', None)
        if(margin != None): self.margin=vector4d(margin)

        
        super().__init__(
            master, 
            bg=master['bg'], name=kwargs.pop('name', None),
            #bg='yellow',
        )
        self.init = False

        if('bg' not in kwargs):
            kwargs['bg'] = kwargs.pop('background', master['bg'])
        
        self.outerframe = tk.Frame(
            self, 
            bg=kwargs.pop('border_color', kwargs.get('bg')) if( not (label and Widget == ctk.Entry)) else kwargs.get('bg'),
        )

        kwargs.pop('border_color', None) #waste it, if still there

        self.innerframe = tk.Frame(
            self.outerframe,
            bg = kwargs.get('bg'),
            #bg='green',
        )

        self.widget:tk.Widget = Widget(self.innerframe, *args, **kwargs)

        self.repack()

        #self.bind('<Any>', lambda e: print('hi'))
    
    def event_handler(self, event:tk.Event):
            self.widget.event_generate(event.type)

    def repack(self):
        self.widget.pack_forget()
        self.innerframe.pack_forget()
        self.outerframe.pack_forget()

        self.widget.pack(padx=self.padding.x, pady=self.padding.y, fill='both', expand=True)
        self.innerframe.pack(padx=self.border.x, pady=self.border.y, fill='both', expand=True)
        self.outerframe.pack(padx=self.margin.x, pady=self.margin.y, fill='both', expand=True)

    def __setattr__(self, __name: str, __value) -> None:
        if(__name in self.main_attributes or __name.split('_')[0] in self.main_attributes_prefixes or 
           __name[0] == '_' or self.init):
            return object.__setattr__(self, __name, __value)
        else:
            return self.widget.__setattr__(__name, __value)
        
    def __getattribute__(self, __name: str):
        if(__name == 'main_attributes' or __name == 'main_attributes_prefixes' or
            __name in self.main_attributes or __name.split('_')[0] in self.main_attributes_prefixes or 
            __name[0] == '_' or self.init):
            return object.__getattribute__(self, __name)
        elif(__name == 'bind'):
            return self.outerframe.__getattribute__(__name)
        else:
            return self.widget.__getattribute__(__name)
        
    def __getitem__(self, key: str):
        if(key in ()):
            return object.__getitem__(key)
        else:
            return self.widget.__getitem__(key)
    
    def __setitem__(self, key: str, value) -> None:
        if(key in ()):
            return object.__setitem__(key)
        else:
            return self.widget.__setitem__(key, value)
        
    def config(self, cnf=None, **kw):
        if(cnf==None):
            for key, value in kw.items():
                key = key.split('_')
                key.append('')
                match(key[0]):
                    case 'padding':
                        match(key[1]):
                            case '':
                                self.padding = vector4d(*value)
                                self.repack()
                            case x if isorientation(x):
                                setattr(self.padding, key[1], value)
                                self.repack()
                            case _:
                                raise tk.TclError('unknown option -"'+'_'.join(key)+'"')
                    case 'border':
                        match(key[1]):
                            case '':
                                self.border = vector4d(*value)
                                self.repack()
                            case x if isorientation(x):
                                setattr(self.border, key[1], value)
                                self.repack()
                            case 'color':
                                self.outerframe.config(bg=value)
                            case _:
                                raise tk.TclError('unknown option -"'+'_'.join(key)+'"')
                    case 'margin':
                        match(key[1]):
                            case '':
                                self.margin = vector4d(*value)
                                self.repack()
                            case x if isorientation(x):
                                setattr(self.margin, key[1], value)
                                self.repack()
                            case _:
                                raise tk.TclError('unknown option -"'+'_'.join(key)+'"')
                    case 'bg' | 'background':
                        key.remove('')
                        self.widget.config(**{'_'.join(key): value})
                        self.innerframe.configure(**{'_'.join(key): value})
                    case _:
                        key.remove('')
                        self.widget.config(**{'_'.join(key): value})
        else:
            self.configure(cnf)

    def bind(self, sequence=None, func=None, add=None, recursive=True):
        if(recursive):
            self.widget.bind(sequence, func, add)
            self.innerframe.bind(sequence, func, add)
        return self.outerframe.bind(sequence, func, add)
    
