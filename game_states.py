#!/usr/bin/env python2.7


from internal_config import MOVE_ENTER, MOVE_PAUSE, MOVE_ESCAPE


class HomeState(object):

    def process_input(self, key):
        if key == MOVE_PAUSE:
            return PlayState()
        elif key == MOVE_ESCAPE:
            return HaltState()
        else:
            return self


class PlayState(object):

    def process_input(self, key):
        if key == MOVE_PAUSE:
            return PauseState()
        elif key == MOVE_ESCAPE:
            return HomeState()
        else:
            return self


class PauseState(object):

    def process_input(self, key):
        if key == MOVE_PAUSE:
            return PlayState()
        elif key == MOVE_ESCAPE:
            return HomeState()
        else:
            return self


class GameOverState(object):

    def process_input(self, key):
        if key in [MOVE_ESCAPE, MOVE_ENTER]:
            return HomeState()
        else:
            return self


class HaltState(object):

    def process_input(self, key):
        return self


class GameState(object):

    def __init__(self):
        self.current_state = HomeState()

    def get_next_state(self, key):
        self.current_state = self.current_state.process_input(key)
        return self.current_state

    def go_to_game_over(self):
        self.current_state = GameOverState()
