from enum import Enum

from core.variable import JsonPath


class MaxLimits(dict, Enum):
    SYS_SONG = {
                JsonPath.SYS_SELECT_SONG.value: 10,
                JsonPath.SYS_VOLUME.value:      10,
                JsonPath.SYS_WINDOW_SCALE.value: 3,
            }

