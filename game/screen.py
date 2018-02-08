# -*- coding: utf8 -*-
"""

Screen is used for drawing screens and elements for each game state.

"""
import pygame

from pygame.colordict import THECOLORS

from element import ELEMENTS_IDS

from game.config import ELEMENTS_COLORS
from game.config import SCREEN_HEIGHT, SCREEN_WIDTH
from game.config import BOARD_OFFSET, BOARD_MATRIX_BORDERS, BOARD_MATRIX_BORDERS_WIDTH, BOARD_MATRIX_BORDERS_COLOR
from game.config import ELEMENT_FILL
from game.config import BACKGROUND_FILL, BACKGROUND_COLOR
from game.config import NXT_E_BLOCK_SIZE, NXT_E_BOX_OFFSET, NXT_E_BOX_SIZE, NXT_E_BCK_COLOR

from game.config import LEVEL_BOX_OFFSET, LEVEL_BOX_SIZE, LEVEL_BOX_BCK_COLOR
from game.config import LINES_BOX_OFFSET, LINES_BOX_SIZE, LINES_BOX_BCK_COLOR
from game.config import SCORE_BOX_OFFSET, SCORE_BOX_SIZE, SCORE_BOX_BCK_COLOR

from game.config import MSG_WELCOME, MSG_USAGE1, MSG_USAGE2, MSG_PAUSED, MSG_UNPAUSE, MSG_GO_HOME, MSG_GAME_OVER
from game.config import LBL_NEXT, LBL_SCORE, LBL_LINES
from game.config import BLOCK_SIZE
from game.config import COLOR_GRAY1, COLOR_WHITE, COLOR_BLACK

from utils.events import current_lines, current_score, current_level, activate_shaking

from game.effects.shaking import Shake


class Screen(object):
    def __init__(self):
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._board = None
        self._next_element = None
        self._board_offset = BOARD_OFFSET
        self._to_shake = False
        self._shaker = Shake(self._board_offset)
        self._lines = 0
        self._score = 0
        self._level = 1

        self._add_listeners()

    def set_board(self, board):
        self._board = board

    def set_next_element(self, element):
        self._next_element = element

    def _activate_shaking(self, *args, **kwargs):
        self._to_shake = True
        self._shaker = Shake(BOARD_OFFSET)

    def draw_home_screen(self):
        self._screen.fill(COLOR_BLACK)

        label_font = pygame.font.SysFont("", 30)

        label = label_font.render(MSG_WELCOME, True, COLOR_WHITE)
        label_rect = label.get_rect()
        label_offset = pygame.Rect((SCREEN_WIDTH - label_rect.width) / 2, (SCREEN_HEIGHT - label_rect.height) / 2,
                                   label_rect.width, label_rect.height)
        self._screen.blit(label, label_offset)

        label_font = pygame.font.SysFont("", 20)

        label = label_font.render(MSG_USAGE1, True, COLOR_WHITE)
        label_rect = label.get_rect()
        label_offset = pygame.Rect((SCREEN_WIDTH - label_rect.width) / 2, (SCREEN_HEIGHT - label_rect.height) / 2 + 20,
                                   label_rect.width, label_rect.height)
        self._screen.blit(label, label_offset)

        label = label_font.render(MSG_USAGE2, True, COLOR_WHITE)
        label_rect = label.get_rect()
        label_offset = pygame.Rect((SCREEN_WIDTH - label_rect.width) / 2, (SCREEN_HEIGHT - label_rect.height) / 2 + 40,
                                   label_rect.width, label_rect.height)
        self._screen.blit(label, label_offset)

    def draw_pause_screen(self):
        tint_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        tint_surface.set_alpha(200)
        tint_surface.fill(COLOR_BLACK)
        self._screen.blit(tint_surface, (0, 0))

        label_font = pygame.font.SysFont("", 30)

        label = label_font.render(MSG_PAUSED, True, COLOR_WHITE)
        label_rect = label.get_rect()
        label_offset = pygame.Rect((SCREEN_WIDTH - label_rect.width) / 2, (SCREEN_HEIGHT - label_rect.height) / 2,
                                   label_rect.width, label_rect.height)
        self._screen.blit(label, label_offset)

        label_font = pygame.font.SysFont("", 20)

        label = label_font.render(MSG_UNPAUSE, True, COLOR_WHITE)
        label_rect = label.get_rect()
        label_offset = pygame.Rect((SCREEN_WIDTH - label_rect.width) / 2, (SCREEN_HEIGHT - label_rect.height) / 2 + 20,
                                   label_rect.width, label_rect.height)
        self._screen.blit(label, label_offset)

    def draw_game_over_screen(self):
        tint_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        tint_surface.set_alpha(200)
        tint_surface.fill(COLOR_BLACK)
        self._screen.blit(tint_surface, (0, 0))

        label_font = pygame.font.SysFont("", 30)

        label = label_font.render(MSG_GAME_OVER, True, COLOR_WHITE)
        label_rect = label.get_rect()
        label_offset = pygame.Rect((SCREEN_WIDTH - label_rect.width) / 2, (SCREEN_HEIGHT - label_rect.height) / 2,
                                   label_rect.width, label_rect.height)
        self._screen.blit(label, label_offset)

        label_font = pygame.font.SysFont("", 20)

        label = label_font.render(MSG_GO_HOME, True, COLOR_WHITE)
        label_rect = label.get_rect()
        label_offset = pygame.Rect((SCREEN_WIDTH - label_rect.width) / 2, (SCREEN_HEIGHT - label_rect.height) / 2 + 20,
                                   label_rect.width, label_rect.height)
        self._screen.blit(label, label_offset)

    def draw_game_play(self):
        self._screen.fill(COLOR_BLACK)

        if self._to_shake:
            try:
                self._board_offset = self._shaker.next()
            except StopIteration:
                self._to_shake = False

        self._draw_board()
        self._draw_next_element_box()
        self._draw_score_box()
        self._draw_lines_box()
        self._draw_level_box()

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

    def _draw_next_element_box(self):
        r = pygame.Rect(NXT_E_BOX_OFFSET.x,
                        NXT_E_BOX_OFFSET.y,
                        NXT_E_BOX_SIZE.x,
                        NXT_E_BOX_SIZE.y)
        pygame.draw.rect(self._screen, NXT_E_BCK_COLOR, r, 0)

        label_font = pygame.font.SysFont("", 20)

        label = label_font.render(LBL_NEXT, True, COLOR_GRAY1)
        label_offset = pygame.Rect(NXT_E_BOX_OFFSET.x, NXT_E_BOX_OFFSET.y, NXT_E_BOX_OFFSET.x, NXT_E_BOX_OFFSET.y)
        self._screen.blit(label, label_offset)

        s = self._next_element.size

        e_offset = (NXT_E_BOX_SIZE - NXT_E_BLOCK_SIZE * s) / 2

        for j, row in enumerate(self._next_element):
            for i, cell in enumerate(row):
                if cell is not ELEMENT_FILL:
                    continue
                r = pygame.Rect(NXT_E_BOX_OFFSET.x + e_offset.x + i * NXT_E_BLOCK_SIZE.x,
                                NXT_E_BOX_OFFSET.y + 10 + e_offset.y + j * NXT_E_BLOCK_SIZE.y,
                                NXT_E_BLOCK_SIZE.x,
                                NXT_E_BLOCK_SIZE.y)
                c = pygame.colordict.THECOLORS[ELEMENTS_COLORS[self._next_element.identifier]]
                pygame.draw.rect(self._screen, c, r, 0)

    def _draw_score_box(self):
        r = pygame.Rect(SCORE_BOX_OFFSET.x, SCORE_BOX_OFFSET.y,
                        SCORE_BOX_SIZE.x, SCORE_BOX_SIZE.y)

        pygame.draw.rect(self._screen, SCORE_BOX_BCK_COLOR, r, 0)

        label_font = pygame.font.SysFont("", 20)
        value_font = pygame.font.SysFont("", 50)

        label = label_font.render(LBL_SCORE, True, COLOR_GRAY1)
        label_offset = pygame.Rect(SCORE_BOX_OFFSET.x, SCORE_BOX_OFFSET.y, SCORE_BOX_SIZE.x, SCORE_BOX_SIZE.y)
        self._screen.blit(label, label_offset)

        value = value_font.render('{}'.format(self._score), True, COLOR_WHITE)
        value_rect = value.get_rect()
        value_text_offset = pygame.Rect(SCORE_BOX_OFFSET.x,
                                        SCORE_BOX_OFFSET.y + (SCORE_BOX_SIZE.y - value_rect.height) / 2,
                                        value_rect.width,
                                        value_rect.height)
        self._screen.blit(value, value_text_offset)

    def _draw_lines_box(self):
        r = pygame.Rect(LINES_BOX_OFFSET.x, LINES_BOX_OFFSET.y,
                        LINES_BOX_SIZE.x, LINES_BOX_SIZE.y)
        pygame.draw.rect(self._screen, LINES_BOX_BCK_COLOR, r, 0)

        label_font = pygame.font.SysFont("", 20)
        value_font = pygame.font.SysFont("", 50)

        label = label_font.render(LBL_LINES, True, COLOR_GRAY1)
        label_offset = pygame.Rect(LINES_BOX_OFFSET.x, LINES_BOX_OFFSET.y, LINES_BOX_SIZE.x, LINES_BOX_SIZE.y)
        self._screen.blit(label, label_offset)

        value = value_font.render('{}'.format(self._lines), True, COLOR_WHITE)
        value_rect = value.get_rect()
        value_text_offset = pygame.Rect(LINES_BOX_OFFSET.x,
                                        LINES_BOX_OFFSET.y + (LINES_BOX_SIZE.y - value_rect.height) / 2,
                                        value_rect.width,
                                        value_rect.height)
        self._screen.blit(value, value_text_offset)

    def _draw_level_box(self):
        r = pygame.Rect(LEVEL_BOX_OFFSET.x, LEVEL_BOX_OFFSET.y,
                        LEVEL_BOX_SIZE.x, LEVEL_BOX_SIZE.y)

        pygame.draw.rect(self._screen, LEVEL_BOX_BCK_COLOR, r, 0)

        label_font = pygame.font.SysFont("", 20)
        value_font = pygame.font.SysFont("", 50)

        label = label_font.render("LEVEL", True, COLOR_GRAY1)
        label_offset = pygame.Rect(LEVEL_BOX_OFFSET.x, LEVEL_BOX_OFFSET.y, LEVEL_BOX_OFFSET.x, LEVEL_BOX_OFFSET.y)
        self._screen.blit(label, label_offset)

        value = value_font.render('{}'.format(self._level), True, COLOR_WHITE)
        value_rect = value.get_rect()
        value_text_offset = pygame.Rect(LEVEL_BOX_OFFSET.x,
                                        LEVEL_BOX_OFFSET.y + (LEVEL_BOX_SIZE.y - value_rect.height) / 2,
                                        value_rect.width,
                                        value_rect.height)
        self._screen.blit(value, value_text_offset)

    def _update_lines(self, *args, **kwargs):
        self._lines = kwargs['lines']

    def _update_score(self, *args, **kwargs):
        self._score = kwargs['score']

    def _update_level(self, *args, **kwargs):
        self._level = kwargs['level']

    def _add_listeners(self):
        current_lines.connect(self._update_lines)
        current_score.connect(self._update_score)
        current_level.connect(self._update_level)
        activate_shaking.connect(self._activate_shaking)
