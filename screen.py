# -*- coding: utf8 -*-

import pygame
from pygame.colordict import THECOLORS

from element import ELEMENTS_IDS, ELEMENTS_COLORS

from internal_config import SCREEN_HEIGHT, SCREEN_WIDTH
from internal_config import BOARD_OFFSET
from internal_config import ELEMENT_BLANK, ELEMENT_FILL
from internal_config import BACKGROUND_FILL, BACKGROUND_COLOR
from internal_config import NXT_E_BLOCK_SIZE, NXT_E_BOX_OFFSET, NXT_E_BOX_SIZE
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
        self._screen.fill(COLOR_GRAY1)

        # if self._to_shake:
        #     try:
        #         self._board_offset = self._shaker.next()
        #     except StopIteration:
        #         self._to_shake = False

        self._draw_board()
        self._draw_next_element()

        pygame.display.update()

    def _draw_board(self):
        raw_board = self._board.get_raw()

        for i, row in enumerate(raw_board):
            for j, cell in enumerate(row):
                if cell == BACKGROUND_FILL:
                    c = BACKGROUND_COLOR
                elif cell in ELEMENTS_IDS:
                    c = pygame.colordict.THECOLORS[ELEMENTS_COLORS[cell]]
                else:
                    c = COLOR_WHITE

                r = pygame.Rect(self._board_offset.x + j * BLOCK_SIZE,
                                self._board_offset.y + i * BLOCK_SIZE,
                                BLOCK_SIZE,
                                BLOCK_SIZE)

                pygame.draw.rect(self._screen, c, r, 0)

    def _draw_next_element(self):
        r = pygame.Rect(NXT_E_BOX_OFFSET.x,
                        NXT_E_BOX_OFFSET.y,
                        NXT_E_BOX_SIZE.x,
                        NXT_E_BOX_SIZE.y)
        pygame.draw.rect(self._screen, COLOR_BLACK, r, 0)

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

