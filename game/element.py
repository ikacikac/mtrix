#!/usr/bin/env python2.7
# -*- coding: utf8 -*-
"""

All elements definitions and helper methods for elements.

"""
from copy import deepcopy
from random import randrange

from game.config import NEW_ELEMENT_X, NEW_ELEMENT_Y
from game.config import ELEMENT_BLANK, ELEMENT_FILL
from game.config import MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, MOVE_SMASH

from game.exceptions import MovementException

# Elements definitions
e1 = [' E ', 'EEE', '   ']
e2 = ['  E', 'EEE', '   ']
e3 = ['E  ', 'EEE', '   ']
e4 = ['EE', 'EE']
e5 = [' E  ', ' E  ', ' E  ', ' E  ']
e6 = [' EE', 'EE ', '   ']
e7 = ['EE ', ' EE', '   ']

elements = [e1, e2, e3, e4, e5, e6, e7]

ELEMENTS_IDS = ['1', '2', '3', '4', '5', '6', '7']

raw_elements = zip(ELEMENTS_IDS, elements)


def try_to_rotate(board, element):
    """
    Takes board matrix and element matrix and rotates element by 90 degrees.

    If there is a collision than MovementException is risen.

    :param Board board:
    :param Element element:

    :raise MovementException

    """
    s = element.size
    x = element.x

    inc = 1
    if board.width/2 < element.x:
        inc = -1

    for i in range(0, s/2+1):
        element.x = x + inc * i
        try:
            element.rotate()
            board.can_place_element(element)
            return
        except MovementException:
            element.rotate(reverse=True)
            continue

    element.x = x


def get_possible_movements(board, element):
    """
    Returns a list of possible moves depending on state of the
     board and position of the element.

    :param Board board:
    :param Element element:
    :return List of movements that are allowed
    :rtype list[int]

    """
    possible_moves = [MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN, MOVE_SMASH]

    try:
        element.x -= 1
        board.can_place_element(element)
    except MovementException:
        possible_moves.pop(possible_moves.index(MOVE_LEFT))
    finally:
        element.x += 1

    try:
        element.x += 1
        board.can_place_element(element)
    except MovementException:
        possible_moves.pop(possible_moves.index(MOVE_RIGHT))
    finally:
        element.x -= 1

    try:
        element.rotate()
        board.can_place_element(element)
    except MovementException:
        possible_moves.pop(possible_moves.index(MOVE_UP))
    finally:
        element.rotate(reverse=True)

    try:
        element.y += 1
        board.can_place_element(element)
    except MovementException:
        possible_moves.pop(possible_moves.index(MOVE_DOWN))
        possible_moves.pop(possible_moves.index(MOVE_SMASH))
    finally:
        element.y -= 1

    return possible_moves


class Element(object):
    """

    :param list _element:
    :param int x:
    :param int y:
    :param int size:
    :param str identifier:

    """
    def __init__(self, element, identifier, x=NEW_ELEMENT_X, y=NEW_ELEMENT_Y):
        self._element = element
        self.x = x
        self.y = y
        self.size = len(element)
        self.identifier = identifier

    def rotate(self, reverse=False):
        if reverse is True:
            self._element = [i for i in reversed(zip(*self._element))]
        else:
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
        return 'Element({} "{}")'.format(self.identifier, ','.join(self._element))


ALL_ELEMENTS = (Element(element, identifier) for identifier, element in raw_elements)

if __name__ == '__main__':
    print 'All elements:'
    for e in ALL_ELEMENTS:
        print repr(e)
