#!/usr/bin/env python2.7
# -*- coding: utf8 -*-

import os
import pygame

from game.config import TITLE, ICON

from game.states import GameStateManager
from game.states import HomeScreenState

if __name__ == '__main__':

    # center window
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    pygame.font.init()

    pygame.display.set_caption(TITLE)
    icon = pygame.image.load(ICON)
    pygame.display.set_icon(icon)

    # enable key to be held
    pygame.key.set_repeat(200, 50)

    # set initial screen and run game
    gsm = GameStateManager(start_state=HomeScreenState())
    gsm.run()

    pygame.quit()
