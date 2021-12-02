import pygame, sys
from pygame.locals import *

from state import State
from core.ui import Menu
from action import ActionType, Action, CURSOR_DIRECTIONS
from core.utils import *

SCREEN_DIMS = (800, 400)


def main():
    pygame.init()

    screen_centre = SCREEN_DIMS[0] / 2, SCREEN_DIMS[1] / 2

    target_fps = 60

    clock = pygame.time.Clock()

    state = State(screen_centre)
    screen = pygame.display.set_mode(SCREEN_DIMS, flags=state.get_display_flags())
    pygame.display.set_caption("Editor")

    while state.running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if state.no_menu_open():
                if event.type == TEXTINPUT:
                    action = Action(ActionType.TEXT, event.text)
                    state.action_handler.add_action(action, state.document)
                    print("Done Text Input: ", event.text)
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        action = Action(ActionType.ENTER, None)
                        state.action_handler.add_action(action, state.document)
                        print("Done Return")
                    elif event.key in CURSOR_DIRECTIONS.keys():
                        action = Action(ActionType.MOVE, CURSOR_DIRECTIONS[event.key])
                        state.action_handler.add_action(action, state.document)
                        print("Done Move", CURSOR_DIRECTIONS[event.key])
                    elif event.key == K_BACKSPACE:
                        action = Action(ActionType.BACKSPACE, None)
                        state.action_handler.add_action(action, state.document)
                        print("Done Backspace")
                    elif event.key == K_DELETE:
                        action = Action(ActionType.DELETE, None)
                        state.action_handler.add_action(action, state.document)
                        print("Done Delete")
                    elif event.key == K_z:
                        if KMOD_CTRL & pygame.key.get_mods():
                            state.action_handler.undo(state.document)
                            print("Done Undo!")
            else:
                if event.type == KEYDOWN:
                    if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                        state.menu.handle_arrow(event.key)
                    elif event.key == K_RETURN:
                        state.menu.handle_enter()
                    elif event.key == K_ESCAPE:
                        state.menu.handle_escape()

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
        state.document.draw(screen)

        state.menu.draw(screen)

        pygame.display.update()
        clock.tick(target_fps)


if __name__ == "__main__":
    main()
