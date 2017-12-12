#!/usr/bin/env python2.7

from time import time

from board import Board
from element import Element, get_possible_movements

from game_events import lines_cleared, level_increased
from game_events import current_lines, current_score, current_level
from game_events import increase_level
from game_events import activate_shaking

from game_exceptions import ColException

from internal_config import BOARD_HEIGHT, BOARD_WIDTH
from internal_config import MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_SMASH, MOVE_ESCAPE
from internal_config import STEP_SECONDS, STEP_CHANGE


class Game(object):
    """

    :param Board board:
    :param bool _take_next:
    :param [Element] _elements:

    """

    def __init__(self):
        self.board = Board.create_board(BOARD_HEIGHT, BOARD_WIDTH)
        # self._to_update = False
        self._take_next = False
        self._y_inc = 0
        self._accumulated_step_time = 0
        self._elements = [Element.get_new_element(), Element.get_new_element()]
        self._last_updated = time()
        self._step_seconds = STEP_SECONDS

        self.score = 0
        self.level = 1
        self.lines = 0

        self._level_score_ranges = [
            (1, 30, STEP_SECONDS),
            (2, 50, STEP_SECONDS - (STEP_SECONDS * STEP_CHANGE)),
            (3, 70, STEP_SECONDS - (STEP_SECONDS * 2 * STEP_CHANGE)),
            (4, 80, STEP_SECONDS - (STEP_SECONDS * 3 * STEP_CHANGE)),
            (5, 90, STEP_SECONDS - (STEP_SECONDS * 4 * STEP_CHANGE)),
        ]

        current_lines.send(lines=self.lines)
        current_score.send(score=self.score)
        current_level.send(level=self.level)

        self._add_listeners()

    def _get_element(self):
        self._elements.append(Element.get_new_element())
        self._elements = self._elements[1:]

    def get_next_element(self):
        """

        :return: Element:

        """
        return self._elements[1]

    def update(self, user_key):
        """

        :param user_key:
        :return:

        """
        start_step = time()

        if self._take_next:
            self._get_element()
            self._take_next = False

        try:
            self.board.can_place_element(self._elements[0])
        except ColException, er:
            self.board.add_element(self._elements[0])
            return False, self.board

        possible_moves = get_possible_movements(self.board, self._elements[0])

        if user_key in possible_moves:
            if user_key == MOVE_UP:
                self._elements[0].rotate()
            elif user_key == MOVE_RIGHT:
                self._elements[0].x += 1
            elif user_key == MOVE_LEFT:
                self._elements[0].x -= 1
            elif user_key == MOVE_DOWN:
                self._elements[0].y += 1
            elif user_key == MOVE_SMASH:
                dy = self.board.get_smashed_position_dy(self._elements[0])
                self._elements[0].y += dy

        possible_moves = get_possible_movements(self.board, self._elements[0])

        if MOVE_DOWN not in possible_moves:
            self.board.add_element(self._elements[0])
            self._take_next = True
            return True, self.board

        self._elements[0].y += self._y_inc

        self._accumulated_step_time += time() - start_step

        if self._accumulated_step_time >= self._step_seconds:
            self._y_inc = 1
            self._accumulated_step_time = 0
        else:
            self._y_inc = 0

        return True, self.board.can_place_element(self._elements[0])

    def _get_score_from_lines(self, lines):
        """

        :param [int] lines:
        :return:
        """
        score = 0

        for i in lines:
            score += BOARD_HEIGHT - i

        if len(lines) == 4:
            score += 10

        return score

    def _update_lines(self, *args, **kwargs):
        lines = kwargs['lines']

        if len(lines) == 4:
            activate_shaking.send()

        self.lines += len(kwargs['lines'])
        self.score += self._get_score_from_lines(lines)

        self._update_level()

        current_lines.send(lines=self.lines)
        current_score.send(score=self.score)

    def _update_level(self):
        # lvl = None
        # step_second = None

        for lvl, score, step_second in self._level_score_ranges:
            if self.score < score:
                self.level = lvl
                self._step_seconds = step_second
                current_level.send(level=self.level)
                return

        self.level = len(self._level_score_ranges)
        self._step_seconds = 0.05
        current_level.send(level=self.level)


    def _add_listeners(self):
        lines_cleared.connect(self._update_lines)
        increase_level.connect(self._update_level)
