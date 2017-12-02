# -*- coding: utf8 -*-

from copy import deepcopy
from random import randrange

from internal_config import NEW_ELEMENT_X, NEW_ELEMENT_Y
from internal_config import ELEMENT_BLANK, ELEMENT_FILL
from internal_config import MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_ESCAPE, MOVE_SMASH

from game_exceptions import MovementException

e1 = [' E ', 'EEE', '   ']
e2 = ['  E', 'EEE', '   ']
e3 = ['E  ', 'EEE', '   ']
e4 = ['EE', 'EE']
e5 = [' E  ', ' E  ', ' E  ', ' E  ']
e6 = [' EE', 'EE ', '   ']
e7 = ['EE ', ' EE', '   ']

elements = [e1, e2, e3, e4, e5, e6, e7]

ELEMENTS_IDS = ['1', '2', '3', '4', '5', '6', '7']

ELEMENTS_COLORS = {
    '1': 'red',
    '2': 'blue',
    '3': 'yellow',
    '4': 'green',
    '5': 'gray',
    '6': 'orange',
    '7': 'white'
}

raw_elements = zip(ELEMENTS_IDS, elements)


def get_possible_movements(board, element):
    """

    :param Board board:
    :param Element element:
    :return:

    """

    # TODO Without deep copies, totally unnecessary

    e_l = deepcopy(element)
    e_l.x -= 1

    e_r = deepcopy(element)
    e_r.x += 1

    e_o = deepcopy(element)
    e_o.rotate()

    e_d = deepcopy(element)
    e_d.y += 1

    possible_moves = [MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN, MOVE_SMASH]

    try:
        board.can_place_element(e_l)
    except MovementException:
        possible_moves.pop(possible_moves.index(MOVE_LEFT))

    try:
        board.can_place_element(e_r)
    except MovementException:
        possible_moves.pop(possible_moves.index(MOVE_RIGHT))

    try:
        board.can_place_element(e_o)
    except MovementException:
        possible_moves.pop(possible_moves.index(MOVE_UP))

    try:
        board.can_place_element(e_d)
    except MovementException:
        possible_moves.pop(possible_moves.index(MOVE_DOWN))
        possible_moves.pop(possible_moves.index(MOVE_SMASH))

    return possible_moves


class Element(object):
    def __init__(self, element, identifier, x=NEW_ELEMENT_X, y=NEW_ELEMENT_Y):
        self._element = element
        self.x = x
        self.y = y
        self.size = len(element)
        self.identifier = identifier

    def rotate(self):
        self._element = zip(*reversed(self._element))

    def get_raw(self):
        return self._element

    @classmethod
    def get_new_element(cls):
        ei = deepcopy(raw_elements[randrange(len(raw_elements))])
        return cls(ei[1], ei[0])

    def __getitem__(self, item):
        return self._element[item]

    def __str__(self):
        lines = []
        for i in range(self.size):
            line = []
            for j in range(self.size):
                if self._element[i][j] == ELEMENT_FILL:
                    line.append(ELEMENT_FILL)
                else:
                    line.append(ELEMENT_BLANK)
            lines.append(''.join(line))

        return ','.join(lines)

    def __repr__(self):
        return '<Element {} "{}">'.format(self.identifier, ','.join(self._element))


ALL_ELEMENTS = (Element(element, identifier) for identifier, element in raw_elements)

if __name__ == '__main__':
    print 'All elements:'
    for e in ALL_ELEMENTS:
        print repr(e)
