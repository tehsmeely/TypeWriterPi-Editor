class _Theme:
    _background_colour = (0,0,0)
    _text_colour = (255,255,255)
    _text_size = 22

    def background_colour(self):
       return self._background_colour

    def text_colour(self):
        return self._text_colour

    def text_size(self):
        return self._text_size

class Default(_Theme):
    pass