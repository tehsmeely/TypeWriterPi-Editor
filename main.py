import pygame, sys
from pygame.locals import *

import themes, document
from action import ActionType, Action, ActionHandler, CURSOR_DIRECTIONS

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

SCREEN_DIMS = (800, 400)

target_fps = 60

clock = pygame.time.Clock()

screen = pygame.display.set_mode(SCREEN_DIMS)
pygame.display.set_caption("Editor")

all_sprites = []

theme = themes.Default()
action_handler = ActionHandler()
document = document.Document(theme)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == TEXTINPUT:
            action = Action(ActionType.TEXT, event.text)
            action_handler.add_action(action, document)
            print("Text Input: ", event.text)
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                action = Action(ActionType.ENTER, None)
                action_handler.add_action(action, document)
                print("Return")
            elif event.key in CURSOR_DIRECTIONS.keys():
                action = Action(ActionType.MOVE, CURSOR_DIRECTIONS[event.key])
                action_handler.add_action(action, document)
                print("Move", CURSOR_DIRECTIONS[event.key])
            elif event.key == K_BACKSPACE:
                action = Action(ActionType.BACKSPACE, None)
                action_handler.add_action(action, document)
                print("Backspace")
            elif event.key == K_DELETE:
                action = Action(ActionType.DELETE, None)
                action_handler.add_action(action, document)
                print("Delete")
            elif event.key == K_F1:
                print(document)
                print(document.lines)
                for line in document.lines:
                    print(line)
                    print(line.content)

    screen.fill(theme.background_colour())

    document.update()
    document.draw(screen)

    pygame.display.update()
    clock.tick(target_fps)
