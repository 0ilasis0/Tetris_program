import random

import pygame
from core.debug import dbg
from core.hmi.list import BaseManager
from core.hmi.variable import SongVariable
from core.variable import JsonPath, PathBase


# self.build_json_map("SONG")
class SongManager(BaseManager):
    def __init__(self):
        self.files          = []
        self.files_name     = []
        self.files_length   = 0

        self.loop = -1

        self.shuffle_list = []   # 儲存隨機排序後的歌曲索引
        self.shuffle_index = 0   # 播放到第幾首

    def on_state_change(self, key: str, value: any):
        ''' 狀態發生改變時執行，可以說是song的main '''
        if key == JsonPath.VOLUME.value:
            try:
                volume = float(value)
            except Exception:
                volume = 0.0
                dbg.log('volume is error')

            pygame.mixer.music.set_volume(max(0.0, min(1.0, volume * 0.1)))
            return

        if key == JsonPath.SELECT_SONG.value:
            self.play_current_song()
            return

    def set(self):
        default_state: dict[str, any] = self.build_default_state(JsonPath.SONG.value)
        json_map: dict[str, tuple[str, str]] = self.build_json_map(JsonPath.SONG.value)
        super().__init__(default_state = default_state, json_map = json_map)

        # self.boot_base()
        pygame.mixer.music.set_volume(self.state.get(JsonPath.VOLUME.value, 5) * 0.1)
        self._load_files()

        # 取得所有歌名
        self.files_name = [file.stem for file in self.files]
        # 所有歌的數量
        self.files_length = len(self.files)
        # 播放第一首歌
        self.play_current_song()

    def play_current_song(self):
        if not self.files:
            dbg.log("song_mg.files is no data")
            return

        # 讀取當前選擇的歌曲索引
        try:
            idx = int(self.state.get(JsonPath.SELECT_SONG.value, 0)) % (self.files_length + SongVariable.RANDOM_SPACE)
        except Exception:
            idx = 0
            dbg.log("song load error")

        idx = self._random_song(idx)

        # 取得要播放的歌曲檔案路徑，並播放音樂
        path = self.files[idx]
        try:
            pygame.mixer.music.load(str(path))
            pygame.mixer.music.play(loops = self.loop, start = 0.0)
        except Exception as e:
            dbg.log(f"[SongManager] play error: {e}")

    def _load_files(self):
        try:
            self.files = list(PathBase.song.glob("*.mp3"))
        except Exception:
            self.files = []
            dbg.log("load music files error")

    def _random_song(self, idx):
        ''' 將最後一個欄位設成隨機播放（洗牌播放） '''
        if idx == self.files_length:
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            self.loop = 0

            # 如果清單用完了 → 重新洗牌
            if not self.shuffle_list or self.shuffle_index >= len(self.shuffle_list):
                self.shuffle_list = list(range(self.files_length))
                random.shuffle(self.shuffle_list)
                self.shuffle_index = 0
                print(f"shuffle new list: {self.shuffle_list}")

            # 取出清單中的下一首
            idx = self.shuffle_list[self.shuffle_index]
            self.shuffle_index += 1

        else:
            pygame.mixer.music.set_endevent(0)
            self.loop = -1

        return idx

song_mg = SongManager()
