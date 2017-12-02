#!/usr/bin/env python2.7
# -*- coding: utf8 -*-

import sys

import pygame

from game import Game
from screen import Screen

from internal_config import TITLE, ICON
from internal_config import STATE_NEW_GAME, STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER
from internal_config import MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_ESCAPE, MOVE_SMASH

from game_events import increase_level

key_pressed = lambda e, k: e.type == pygame.KEYDOWN and e.key == k


def pg_get_input():
    key = None

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.USEREVENT + 1:
            increase_level.send(level=1)
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

    return key

if __name__ == '__main__':

    pygame.init()
    pygame.font.init()

    pygame.display.set_caption(TITLE)
    icon = pygame.image.load(ICON)
    pygame.display.set_icon(icon)

    level_increaser = pygame.time.set_timer(pygame.USEREVENT + 1, 20000)

    screen = Screen()

    game = Game()
    clock = pygame.time.Clock()

    state = STATE_NEW_GAME

    while True:

        user_key = pg_get_input()

        if user_key == MOVE_ESCAPE:
            print 'GAME OVER'
            break

        runnable, board = game.update(user_key)

        if runnable is False:
            print 'GAME OVER'
            break

        screen.set_next_element(game.get_next_element())
        screen.set_board(board)
        screen.draw()

        clock.tick(60)
