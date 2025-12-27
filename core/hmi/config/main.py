from core.hmi.config.song import SysSongManager
from core.hmi.config.window_scale import SysWindowManager
from core.hmi.list import BaseManager
from core.variable import JsonPath, PageTable


class SysConfigManager(BaseManager, SysSongManager, SysWindowManager):
    def __init__(self):
        SysSongManager.__init__(self)
        SysWindowManager.__init__(self)

    def on_state_change(self, key: str, value: any):
        """
        這裡是總路由 (Router)。
        負責判斷 key 是屬於哪個部門的，然後轉發給對應的區塊處理。
        """
        # 視窗部門
        if key == JsonPath.SYS_WINDOW_SCALE.value:
            self.apply_window_logic(value)

        # 歌曲部門 (可以是多個 key)
        elif key in [JsonPath.SYS_VOLUME.value, JsonPath.SYS_SELECT_SONG.value]:
            self.apply_song_logic(key, value)

    def setup(self):
        default_state: dict[str, any] = self.build_default_state(JsonPath.SYS_CONFIG.value)
        json_map: dict[str, tuple[str, str]] = self.build_json_map(JsonPath.SYS_CONFIG.value)

        # 手動呼叫 BaseManager 的 init 來載入 JSON
        BaseManager.__init__(self, default_state = default_state, json_map = json_map)

        self.page_table = PageTable.SYS_CONFIG
        # self.boot_base()

        self.init_song_setup()
        self.init_window_setup()

    def interrupt_window_scale(self, index: int):
        """
        給外部事件interrupt呼叫使用
        """
        key = JsonPath.SYS_WINDOW_SCALE.value
        self.state[key] = index

        # 執行變更邏輯
        self.on_state_change(key, index)
        # 觸發存檔
        self._save()

sys_config_mg = SysConfigManager()
