from enum import Enum

import pygame
from core.screen.variable import ScreenConfig
from core.variable import colors

#  0 0 0 0
#  0 0 0 0
#  0 0 0 0
#  0 0 0 0

figures = {
    "I": {
        "rotations": [[2, 6, 10, 14], [4, 5, 6, 7]],
        "color": colors[4]
    },
    "Z": {
        "rotations": [[1, 2, 6, 7], [2, 5, 6, 9]],
        "color": colors[5]
    },
    "S": {
        "rotations": [[6, 7, 9, 10], [2, 6, 7, 11]],
        "color": colors[6]
    },
    "J": {
        "rotations": [[2, 3, 6, 10], [5, 6, 7, 11], [3, 7, 10, 11], [1, 5, 6, 7]],
        "color": colors[10]
    },
    "L": {
        "rotations": [[2, 3, 7, 11], [3, 5, 6, 7], [2, 6, 10, 11], [5, 6, 7, 9]],
        "color": colors[9]
    },
    "T": {
        "rotations": [[2, 5, 6, 7], [2, 6, 7, 10], [5, 6, 7, 10], [3, 6, 7, 11]],
        "color": colors[11]
    },
    "O": {
        "rotations": [[2, 3, 6, 7]],
        "color": colors[13]
    },
}



class BaseVariable:
    NUMBER_MAX = 1000

class GameState(Enum):
    STATE_START       = 'start'
    STATE_KO          = 'ko'
    STATE_GAMEOVER    = 'gameover'

class GameVariable:
    # SIZE AND BOLCK
    WIDTH_BLOCK     = 10
    HEIGHT_BLOCK    = 20
    CELL_BLOCK      = 4
    ZOOM_SIZE       = ScreenConfig.tetris_cell

    # COLORS
    EMPTY_COLOR = colors[1]
    RAISE_COLOR = colors[2]
    MINE_COLOR  = colors[0]
    GRID_COLOR  = colors[3]

    # GAME
    MAX_KO_COUNT    = 3
    MAX_COMBO       = 20
    MAX_SCORE       = BaseVariable.NUMBER_MAX

    # SYS_BASE
    DROP_CLOCK  = 500    # 方塊每 0.5 秒自動下落
    FPS         = 60

    # OTHER
    SINGLE_MENU_WIDTH_BLOCK     = 5
    SINGLE_MENU_HEIGHT_BLOCK    = 2


class RankVariable:
    RANK_TOTAL = 3
    DATA_TOTAL = 4

# 設定遊戲 FPS
clock = pygame.time.Clock()
