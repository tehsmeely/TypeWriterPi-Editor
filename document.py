from cursor import Cursor
from core.utils import *


class Document:
    def __init__(self, theme):
        self.theme = theme
        self.lines = [Line(theme)]
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

    def update(self, cursor_disable=False):
        self.cursor.update(self, cursor_disable)

    def get_line(self, index):
        if 0 <= index < len(self.lines):
            return self.lines[index]

    def get_current_line(self):
        return self.get_line(self.cursor.line)

    def insert_line(self, at, initial_content):
        self.lines.insert(at, Line(self.theme, initial_content))

    def append_line(self, initial_content):
        self.insert_line(len(self.lines), initial_content)

    def remove_line(self, line_index, keep_content=True):
        """Removes a line, optionally appending its content to the line above
        Will not remove the 0th line if it has content
        """
        if keep_content and line_index > 0:
            self.lines[line_index - 1].append_content(self.lines[line_index].content)

        if line_index == 0 and len(self.lines[line_index].content) > 0:
            return False
        else:
            del self.lines[line_index]
            return True

    def to_content_iter(self):
        return ("".join(line.content) for line in self.lines)

    def clear(self, hard=False):
        if hard:
            self.lines = []
        else:
            self.lines = [Line(self.theme)]
        self.cursor.line = 0
        self.cursor.column = 0


class Line:
    def __init__(self, theme, initial_content=None):
        if initial_content is None:
            initial_content = []
        self.content = initial_content
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
        print("Add text, {}->{}".format(text, insert_at))
        if isinstance(text, str) and len(text) == 1:
            self.content.insert(insert_at, text)
            self.dirty = True
            return len(text)
        else:
            raise ValueError("[add_text] only takes len 1 string")

    def append_content(self, text):
        """Add content to the end of a line"""
        self.content.extend(text)
        self.dirty = True

    def remove_at(self, index):
        index = clamp(index, 0, len(self.content) - 1)
        removed = self.content[index]
        del self.content[index]
        self.dirty = True
        return removed

    def width_to_column(self, column):
        # if column > len content it is just fine
        return self.theme.font().size("".join(self.content[:column]))[0]

    def set_content(self, new_content):
        self.dirty = True
        self.content = new_content

    def make_texture(self):
        self.texture = self.theme.font().render(
            "".join(self.content), True, self.theme.text_colour()
        )
