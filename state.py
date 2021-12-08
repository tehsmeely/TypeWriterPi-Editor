import config, pygame
from file_manager import FileManager, EXTENSION
from themes import theme_from_config
from action import ActionHandler
from document import Document
from menu import MenuRoot
from status_bar import StatusBar
import core.power


class State:
    def __init__(self, screen_dims):
        self.screen_centre = screen_dims[0] / 2, screen_dims[1] / 2
        self.screen_dims = screen_dims
        self.running = True
        self.general_config = config.load_config()
        self.theme = theme_from_config(self.general_config)
        self.status_bar = StatusBar(
            screen_dims[0], (0, screen_dims[1] - 20), self.theme
        )
        self.file_manager = FileManager(self.general_config)
        self.action_handler = ActionHandler()
        self.document = Document(self.theme)
        self.menu = MenuRoot(self)

    def get_display_flags(self):
        if self.general_config["display"]["fullscreen"]:
            return pygame.FULLSCREEN | pygame.NOFRAME
        else:
            return 0

    def update(self):
        self.document.update(cursor_disable=(self.menu.is_open()))
        self.file_manager.update(self.document)
        self._update_status_bar()

    def _update_status_bar(self):
        self.status_bar.set_right(self.document.cursor.to_status_string())
        self.status_bar.set_centre(self.file_manager.to_status_string())

    def draw(self, screen):
        self.document.draw(screen)
        self.menu.draw(screen)
        self.status_bar.draw(screen)

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
