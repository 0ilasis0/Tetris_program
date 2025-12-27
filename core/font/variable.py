from dataclasses import dataclass
from enum import Enum


class RenderingWord(Enum):
    # GAME
    COMBO   = 'COMBO'
    SCORE   = 'score:'
    KO      = 'KO'

    # SYS_CONFIG
    SHUFFLE = '隨機播放'
    WINDOW_SCALE_NUMBER = [
        "全螢幕(1980X1080)",
        "視窗(1451X788)",
        "略小(1320X720)",
        "迷你(990X540)",
    ]

    # RANK
    RANKING = '名次'
    SEC     = '秒'
    MIN     = '分'
    FRACTION= '分數'
