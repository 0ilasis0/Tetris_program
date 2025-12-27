from core.keyboard.variable import MaxLimits
from core.variable import JsonPath


class ConfigSongVar:
    WIDTH_BLOCK     = MaxLimits.SYS_SONG[JsonPath.SYS_VOLUME.value]
    HEIGHT_BLOCK    = 1

    # 因為加入隨機播放所以歌的實際長度+1
    RANDOM_SPACE    = 1

    # WINDOW_SCALE
    window_scale_list = [1.0, 0.73, 0.67, 0.5]
