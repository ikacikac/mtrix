# -*- coding: utf8 -*-


class MovementException(Exception):
    pass


class RightException(MovementException):
    pass


class LeftException(MovementException):
    pass


class RotateException(MovementException):
    pass


class ColException(MovementException):
    pass


class DownException(MovementException):
    pass


