from core.base import central_mg
from core.debug import dbg
from core.hmi.config.variable import ConfigSongVar
from core.keyboard.variable import MaxLimits
from core.variable import JsonPath


class SysWindowManager:
    """
    這是一個 Mixin，不單獨使用，必須被繼承。
    因為假設 self 擁有 BaseManager 中的 state, on_state_change, _save 等 BaseManager 的屬性
    """
    def __init__(self) -> None:
        self.window_scale_amount = 0

    def init_window_setup(self):
        saved_size_idx = self.state.get(JsonPath.SYS_WINDOW_SCALE.value, 0)
        if saved_size_idx < 0 or saved_size_idx >= len(ConfigSongVar.window_scale_list):
            saved_size_idx = 0
            # 同步修正 state，避免下次存檔存錯
            self.state[JsonPath.SYS_WINDOW_SCALE.value] = 0

        # 取得對應倍率
        target_ratio = ConfigSongVar.window_scale_list[saved_size_idx]
        # 更新螢幕大小
        central_mg.sys_window_scale_pending = target_ratio

        # 如果預設Screen_Size數量錯誤，則自行更新song的數量
        self.window_scale_amount = len(ConfigSongVar.window_scale_list)
        window_scale_amount = self.window_scale_amount - 1
        if MaxLimits.SYS_SONG[JsonPath.SYS_WINDOW_SCALE.value] != window_scale_amount:
            MaxLimits.SYS_SONG[JsonPath.SYS_WINDOW_SCALE.value] = window_scale_amount
            dbg.error(f"Updated MaxLimits: {JsonPath.SYS_WINDOW_SCALE.value} -> {window_scale_amount}")

    def apply_window_logic(self, value):
        """ 處理視窗改變的邏輯 (給 on_state_change 呼叫) """
        target_ratio = ConfigSongVar.window_scale_list[value]
        central_mg.sys_window_scale_pending = target_ratio

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
