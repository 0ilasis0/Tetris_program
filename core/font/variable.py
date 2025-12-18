from enum import Enum


class RenderingWord(Enum):
    # GAME
    COMBO   = 'COMBO'
    SCORE   = 'score:'
    KO      = 'KO'

    # SONG
    SHUFFLE = '隨機播放'

    # RANK
    RANKING = '名次'
    SEC     = '秒'
    MIN     = '分'
    FRACTION= '分數'
