#!/usr/bin/env python2.7

from time import time

from board import Board
from element import Element, get_possible_movements

from game_exceptions import ColException

from internal_config import BOARD_HEIGHT, BOARD_WIDTH
from internal_config import MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_SMASH, MOVE_ESCAPE
from internal_config import STEP_SECONDS


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
            return False, None

        possible_moves = get_possible_movements(self.board, self._elements[0])

        # print possible_moves

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

        if self._accumulated_step_time >= STEP_SECONDS:
            self._y_inc = 1
            self._accumulated_step_time = 0
        else:
            self._y_inc = 0

        return True, self.board.can_place_element(self._elements[0])

