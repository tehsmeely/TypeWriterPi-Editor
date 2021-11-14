import pygame
from blinker import Blinker
from action import CursorDirection


class Cursor:
    def __init__(self, theme):
        self.line = 0
        self.column = 0
        self.theme = theme
        self.blinker = Blinker()
        self.rect = pygame.Rect(0, 0, 2, self.theme.text_size() - 1)

    def __repr__(self):
        return "Cursor(line:{}, column:{})".format(self.line, self.column)

    def update(self, document):
        line = document.get_current_line()
        if line is not None:
            self.rect.x = document.left_margin + line.width_to_column(self.column)
        else:
            self.rect.x = 0
        self.rect.y = self.line * self.theme.text_size()
        self.blinker.update()

    def draw(self, screen):
        if self.blinker.is_on():
            screen.fill(self.theme.text_colour(), self.rect)

    def move(self, document, direction):
        moved = False
        if direction == CursorDirection.LEFT:
            if self.column > 0:
                self.column -= 1
                moved = True
        elif direction == CursorDirection.RIGHT:
            line = document.get_current_line()
            if line is not None and self.column < len(line.content):
                self.column += 1
                moved = True

        elif direction == CursorDirection.UP:
            if self.line > 0:
                self.line -= 1
                moved = True

        elif direction == CursorDirection.DOWN:
            if self.line < len(document.lines) - 1:
                self.line += 1
                moved = True

        return moved
