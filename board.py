# -*- cofing: utf8 -*-


from copy import deepcopy
from blinker import signal

from game_events import lines_cleared

from game_exceptions import *

from element import Element

from internal_config import WALL_LEFT, WALL_RIGHT, FLOOR, BACKGROUND_FILL
from internal_config import ELEMENT_FILL, ELEMENT_BLANK
from internal_config import BOARD_HEIGHT, BOARD_WIDTH


class Board(object):
    def __init__(self, height, width, matrix):
        self.height = height
        self.width = width
        self._board = matrix

    def can_place_element(self, element):
        """

        :param Element element:
        :return: bool
        """
        board = deepcopy(self)

        for y in range(element.size):
            for x in range(element.size):
                if element[y][x] == ELEMENT_BLANK:
                    continue
                if board[y + element.y][x + element.x] == WALL_LEFT:
                    raise LeftException()
                if board[y + element.y][x + element.x] == WALL_RIGHT:
                    raise RightException()
                if board[y + element.y][x + element.x] == FLOOR:
                    raise DownException()
                if board[y + element.y][x + element.x] != BACKGROUND_FILL:
                    raise ColException("{} is not {}, {}, {}".format(board[y + element.y][x + element.x],
                                                                     BACKGROUND_FILL, x, y))
                board[y + element.y][x + element.x] = element.identifier

        return board

    def get_smashed_position_dy(self, element):
        """

        :param Element element:
        :return:
        """
        y = 0

        e = deepcopy(element)

        while True:
            try:
                e.y += 1
                self.can_place_element(e)
                y += 1
            except MovementException:
                return y

    def try_to_clear(self):
        raw = self.get_raw()

        filled_rows = []

        for i, r in enumerate(raw):
            if BACKGROUND_FILL not in r:
                filled_rows.insert(0, i)

        if len(filled_rows) == 0:
            return False

        for fr in filled_rows:
            del self._board[fr]

        get_new_row = lambda: [WALL_LEFT] + [BACKGROUND_FILL] * BOARD_WIDTH + [WALL_RIGHT]

        [self._board.insert(0, get_new_row()) for i in range(len(filled_rows))]

        self._board[-1] = [FLOOR] * (BOARD_WIDTH + 2)

        self._board = self._board[:BOARD_HEIGHT + 1]

        lines_cleared.send(lines=len(filled_rows))

    def add_element(self, element):
        """

        :param Element element:
        :return:
        """
        for y in range(element.size):
            for x in range(element.size):
                if element[y][x] == ELEMENT_BLANK:
                    continue
                # if self._board[y + element.y][x + element.x]:
                #     raise Exception()
                self._board[y + element.y][x + element.x] = element.identifier

        self.try_to_clear()

    def print_board(self):
        print self

    def get_raw(self):
        return [[i for i in b[1:-1]] for b in self._board[:-1]]

    def get_raw_walls(self):
        return deepcopy(self._board)

    @classmethod
    def create_board(cls, height, width):
        matrix = []
        for y in range(height):
            row = list()
            row.append(WALL_LEFT)
            for x in range(width):
                row.append(BACKGROUND_FILL)
            row.append(WALL_RIGHT)
            matrix.append(row)
        matrix.append(FLOOR * (width + 2))
        return cls(height, width, matrix=matrix)

    def __getitem__(self, item):
        return self._board[item]

    def __str__(self):
        res = '\n'
        return res + '\n'.join([' '.join([str(i) for i in b]) for b in self._board])


if __name__ == '__main__':

    board = Board.create_board(BOARD_HEIGHT, BOARD_WIDTH)
    print board