import pygame.font


class _Theme:
    _background_colour = (0, 0, 0)
    _text_colour = (255, 255, 255)
    _text_size = 22
    _big_text_size = 42
    _small_text_size = 20

    def __init__(self):
        self._font = pygame.font.Font(None, self._text_size)
        self._small_font = pygame.font.Font(None, self._small_text_size)
        self._big_font = pygame.font.Font(None, self._big_text_size)

    def background_colour(self):
        return self._background_colour

    def text_colour(self):
        return self._text_colour

    def text_size(self):
        return self._text_size

    def font(self):
        return self._font

    def big_font(self):
        return self._big_font

    def small_font(self):
        return self._small_font


class Default(_Theme):
    pass


def theme_from_config(general_config):
    theme_name = general_config["theme"]
    if theme_name == "default":
        return Default()
    else:
        raise ValueError("Invalid theme in config. theme={}".format(theme_name))
