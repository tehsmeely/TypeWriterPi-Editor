import pygame, sys
from pygame.locals import *

from state import State
from core.ui import Menu
from action import ActionType, Action, CURSOR_DIRECTIONS
from core.utils import *

SCREEN_DIMS = (800, 480)


def main():
    pygame.init()

    target_fps = 60

    clock = pygame.time.Clock()

    state = State(SCREEN_DIMS)
    screen = pygame.display.set_mode(SCREEN_DIMS, flags=state.get_display_flags())
    pygame.display.set_caption("Editor")
    pygame.key.set_repeat(300, 100)

    while state.running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if state.no_menu_open():
                if event.type == TEXTINPUT:
                    action = Action(ActionType.TEXT, event.text)
                    state.action_handler.add_action(action, state.document)
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        action = Action(ActionType.ENTER, None)
                        state.action_handler.add_action(action, state.document)
                    elif event.key in CURSOR_DIRECTIONS.keys():
                        action = Action(ActionType.MOVE, CURSOR_DIRECTIONS[event.key])
                        state.action_handler.add_action(action, state.document)
                    elif event.key == K_BACKSPACE:
                        action = Action(ActionType.BACKSPACE, None)
                        state.action_handler.add_action(action, state.document)
                    elif event.key == K_DELETE:
                        action = Action(ActionType.DELETE, None)
                        state.action_handler.add_action(action, state.document)
                    elif event.key == K_z:
                        if KMOD_CTRL & pygame.key.get_mods():
                            state.action_handler.undo(state.document)
            else:
                if event.type == TEXTINPUT:
                    state.menu.handle_text(event.text)
                elif event.type == KEYDOWN:
                    if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                        state.menu.handle_arrow(event.key)
                    elif event.key == K_RETURN:
                        state.menu.handle_enter()
                    elif event.key == K_ESCAPE:
                        state.menu.handle_escape()
                    elif event.key == K_BACKSPACE:
                        state.menu.handle_backspace()

            if event.type == KEYDOWN:
                if event.key == K_F1:
                    print(state.document)
                    print(state.document.lines)
                    for line in state.document.lines:
                        print(line)
                        print(line.content)
                elif event.key == K_F2:
                    print(state.action_handler)
                    for event in state.action_handler.history:
                        print(event)
                elif event.key == K_F3:
                    print(state.document.cursor)
                elif event.key == K_F4:
                    state.menu.open_main()
                elif event.key == K_F5:
                    res = pygame.display.toggle_fullscreen()
                    print("Toggled Fullscreen: {}".format(res))

        screen.fill(state.theme.background_colour())

        state.update()
        state.draw(screen)

        pygame.display.update()
        clock.tick(target_fps)


if __name__ == "__main__":
    main()
