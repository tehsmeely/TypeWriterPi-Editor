from __future__ import annotations
from enum import Enum
from collections import deque
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from document import Document

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

    def __repr__(self):
        return "Action({},{})".format(self.action_type, self.action_data)


class ActionHandler:
    def __init__(self):
        self.history = deque([], 20)

    def add_action(self, action, document):
        print("Adding Action:", action)
        modified_action_after_apply = apply_action(action, document)
        if modified_action_after_apply is not None:
            self.history.append(modified_action_after_apply)

    def undo(self, document):
        if len(self.history) > 0:
            action = self.history.pop()
            print("undoing: {}".format(action))
            apply_inverse_action(action, document)


def apply_action__text(
    action: Action, document: Document, move_cursor: bool = True
) -> Optional[Action]:
    print("Adding Text")
    line = document.get_current_line()
    if line is not None:
        insert_at = min(len(line.content), document.cursor.column)
        maybe_cursor_move = line.add_text(insert_at, action.action_data)
        if maybe_cursor_move:
            if move_cursor:
                document.cursor.column = insert_at + maybe_cursor_move
            return action
    return None


def apply_action__enter(
    action: Action, document: Document, move_cursor: bool = True
) -> Optional[Action]:
    print("Enter: Newline")
    ## TODO: Delete to right of cursor???
    line = document.get_current_line()
    if line is not None:
        cut_at = min(len(line.content), document.cursor.column)
        print("Newline from line", line.content, "cutting at", cut_at)
        content_to_carry_down = line.truncate(cut_at)
        print("Carrying down to new line: {}", content_to_carry_down)
        document.insert_line(document.cursor.line + 1, content_to_carry_down)
        if move_cursor:
            document.cursor.line += 1
            document.cursor.column = 0
    return action


def apply_action__backspace(action: Action, document: Document) -> Optional[Action]:
    line = document.get_current_line()
    print("Backspace")
    if line is not None:
        if document.cursor.column > 0:
            removed_char = line.remove_at(document.cursor.column - 1)
            document.cursor.column -= 1
            action.action_data = ("DEL", removed_char)
        elif document.cursor.line > 0:
            # cursor line must be > 0 so we cant delete first line
            prev_line = document.get_line(document.cursor.line - 1)
            new_column = document.cursor.column
            if prev_line is not None:
                new_column = len(prev_line.content)
            document.remove_line(document.cursor.line)
            action.action_data = ("LINE", document.cursor.line)
            document.cursor.line -= 1
            document.cursor.column = new_column

    return action


def apply_action__delete(action: Action, document: Document) -> Optional[Action]:
    line = document.get_current_line()
    print("Delete")
    if line is not None:
        if document.cursor.column < len(line.content):
            removed_char = line.remove_at(document.cursor.column)
            action.action_data = ("DEL", removed_char)
        elif document.cursor.line < (len(document.lines) - 1):
            document.remove_line(document.cursor.line + 1)
            action.action_data = ("LINE", document.cursor.line)
    return action


def apply_action__move(action: Action, document: Document) -> Optional[Action]:
    did_move = document.cursor.move(document, action.action_data)
    if not did_move:
        action.action_data = CursorDirection.NO_MOVE
    return action


def apply_action(action: Action, document: Document) -> Optional[Action]:
    # TEXT
    if action.action_type == ActionType.TEXT:
        return apply_action__text(action, document)

    # ENTER
    elif action.action_type == ActionType.ENTER:
        return apply_action__enter(action, document)

    # BACKSPACE
    elif action.action_type == ActionType.BACKSPACE:
        return apply_action__backspace(action, document)

    # DELETE
    elif action.action_type == ActionType.DELETE:
        return apply_action__delete(action, document)

    # MOVE
    elif action.action_type == ActionType.MOVE:
        return apply_action__move(action, document)

    else:
        print("Unknown Action Type: {}", action.action_type)
        return action


def apply_inverse_action(action: Action, document: Document):
    if action.action_type == ActionType.TEXT or action.action_type == ActionType.ENTER:
        apply_action__backspace(action, document)

    elif action.action_type == ActionType.BACKSPACE:
        if action.action_data is not None:
            if action.action_data[0] == "DEL":
                reapply_action = Action(ActionType.TEXT, action.action_data[1])
                apply_action__text(reapply_action, document)
            elif action.action_data[0] == "LINE":
                apply_action__enter(action, document)

    elif action == ActionType.DELETE:
        if action.action_data is not None:
            if action.action_data[0] == "DEL":
                reapply_action = Action(ActionType.TEXT, action.action_data[1])
                apply_action__text(reapply_action, document, move_cursor=False)
            elif action.action_data[0] == "LINE":
                apply_action__enter(action, document, move_cursor=False)

    elif action.action_type == ActionType.MOVE:
        reverse_move = INVERTED_DIRECTIONS.get(action.action_data)
        if reverse_move is not None:
            document.cursor.move(document, reverse_move)
