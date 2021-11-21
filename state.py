import config, pygame
from file_manager import FileManager, EXTENSION
from themes import theme_from_config
from action import ActionHandler
from document import Document
from core.ui import Menu
from core.utils import *


class State:
    def __init__(self, screen_centre):
        self.running = True
        self.general_config = config.load_config()
        self.file_manager = FileManager(self.general_config)
        self.theme = theme_from_config(self.general_config)
        self.action_handler = ActionHandler()
        self.document = Document(self.theme)
        self.menu = None
        self.screen_centre = screen_centre

    def get_display_flags(self):
        if self.general_config["display"]["fullscreen"]:
            return pygame.FULLSCREEN | pygame.NOFRAME
        else:
            return 0

    def update(self):
        self.document.update(cursor_disable=(self.menu is not None))
        self.file_manager.update(self.document)

    def stop(self):
        print("Stopping")
        self.running = False

    def close_menu(self):
        print("Closing Menu")
        self.menu = None

    def execute_menu(self, close_after=False):
        self.menu.execute()
        if close_after:
            self.menu = None

    def load(self):
        files = self.file_manager.find_files()
        print(files)
        max_files = 8
        if len(files) > max_files:
            files = files[:max_files]
        file_options = [
            (
                file.removesuffix(EXTENSION),
                Curry(self.file_manager.load_file, file, self.document),
            )
            for file in files
        ]
        self.menu = Menu(file_options, self.theme, self.screen_centre)
        print("Saving")
