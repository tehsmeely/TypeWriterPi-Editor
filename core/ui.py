import pygame
import themes


class Menu:
    def __init__(self, options, theme, midpoint):
        if len(options) < 1:
            raise ValueError("Menu must be created with nonzero number of options")
        self.options = [Option(option_s, cb, theme) for option_s, cb in options]
        self.active_index = 0
        self.padding = 10
        self.background, self.background_rect = self._make_background(theme)
        self.background_rect.center = midpoint

    def move(self, by):
        new_index = self.active_index + by
        if 0 <= new_index < len(self.options):
            self.active_index = new_index

    def reset(self):
        self.active_index = 0

    def execute(self):
        return self.options[self.active_index].callback.call()

    def should_close_on_execute(self):
        return self.options[self.active_index].callback.close_on_call

    def draw(self, screen):
        y0 = self.background_rect.top + self.padding
        x = self.background_rect.center[0]
        screen.blit(self.background, self.background_rect)
        offset = self.options[0].texture.get_size()[1]
        for (i, option) in enumerate(self.options):
            y = y0 + (i * (offset + (2 * self.padding)))
            option.draw(screen, (x, y), i == self.active_index)

    def _make_background(self, theme: themes._Theme):
        option_height = self.options[0].texture.get_size()[1]
        height = (option_height + (2 * self.padding)) * len(self.options)
        width = max([o.texture.get_size()[0] for o in self.options]) + (
            2 * self.padding
        )
        background = pygame.Surface((width, height))
        background.fill(theme.text_colour())
        fill_rect = pygame.Rect(1, 1, width - 2, height - 2)
        fill_rect.center = (width / 2, height / 2)
        background.fill(theme.background_colour(), fill_rect)
        return background, pygame.Rect((0, 0), (width, height))


class OptionCallback:
    def __init__(self, f, close_on_call=True):
        self.f = f
        self.close_on_call = close_on_call

    def call(self):
        return self.f()


class Option:
    def __init__(self, s, callback, theme):
        self.callback = callback
        self.texture = theme.big_font().render(s, True, theme.text_colour())
        self.texture_rect = self.texture.get_rect()
        text_size = self.texture.get_size()
        underline_width = 2
        self.underline = pygame.Surface((text_size[0], underline_width))
        self.underline.fill(theme.text_colour())
        self.underline_rect = self.underline.get_rect()
        self.underline_offset = text_size[1] - underline_width

    def draw(self, screen, midtop, active):
        self.texture_rect.midtop = midtop
        screen.blit(self.texture, self.texture_rect)
        if active:
            self.underline_rect.midtop = midtop[0], midtop[1] + self.underline_offset
            screen.blit(self.underline, self.underline_rect)
