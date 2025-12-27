from core.tetris_game.variable import GameVar


class LevelParameter:
    MAX_LEVEL = 10 - 1
    LEVEL_INTERVAL = 20

    # drop_clock, raise_interval uint is ms
    difficult_table = {
        0:  {"drop_clock": GameVar.DROP_CLOCK * 1.0, "raise_lines": 0, "raise_interval": GameVar.DROP_CLOCK * 14 // 1000},
        1:  {"drop_clock": GameVar.DROP_CLOCK * 0.9, "raise_lines": 0, "raise_interval": GameVar.DROP_CLOCK * 14 // 1000},
        2:  {"drop_clock": GameVar.DROP_CLOCK * 0.9, "raise_lines": 1, "raise_interval": GameVar.DROP_CLOCK * 14 // 1000},
        3:  {"drop_clock": GameVar.DROP_CLOCK * 0.8, "raise_lines": 1, "raise_interval": GameVar.DROP_CLOCK * 12 // 1000},
        4:  {"drop_clock": GameVar.DROP_CLOCK * 0.7, "raise_lines": 1, "raise_interval": GameVar.DROP_CLOCK * 12 // 1000},
        5:  {"drop_clock": GameVar.DROP_CLOCK * 0.6, "raise_lines": 1, "raise_interval": GameVar.DROP_CLOCK * 10 // 1000},
        6:  {"drop_clock": GameVar.DROP_CLOCK * 0.8, "raise_lines": 2, "raise_interval": GameVar.DROP_CLOCK * 14 // 1000},
        7:  {"drop_clock": GameVar.DROP_CLOCK * 0.8, "raise_lines": 2, "raise_interval": GameVar.DROP_CLOCK * 12 // 1000},
        8:  {"drop_clock": GameVar.DROP_CLOCK * 0.6, "raise_lines": 2, "raise_interval": GameVar.DROP_CLOCK * 12 // 1000},
        9:  {"drop_clock": GameVar.DROP_CLOCK * 0.5, "raise_lines": 2, "raise_interval": GameVar.DROP_CLOCK * 10 // 1000},
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
