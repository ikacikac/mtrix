# -*- coding: utf8 -*-

"""
Game utilities


Included are:
- Vect2D helper class for 2D vector representation and operations,
- Events that are risen and that can be connected to.

"""


class Vect2D(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_tuple(self):
        return self.x, self.y

    def __add__(self, other):
        """

        :param Vect2D other:
        :return:

        """
        return Vect2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """

        :param Vect2D other:
        :return:

        """
        return Vect2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, int):
            return Vect2D(self.x * other, self.y * other)

    def __div__(self, other):
        if isinstance(other, int):
            return Vect2D(self.x / other, self.y / other)

    def __repr__(self):
        return "Vect2D({}, {})".format(self.x, self.y)

    def __str__(self):
        return "Vect2D x:{} y:{}".format(self.x, self.y)
