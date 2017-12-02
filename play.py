#!/usr/bin/env python2.7
# -*- coding: utf8 -*-

import sys

import pygame

from game import Game
from screen import Screen

from internal_config import STATE_NEW_GAME, STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER
from internal_config import MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_ESCAPE, MOVE_SMASH

key_pressed = lambda e, k: e.type == pygame.KEYDOWN and e.key == k


def pg_get_input():
    key = None

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
        elif key_pressed(event, pygame.K_UP):
            # print 'UP'
            key = MOVE_UP
        elif key_pressed(event, pygame.K_DOWN):
            # print 'DOWN'
            key = MOVE_DOWN
        elif key_pressed(event, pygame.K_LEFT):
            # print 'LEFT'
            key = MOVE_LEFT
        elif key_pressed(event, pygame.K_RIGHT):
            # print 'RIGHT'
            key = MOVE_RIGHT
        elif key_pressed(event, pygame.K_ESCAPE):
            key = MOVE_ESCAPE
        elif key_pressed(event, pygame.K_RETURN):
            key = MOVE_SMASH

    return key

if __name__ == '__main__':

    from random import randrange
    from time import time, sleep

    pygame.init()

    pygame.font.init()
    font = pygame.font.SysFont("", 20)

    game = Game()
    clock = pygame.time.Clock()

    state = STATE_NEW_GAME

    screen = Screen()

    while True:

        user_key = pg_get_input()

        if user_key == MOVE_ESCAPE:
            print 'GAME OVER'
            break

        if user_key == MOVE_SMASH:
            screen.activate_shaking()

        runnable, board = game.update(user_key)

        if runnable is False:
            print 'GAME OVER'
            break

        screen.set_next_element(game.get_next_element())
        screen.set_board(board)
        screen.draw()

        clock.tick(60)
