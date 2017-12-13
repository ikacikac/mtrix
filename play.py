#!/usr/bin/env python2.7
# -*- coding: utf8 -*-

import os
import pygame

from internal_config import TITLE, ICON
from game_states import *

if __name__ == '__main__':

    os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    pygame.font.init()

    pygame.display.set_caption(TITLE)
    icon = pygame.image.load(ICON)
    pygame.display.set_icon(icon)

    pygame.key.set_repeat(200, 50)

    gsm = GameStateManager(start_state=HomeScreenState())
    gsm.run()

    pygame.quit()
