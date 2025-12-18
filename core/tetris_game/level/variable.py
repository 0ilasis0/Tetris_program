from enum import Enum

from core.tetris_game.variable import GameVariable


class LevelParameter:
    MAX_LEVEL = 10 - 1
    LEVEL_INTERVAL = 20

    # drop_clock, raise_interval uint is ms
    difficult_table = {
        0:  {"drop_clock": GameVariable.DROP_CLOCK * 1.0, "raise_lines": 0, "raise_interval": GameVariable.DROP_CLOCK * 14},
        1:  {"drop_clock": GameVariable.DROP_CLOCK * 0.9, "raise_lines": 0, "raise_interval": GameVariable.DROP_CLOCK * 14},
        2:  {"drop_clock": GameVariable.DROP_CLOCK * 0.9, "raise_lines": 1, "raise_interval": GameVariable.DROP_CLOCK * 14},
        3:  {"drop_clock": GameVariable.DROP_CLOCK * 0.8, "raise_lines": 1, "raise_interval": GameVariable.DROP_CLOCK * 12},
        4:  {"drop_clock": GameVariable.DROP_CLOCK * 0.7, "raise_lines": 1, "raise_interval": GameVariable.DROP_CLOCK * 12},
        5:  {"drop_clock": GameVariable.DROP_CLOCK * 0.6, "raise_lines": 1, "raise_interval": GameVariable.DROP_CLOCK * 10},
        6:  {"drop_clock": GameVariable.DROP_CLOCK * 0.8, "raise_lines": 2, "raise_interval": GameVariable.DROP_CLOCK * 14},
        7:  {"drop_clock": GameVariable.DROP_CLOCK * 0.8, "raise_lines": 2, "raise_interval": GameVariable.DROP_CLOCK * 12},
        8:  {"drop_clock": GameVariable.DROP_CLOCK * 0.6, "raise_lines": 2, "raise_interval": GameVariable.DROP_CLOCK * 12},
        9:  {"drop_clock": GameVariable.DROP_CLOCK * 0.5, "raise_lines": 2, "raise_interval": GameVariable.DROP_CLOCK * 10},
    }

    level_table = {
        0: 0,
        30: 1,
        60: 2,
        90: 3,
        120: 4,
        150: 5,
        180: 6,
        210: 7,
        240: 8,
        270: 9,
    }
