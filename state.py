import config, pygame
from file_manager import FileManager, EXTENSION
from themes import theme_from_config
from action import ActionHandler
from document import Document
from menu import MenuRoot
import core.power


class State:
    def __init__(self, screen_centre):
        self.screen_centre = screen_centre
        self.running = True
        self.general_config = config.load_config()
        self.file_manager = FileManager(self.general_config)
        self.theme = theme_from_config(self.general_config)
        self.action_handler = ActionHandler()
        self.document = Document(self.theme)
        self.menu = MenuRoot(self)

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

    def no_menu_open(self):
        return not self.menu.is_open()

    def _power_control_enabled(self):
        return self.general_config["system"]["power_control_enabled"]

    def shutdown(self):
        if self._power_control_enabled():
            core.power.shutdown()
        else:
            print("Would SHUTDOWN, but not enabled")

    def restart(self):
        if self._power_control_enabled():
            core.power.shutdown()
        else:
            print("Would SHUTDOWN, but not enabled")
