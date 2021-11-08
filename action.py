from enum import Enum
from collections import deque

import pygame.locals

HISTORY_SIZE = 20


class CursorDirection(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    NO_MOVE = 5


CURSOR_DIRECTIONS = {
    pygame.locals.K_UP: CursorDirection.UP,
    pygame.locals.K_RIGHT: CursorDirection.RIGHT,
    pygame.locals.K_DOWN: CursorDirection.DOWN,
    pygame.locals.K_LEFT: CursorDirection.LEFT,
}

INVERTED_DIRECTIONS = {
    CursorDirection.DOWN: CursorDirection.UP,
    CursorDirection.LEFT: CursorDirection.RIGHT,
    CursorDirection.UP: CursorDirection.DOWN,
    CursorDirection.RIGHT: CursorDirection.LEFT,
}


class ActionType(Enum):
    TEXT = 1
    ENTER = 2
    BACKSPACE = 3
    DELETE = 4
    MOVE = 5


class Action:
    def __init__(self, action_type, action_data):
        self.action_type = action_type
        self.action_data = action_data


class ActionHandler:
    def __init__(self):
        self.history = deque([], 20)

    def add_action(self, action, document):
        print("Adding Action:", action)
        modified_action_after_apply = apply_action(action, document)
        self.history.append(modified_action_after_apply)

    def undo(self, document):
        if len(self.history) > 0:
            apply_inverse_action(self.history.pop(), document)


def apply_action(action, document):
    #
    # TEXT
    #
    if action.action_type == ActionType.TEXT:
        print("Adding Text")
        line = document.get_current_line()
        if line is not None:
            insert_at = min(len(line.content), document.cursor.column)
            cursor_move = line.add_text(insert_at, action.action_data)
            document.cursor.column = insert_at + cursor_move

    #
    # ENTER
    #
    elif action.action_type == ActionType.ENTER:
        line = document.get_current_line()
        if line is not None:
            cut_at = min(len(line.content), document.cursor.column)
            print("Newline from line", line.content, "cutting at", cut_at)
            content_to_carry_down = line.truncate(cut_at)
            document.cursor.line += 1
            document.cursor.column = 0
            document.insert_line(document.cursor.line, content_to_carry_down)

    #
    # BACKSPACE
    #
    elif action.action_type == ActionType.BACKSPACE:
        line = document.get_current_line()
        if line is not None:
            if document.cursor.column > 0:
                removed_char = line.remove_at(document.cursor.column - 1)
                document.cursor.column -= 1
                action.action_data = ("DEL", removed_char)
            elif document.cursor.line > 0:
                document.remove_line(document.cursor.line)
                action.action_data = ("LINE", document.cursor.line)
                document.cursor.line -= 1

    #
    # DELETE
    #
    elif action.action_type == ActionType.DELETE:
        line = document.get_current_line()
        if line is not None:
            if document.cursor.column < len(line.content):
                removed_char = line.remove_at(document.cursor.column)
                action.action_data = ("DEL", removed_char)
            elif document.cursor.line < len(document.lines - 1):
                document.remove_line(document.cursor.line + 1)
                action.action_data = ("LINE", document.cursor.line)
    #
    # MOVE
    #
    elif action.action_type == ActionType.MOVE:
        did_move = document.cursor.move(document, action.action_data)
        if not did_move:
            action.action_data = CursorDirection.NO_MOVE

    return action


def apply_inverse_action(action, document):
    if action == ActionType.TEXT:
        pass
    elif action == ActionType.ENTER:
        pass
    elif action == ActionType.BACKSPACE:
        pass
    elif action == ActionType.DELETE:
        pass
    elif action.action_type == ActionType.MOVE:
        reverse_move = INVERTED_DIRECTIONS.get(action.action_data)
        if reverse_move is not None:
            document.cursor.move(document, reverse_move)
