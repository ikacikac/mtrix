# -*- coding: utf8 -*-

import os

from utils import Vect2D

PROJ_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MEDIA_PATH = os.path.join(PROJ_PATH, 'media')

# COLORS

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GRAY1 = (200, 200, 200)
COLOR_GRAY2 = (30, 30, 30)
COLOR_RAND1 = (0, 200, 200)

# ELEMENT CONFIG

NEW_ELEMENT_X = 3
NEW_ELEMENT_Y = 0

ELEMENT_FILL = 'E'
ELEMENT_BLANK = ' '

BLOCK_SIZE = 25  # pixels

ELEMENTS_COLORS = {
    '1': 'red',
    '2': 'blue',
    '3': 'yellow',
    '4': 'green',
    '5': 'gray',
    '6': 'orange',
    '7': 'white'
}

# SCREEN CONFIG

SCREEN_WIDTH = 488  # pixels
SCREEN_HEIGHT = 600  # pixels

BOARD_OFFSET = Vect2D(50, 50)

NXT_E_BOX_OFFSET = Vect2D(350, 50)
NXT_E_BOX_SIZE = Vect2D(87.5, 87.5)
NXT_E_BLOCK_SIZE = Vect2D(15, 15)
NXT_E_BCK_COLOR = COLOR_BLACK

SCORE_BOX_OFFSET = Vect2D(350, 187.5)
SCORE_BOX_SIZE = Vect2D(87.5, 87.5)
SCORE_BOX_BCK_COLOR = COLOR_BLACK

LINES_BOX_OFFSET = Vect2D(350, 325)
LINES_BOX_SIZE = Vect2D(87.5, 87.5)
LINES_BOX_BCK_COLOR = COLOR_BLACK

LEVEL_BOX_OFFSET = Vect2D(350, 462.5)
LEVEL_BOX_SIZE = Vect2D(87.5, 87.5)
LEVEL_BOX_BCK_COLOR = COLOR_BLACK

# BOARD CONFIG

WALL_LEFT = 'L'
WALL_RIGHT = 'R'
FLOOR = 'F'
BACKGROUND_FILL = '_'
BACKGROUND_COLOR = COLOR_BLACK

BOARD_HEIGHT = 20
BOARD_WIDTH = 10

BOARD_MATRIX_BORDERS = True
BOARD_MATRIX_BORDERS_COLOR = COLOR_GRAY2
BOARD_MATRIX_BORDERS_WIDTH = 1


# GAME

TITLE = 'MTRIX'
ICON = MEDIA_PATH + '/game.png'

MSG_WELCOME = "Welcome to MTRIX"
MSG_USAGE1 = "Play/Pause (P)"
MSG_USAGE2 = "Quit (ESC)"
MSG_PAUSED = "PAUSED"
MSG_UNPAUSE = "UNPAUSE (P)"
MSG_GAME_OVER = "GAME OVER"
MSG_GO_HOME = "Home Screen (P)"

LBL_NEXT = "NEXT"
LBL_SCORE = "SCORE"
LBL_LINES = "LINES"

MOVE_LEFT = 1
MOVE_UP = 2
MOVE_RIGHT = 3
MOVE_DOWN = 4
MOVE_ESCAPE = 5
MOVE_SMASH = 6
MOVE_ENTER = 6
MOVE_PAUSE = 7

STEP_SECONDS = 0.1
STEP_CHANGE = 0.1  # should be < 1