# -*- coding: utf8 -*-

import pygame
from pygame.colordict import THECOLORS

from element import ELEMENTS_IDS, ELEMENTS_COLORS

from internal_config import SCREEN_HEIGHT, SCREEN_WIDTH
from internal_config import BOARD_OFFSET, BOARD_MATRIX_BORDERS, BOARD_MATRIX_BORDERS_WIDTH, BOARD_MATRIX_BORDERS_COLOR
from internal_config import ELEMENT_BLANK, ELEMENT_FILL
from internal_config import BACKGROUND_FILL, BACKGROUND_COLOR
from internal_config import NXT_E_BLOCK_SIZE, NXT_E_BOX_OFFSET, NXT_E_BOX_SIZE, NXT_E_BCK_COLOR

from internal_config import LEVEL_BOX_OFFSET, LEVEL_BOX_SIZE, LEVEL_BOX_BCK_COLOR
from internal_config import LINES_BOX_OFFSET, LINES_BOX_SIZE, LINES_BOX_BCK_COLOR
from internal_config import SCORE_BOX_OFFSET, SCORE_BOX_SIZE, SCORE_BOX_BCK_COLOR

from internal_config import BLOCK_SIZE
from internal_config import COLOR_GRAY1, COLOR_WHITE, COLOR_BLACK


class Screen(object):

    def __init__(self):
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._board = None
        self._next_element = None
        self._board_offset = BOARD_OFFSET
        self._to_shake = False
        # self._shaker = Shake(self._board_offset)

    def set_board(self, board):
        self._board = board

    def set_next_element(self, element):
        self._next_element = element

    def activate_shaking(self):
        self._to_shake = True
        # self._shaker = Shake(Config.BOARD_OFFSET)

    def draw(self):
        self._screen.fill(COLOR_BLACK)

        # if self._to_shake:
        #     try:
        #         self._board_offset = self._shaker.next()
        #     except StopIteration:
        #         self._to_shake = False

        self._draw_board()
        self._draw_next_element()
        self._draw_scores_box()
        self._draw_lines_box()
        self._draw_level_box()

        pygame.display.update()

    def _draw_board(self):
        raw_board = self._board.get_raw()

        for i, row in enumerate(raw_board):
            for j, cell in enumerate(row):
                if cell == BACKGROUND_FILL and BOARD_MATRIX_BORDERS:
                    c = BOARD_MATRIX_BORDERS_COLOR
                    w = BOARD_MATRIX_BORDERS_WIDTH
                elif cell == BACKGROUND_FILL:
                    c = BACKGROUND_COLOR
                    w = 0
                elif cell in ELEMENTS_IDS:
                    c = pygame.colordict.THECOLORS[ELEMENTS_COLORS[cell]]
                    w = 0
                else:
                    c = COLOR_WHITE
                    w = 0

                r = pygame.Rect(self._board_offset.x + j * BLOCK_SIZE,
                                self._board_offset.y + i * BLOCK_SIZE,
                                BLOCK_SIZE,
                                BLOCK_SIZE)

                pygame.draw.rect(self._screen, c, r, w)

    def _draw_next_element(self):
        r = pygame.Rect(NXT_E_BOX_OFFSET.x,
                        NXT_E_BOX_OFFSET.y,
                        NXT_E_BOX_SIZE.x,
                        NXT_E_BOX_SIZE.y)
        pygame.draw.rect(self._screen, NXT_E_BCK_COLOR, r, 0)

        s = self._next_element.size

        o = (NXT_E_BOX_SIZE - NXT_E_BLOCK_SIZE * s)/2

        e_offset = o

        for j, row in enumerate(self._next_element):
            for i, cell in enumerate(row):
                if cell is not ELEMENT_FILL:
                    continue
                r = pygame.Rect(NXT_E_BOX_OFFSET.x + e_offset.x + i * NXT_E_BLOCK_SIZE.x,
                                NXT_E_BOX_OFFSET.y + e_offset.y + j * NXT_E_BLOCK_SIZE.y,
                                NXT_E_BLOCK_SIZE.x,
                                NXT_E_BLOCK_SIZE.y)
                c = pygame.colordict.THECOLORS[ELEMENTS_COLORS[self._next_element.identifier]]
                pygame.draw.rect(self._screen, c, r, 0)

    def _draw_scores_box(self):
        r = pygame.Rect(SCORE_BOX_OFFSET.x, SCORE_BOX_OFFSET.y,
                        SCORE_BOX_SIZE.x, SCORE_BOX_SIZE.y)

        pygame.draw.rect(self._screen, SCORE_BOX_BCK_COLOR, r, 0)

    def _draw_lines_box(self):
        r = pygame.Rect(LINES_BOX_OFFSET.x, LINES_BOX_OFFSET.y,
                        LINES_BOX_SIZE.x, LINES_BOX_SIZE.y)

        pygame.draw.rect(self._screen, LINES_BOX_BCK_COLOR, r, 0)

    def _draw_level_box(self):
        r = pygame.Rect(LEVEL_BOX_OFFSET.x, LEVEL_BOX_OFFSET.y,
                        LEVEL_BOX_SIZE.x, LEVEL_BOX_SIZE.y)

        pygame.draw.rect(self._screen, LEVEL_BOX_BCK_COLOR, r, 0)
