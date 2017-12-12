#!/usr/bin/env python2.7


import pygame

from internal_config import MOVE_ENTER, MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT
from game import Game
from screen import Screen

key_pressed = lambda e, k: e.type == pygame.KEYDOWN and e.key == k


class GameStateManager(object):
    """
    :param GameState state:
    :param GameState previous_state:
    :param bool _done:

    """
    def __init__(self, start_state=None):
        self.state = start_state

        self.previous_state = None

        self._done = False
        self._clock = pygame.time.Clock()

    def run(self):
        while self._done is False:
            self.handle_event()
            self.update()
            self.draw()
            pygame.display.update()
            self._clock.tick(60)

    def handle_event(self):
        for event in pygame.event.get():
            self.state.handle_event(event)

    def update(self):
        if self.state.quit:
            self._done = True
        elif self.state.done:
            self.flip_state()
        else:
            self.state.update()

    def draw(self):
        # TODO reference to screen?
        self.state.draw()

    def flip_state(self):
        next_state = self.state.next_state
        context = self.state.context
        self.state = next_state(context=context)
        self.state.startup()


class GameState(object):
    """
    :param Context _context:
    :param GameState next_state:
    :param bool quit:
    :param bool done:l

    """
    def __init__(self, context=None):
        """

        :param Context context:
        :return:
        """
        self.context = context
        self.next_state = None
        self.quit = False
        self.done = False

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def startup(self):
        pass


class HomeScreenState(GameState):

    def __init__(self, *args, **kwargs):
        super(HomeScreenState, self).__init__(*args, **kwargs)
        self.context = Context(game=Game(), screen=Screen())
        self._screen = self.context.screen
        self._game = self.context.game

    def handle_event(self, event):
        if key_pressed(event, pygame.K_p):
            self.next_state = GamePlayState
            self.done = True
        elif key_pressed(event, pygame.K_ESCAPE):
            self.done = True
            self.quit = True

    def update(self):
        pass

    def draw(self):
        self._screen.draw_home_screen()


class GamePlayState(GameState):

    def __init__(self, *args, **kwargs):
        super(GamePlayState, self).__init__(*args, **kwargs)
        self._screen = self.context.screen
        self._game = self.context.game
        self._board = None
        self._key = None

    def handle_event(self, event):
        if key_pressed(event, pygame.K_ESCAPE):
            self.next_state = HomeScreenState
            self.done = True
        elif key_pressed(event, pygame.K_p):
            self.next_state = GamePauseState
            self.done = True
        elif key_pressed(event, pygame.K_UP):
            self._key = MOVE_UP
        elif key_pressed(event, pygame.K_DOWN):
            self._key = MOVE_DOWN
        elif key_pressed(event, pygame.K_LEFT):
            self._key = MOVE_LEFT
        elif key_pressed(event, pygame.K_RIGHT):
            self._key = MOVE_RIGHT
        elif key_pressed(event, pygame.K_RETURN):
            self._key = MOVE_ENTER
        else:
            self._key = None

    def update(self):
        c, self._board = self._game.update(self._key)
        self._key = None
        if c is False:
            self.done = True
            self.next_state = GameOverState

    def draw(self):
        self._screen.set_next_element(self._game.get_next_element())
        self._screen.set_board(self._board)
        self._screen.draw_game_play()

    def startup(self):
        _, self._board = self._game.update(self._key)
        self._key = None


class GamePauseState(GameState):

    def __init__(self, *args, **kwargs):
        super(GamePauseState, self).__init__(*args, **kwargs)
        self._screen = self.context.screen
        self._game = self.context.game
        self._board = None
        self._key = None

    def handle_event(self, event):
        if key_pressed(event, pygame.K_ESCAPE):
            self.next_state = HomeScreenState
            self.done = True
        elif key_pressed(event, pygame.K_p):
            self.next_state = GamePlayState
            self.done = True
        else:
            self._key = None

    def draw(self):
        self._screen.set_next_element(self._game.get_next_element())
        self._screen.set_board(self._board)
        self._screen.draw_game_play()
        self._screen.draw_pause_screen()

    def startup(self):
        _, self._board = self._game.update(self._key)
        self._key = None


class GameOverState(GameState):

    def __init__(self, *args, **kwargs):
        super(GameOverState, self).__init__(*args, **kwargs)
        self._screen = self.context.screen
        self._game = self.context.game
        self._board = None
        self._key = None

    def handle_event(self, event):
        if key_pressed(event, pygame.K_ESCAPE):
            self.next_state = HomeScreenState
            self.done = True
            self.quit = True
        elif key_pressed(event, pygame.K_p):
            self.next_state = HomeScreenState
            self.done = True
        else:
            self._key = None

    def draw(self):
        self._screen.set_next_element(self._game.get_next_element())
        self._screen.set_board(self._board)
        self._screen.draw_game_play()
        self._screen.draw_game_over_screen()

    def startup(self):
        _, self._board = self._game.update(self._key)
        self._key = None


class Context(object):

    def __init__(self, screen, game):
        """

        :param Screen screen:
        :param Game game:
        :return:
        """
        self.screen = screen
        self.game = game