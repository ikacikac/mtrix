# -*- coding: utf8 -*-

from math import sin, cos
from random import randrange

from vectors import Vect2D


def Shake(offset):
    """

    Credits to:
    https://gamedev.stackexchange.com/questions/1828/realistic-camera-screen-shake-from-explosion

    :param Vect2D offset:
    :return:

    """
    init_offset = offset
    radius = 30.0

    rand_angle = randrange(360)
    offset = Vect2D(sin(rand_angle) * radius, cos(rand_angle) * radius)

    yield init_offset + offset

    while radius > 1.0:
        radius *= 0.9
        rand_angle += 180 + randrange(60)
        offset = Vect2D(sin(rand_angle) * radius, cos(rand_angle) * radius)
        yield init_offset + offset

    yield init_offset