from cursor import Cursor
import pygame.font
from utils import *


class Document:
    def __init__(self, theme):
        self.font = pygame.font.Font(None, theme.text_size())
        self.theme = theme
        self.lines = [Line(self.font, theme)]
        self.cursor = Cursor(self.theme)

        self.left_margin = 5

    def draw(self, screen):
        y = 4
        for line in self.lines:
            if line.dirty:
                line.make_texture()
            screen.blit(line.texture, (self.left_margin, y))
            y += self.theme.text_size()

        self.cursor.draw(screen)

    def update(self):
        self.cursor.update(self)

    def get_current_line(self):
        if self.cursor.line < len(self.lines):
            return self.lines[self.cursor.line]

    def insert_line(self, at, initial_content):
        self.lines.insert(at, Line(self.font, self.theme, initial_content))

    def remove_line(self, line_index, keep_content=True):
        """Removes a line, optionally appending its content to the line above
        Will not remove the 0th line if it has content
        """
        if keep_content and line_index > 0:
            self.lines[line_index - 1].append_text(self.lines[line_index].content)

        if line_index == 0 and len(self.lines[line_index].content) > 0:
            return False
        else:
            del self.lines[line_index]
            return True


class Line:
    def __init__(self, font, theme, initial_content=None):
        if initial_content is None:
            initial_content = []
        self.content = initial_content
        self.font = font
        self.theme = theme
        self.dirty = False
        self.texture = None
        self.make_texture()

    def truncate(self, truncate_from):
        ret = self.content[truncate_from:]
        self.content = self.content[:truncate_from]
        return ret

    def add_text(self, insert_at, text):
        """Add text anywhere in a line"""
        self.content.insert(insert_at, text)
        self.dirty = True
        return len(text)

    def append_text(self, text):
        """Add text to the end of a line"""
        self.add_text(len(self.content), text)

    def remove_at(self, index):
        index = clamp(index, 0, len(self.content) - 1)
        removed = self.content[index]
        del self.content[index]
        return removed

    def width_to_column(self, column):
        # if column > len content it is just fine
        return self.font.size("".join(self.content[:column]))[0]

    def set_content(self, new_content):
        self.dirty = True
        self.content = new_content

    def make_texture(self):
        self.texture = self.font.render(
            "".join(self.content), True, self.theme.text_colour()
        )
