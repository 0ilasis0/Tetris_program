import pygame
from core.hmi.config.main import sys_config_mg
from core.hmi.config.variable import ConfigSongVar
from core.screen.variable import ScreenConfig
from core.variable import JsonPath


def main_interrupt(event):
    # 音樂播放完畢
    if event.type == pygame.USEREVENT:
        sys_config_mg.play_current_song()           # 再隨機播放下一首

    # 偵測右上角螢幕縮放標籤是否被按下
    elif event.type == pygame.VIDEORESIZE:
        raw_ratio = event.h / ScreenConfig.DESIGN_HEIGHT

        # 者出最接近的現有螢幕倍率的數值
        renew_index = min(
                range(len(ConfigSongVar.window_scale_list)),
                key = lambda i: abs(ConfigSongVar.window_scale_list[i] - raw_ratio)
            )

        current_idx = sys_config_mg.state.get(JsonPath.SYS_WINDOW_SCALE.value, 0)

        if renew_index != current_idx:
            sys_config_mg.interrupt_window_scale(renew_index)


