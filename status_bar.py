import pygame


class StatusBar:
    def __init__(self, width, topleft, theme):
        self.padding = 1
        height = theme.small_font().size("|")[1] + (2 * self.padding)
        self.rect = pygame.Rect(topleft, (width, height))
        self.surface = pygame.Surface((width, height))
        self.theme = theme
        self.surface.fill(self.theme.text_colour())

        self.texts = ["", "", ""]
        self.text_textures = [None, None, None]
        self.text_rects = [None, None, None]
        self.dirty = True

    def set_text(self, left, mid, right):
        self.texts = [left, mid, right]
        self.dirty = True

    def set_left(self, left):
        if left != self.texts[0]:
            self.texts[0] = left
            self.dirty = True

    def set_centre(self, centre):
        if centre != self.texts[1]:
            self.texts[1] = centre
            self.dirty = True

    def set_right(self, right):
        if right != self.texts[2]:
            self.texts[2] = right
            self.dirty = True

    def draw(self, screen):
        if self.dirty:
            self._make_text()
        self.surface.fill(self.theme.text_colour())
        for text, text_rect in zip(self.text_textures, self.text_rects):
            if text is not None:
                self.surface.blit(text, text_rect)

        screen.blit(self.surface, self.rect)

    def _make_text(self):
        self.text_textures = [
            self.theme.small_font().render(
                self.texts[i], True, self.theme.background_colour()
            )
            for i in range(3)
        ]
        self.text_rects = [text.get_rect() for text in self.text_textures]
        self.text_rects[0].topleft = (self.padding, self.padding)
        self.text_rects[1].midtop = (self.rect.width / 2, self.padding)
        self.text_rects[2].topright = (self.rect.width - self.padding, self.padding)
