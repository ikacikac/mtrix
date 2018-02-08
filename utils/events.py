# -*- coding: utf8 -*-

import blinker


lines_cleared = blinker.signal('board/lines_removed')

current_lines = blinker.signal('game/lines')
current_score = blinker.signal('game/score')
current_level = blinker.signal('game/level')

level_increased = blinker.signal('game/level_increased')

increase_level = blinker.signal('timer/increase_level')

activate_shaking = blinker.signal('game/activate_shaking')