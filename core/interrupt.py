import pygame

from core.hmi.song import song_mg


def main_interrupt(event):
    # 音樂播放完畢
    if event.type == pygame.USEREVENT:
        song_mg.play_current_song()           # 再隨機播放下一首
