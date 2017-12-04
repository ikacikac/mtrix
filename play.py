#!/usr/bin/env python2.7
# -*- coding: utf8 -*-

import sys

import pygame

from game import Game
from screen import Screen

from internal_config import TITLE, ICON
from internal_config import MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_ESCAPE, MOVE_SMASH, MOVE_PAUSE

from game_states import GameState, HomeState, PauseState, PlayState, GameOverState, HaltState

key_pressed = lambda e, k: e.type == pygame.KEYDOWN and e.key == k


def pg_get_input():
    key = None

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
        elif key_pressed(event, pygame.K_UP):
            key = MOVE_UP
        elif key_pressed(event, pygame.K_DOWN):
            key = MOVE_DOWN
        elif key_pressed(event, pygame.K_LEFT):
            key = MOVE_LEFT
        elif key_pressed(event, pygame.K_RIGHT):
            key = MOVE_RIGHT
        elif key_pressed(event, pygame.K_ESCAPE):
            key = MOVE_ESCAPE
        elif key_pressed(event, pygame.K_RETURN):
            key = MOVE_SMASH
        elif key_pressed(event, pygame.K_p):
            key = MOVE_PAUSE

    return key

if __name__ == '__main__':

    pygame.init()
    pygame.font.init()

    pygame.display.set_caption(TITLE)
    icon = pygame.image.load(ICON)
    pygame.display.set_icon(icon)

    pygame.key.set_repeat(200, 50)

    screen = Screen()

    game = Game()
    clock = pygame.time.Clock()

    game_state_machine = GameState()

    new_game_state = None
    old_game_state = game_state_machine.current_state

    while True:
        user_key = pg_get_input()

        new_game_state = game_state_machine.get_next_state(user_key)

        if isinstance(new_game_state, HomeState):
            if new_game_state != old_game_state:
                game = Game()
            screen.draw_home_screen()

        elif isinstance(new_game_state, PlayState):
            runnable, board = game.update(user_key)

            if runnable is False:
                game_state_machine.go_to_game_over()

            screen.set_next_element(game.get_next_element())
            screen.set_board(board)
            screen.draw_game_play()

        elif isinstance(new_game_state, PauseState):
            screen.draw_pause_screen()

        elif isinstance(new_game_state, GameOverState):
            screen.draw_game_over_screen()

        elif isinstance(new_game_state, HaltState):
            break

        clock.tick(60)
