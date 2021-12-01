import enum

import pygame

from core.utils import *
from core.ui import Menu, OptionCallback
from file_manager import EXTENSION


class MenuType(enum.Enum):
    NONE = 1
    MAIN = 2
    FILE_PICKER = 3
    SYSTEM = 4


class MenuRoot:
    def __init__(self, state):
        self.current_menu_type = MenuType.NONE
        self.state = state

        self.main_menu = _create_main_menu(self.state, self)
        self.file_picker_page, self.file_picker = _create_file_picker(self.state, 0)
        self.system_menu = _create_system_menu(self.state, self)

    def _get_menu(self):
        if self.current_menu_type == MenuType.MAIN:
            return self.main_menu
        elif self.current_menu_type == MenuType.FILE_PICKER:
            return self.file_picker
        elif self.current_menu_type == MenuType.SYSTEM:
            return self.system_menu
        else:
            return None

    def draw(self, screen):
        current_menu = self._get_menu()
        if current_menu is not None:
            current_menu.draw(screen)

    def handle_arrow(self, arrow):
        current_menu = self._get_menu()
        if (
            arrow in [pygame.K_LEFT, pygame.K_RIGHT]
            and self.current_menu_type == MenuType.FILE_PICKER
        ):
            if arrow == pygame.K_LEFT:
                self.file_picker_page -= 1
            else:
                self.file_picker_page += 1
            self.file_picker_page, self.file_picker = _create_file_picker(self.state, 0)
        elif current_menu is not None:
            if arrow == pygame.K_UP:
                current_menu.move(-1)
            elif arrow == pygame.K_DOWN:
                current_menu.move(1)

    def handle_enter(self):
        current_menu = self._get_menu()
        if current_menu is not None:
            print(current_menu.execute())
            if current_menu.should_close_on_execute():
                self.current_menu_type = MenuType.NONE

    def handle_escape(self):
        self.current_menu_type = None

    def close_menu(self):
        self.current_menu_type = MenuType.NONE

    def open_main(self):
        self.current_menu_type = MenuType.MAIN

    def open_file_picker(self):
        self.file_picker_page, self.file_picker = _create_file_picker(self.state, 0)
        self.current_menu_type = MenuType.FILE_PICKER

    def open_system_menu(self):
        self.current_menu_type = MenuType.SYSTEM


def _create_main_menu(state, menu_root):
    return Menu(
        [
            ("RESUME", OptionCallback(Curry(menu_root.close_menu))),
            ("EXIT", OptionCallback(Curry(state.stop))),
            (
                "NEW",
                OptionCallback(Curry(menu_root.open_file_input), close_on_call=False),
            ),
            (
                "LOAD",
                OptionCallback(Curry(menu_root.open_file_picker), close_on_call=False),
            ),
            (
                "SYSTEM",
                OptionCallback(Curry(menu_root.open_system_menu), close_on_call=False),
            ),
        ],
        state.theme,
        state.screen_centre,
    )


def _create_system_menu(state, menu_root):
    return Menu(
        [
            ("RESUME", OptionCallback(Curry(menu_root.close_menu))),
            ("SHUTDOWN", OptionCallback(Curry(state.shutdown))),
            ("RESTART", OptionCallback(Curry(state.restart))),
        ],
        state.theme,
        state.screen_centre,
    )


def _create_file_picker(state, page):
    files = state.file_manager.find_files()
    page_size = 8
    num_chunks, chunks = make_chunks(files, page_size)
    page = clamp(page, 0, num_chunks - 1)
    files = chunks[page]
    file_options = [
        (
            file.removesuffix(EXTENSION),
            OptionCallback(Curry(state.file_manager.load_file, file, state.document)),
        )
        for file in files
    ]
    menu = Menu(file_options, state.theme, state.screen_centre)
    return page, menu
