class _base_color():
    def __init__(self, html: str = '', *args) -> None:
        self._html = html
        self._shades = []
        self.complement = None

        for arg in args:
            self._shades.append(_base_color(arg))

    def __str__(self) -> str:
        return '#'+self._html.upper()
    
    def __getattr__(self, name: str) -> str:
        if(name.startswith('shade')):
            try:
                return self._shades[int(name[5:])-1]
            except IndexError:
                return self
                raise AttributeError(f'color "{name}" does not exist')
        else:
            raise AttributeError()

    @property
    def rgb(self):
        r = int(self._html[0:2], 16)
        g = int(self._html[2:4], 16)
        b = int(self._html[4:6], 16)
        return [r, g, b]
    
    @property
    def html(self):
        return self.__str__()
    

    
class _complement(_base_color):
    def __init__(self, color: _base_color, original_color: _base_color) -> None:
        super().__init__(color._html)
        self.complement = original_color
    

class color():
    red = _base_color('e30613')
    white = _base_color('ffffff')
    black = _base_color('000000')
    anthracite = _base_color('575757', '797979', '9a9a9a', 'bcbcbc', 'dddddd')
    turquoise = _base_color('0c8282', '3d9b9b', '6db4b4', '9ecdcd', 'cee6e6')
    green = _base_color('005f35', '337f5d', '669f86', '99bfae', 'ccdfd7')
    blue = _base_color('00466e', '336b8b', '7090a8', '99b5c5', 'ccdae2')
    yellow = _base_color('f0a000', 'f3b333', 'f6c666', 'f9d999', 'fceccc')
    lightblue = _base_color('75a5af')
    brown = _base_color('731e1e')
    purple = _base_color('551432')
    rose = _base_color('e15f5f')
    pink = _base_color('bc4077')
    lightgreen = _base_color('6ea52d')
    beige = _base_color('967d51')
    orange = _base_color('ff5f00')
    lightpurple = _base_color('816183')

    red.complement = white
    white.complement = anthracite
    black.complement = white
    anthracite.complement = white
    anthracite.shade1.complement = white
    anthracite.shade2.complement = white
    anthracite.shade3.complement = black
    anthracite.shade4.complement = black
    turquoise.complement = white
    turquoise.shade1.complement = white
    turquoise.shade2.complement = white
    turquoise.shade3.complement = black
    turquoise.shade4.complement = black
    green.complement = white
    green.shade1.complement = white
    green.shade2.complement = white
    green.shade3.complement = black
    green.shade4.complement = black
    blue.complement = white
    blue.shade1.complement = white
    blue.shade2.complement = white
    blue.shade3.complement = black
    blue.shade4.complement = black
    yellow.complement = white
    yellow.shade1.complement = black
    yellow.shade2.complement = black
    yellow.shade3.complement = black
    yellow.shade4.complement = black
    lightblue.complement = anthracite
    brown.complement = white
    purple.complement = white
    rose.complement = white
    pink.complement = white
    lightgreen.complement = white
    beige.complement = white
    orange.complement = white
    lightpurple.complement = white

COLOR = color()

if __name__ == "__main__":
    COLOR = color()
    print(COLOR.red)
    print(COLOR.red.complement)