from copy import deepcopy

from core.debug import dbg
from core.font.json_manager import json_mg
from core.keyboard.base import keyboard_mg
from core.variable import PageTable, PathConfig


class BaseManager:
    """
    通用 manager：負責 state 管理、hook_x/hook_y 切換邏輯、以及（可選）JSON load/save。
    default_state: 初始 state dict
    json_map: dict[state_key] = (json_section, json_key)
    """
    def __init__(
            self,
            default_state:  dict[str, any],
            json_map:       dict[str, tuple[str, str]] | None = None
        ):
        self.page_table:        PageTable | None            = None
        # 管理當前程式內的「運行狀態」，也就是 hook_x / hook_y 控制的值
        self.state:             dict[str, any]              = deepcopy(default_state)
        # 保留「初始化的預設狀態」，方便重置或做型別判斷
        self._default_state:    dict[str, any]              = deepcopy(default_state)

        # 表示「state_key 對應到 JSON 的哪個 section/欄位」
        self.json_map:          dict[str, tuple[str, str]]  = json_map or {}
        # 用途：把操作索引（hook_y）對應到 state_key，操作介面用 hook_y 選擇不同欄位 → 找到對應的 state_key
        self.key_map:           dict[int, str]              = dict(enumerate(self.state.keys()))

        # 紀錄目前操作的欄位（hook_y 對應的 state_key）
        self.current_operate:   int                         = 0
        # 記錄上一次 hook_x 的值，用來判斷是否有變化
        self.last_hook_x:       any                         = None

    ''' ---- 公開 ---- '''
    def main_process(self):
        ''' 處理鍵盤輸入 / hook 狀態變化的入口方法 '''
        if keyboard_mg.hook_y != self.current_operate:
            self._switch_operation(keyboard_mg.hook_y)
        self._apply_hook_x_change(keyboard_mg.hook_x)

        # 確保程式啟動後 hook_x/hook_y 與 state 同步
        init_key = self.key_map.get(self.current_operate)
        if init_key is not None:
            keyboard_mg.hook_x = self.state.get(init_key, keyboard_mg.hook_x)
            keyboard_mg.hook_y = self.current_operate
            self.last_hook_x = keyboard_mg.hook_x

    def boot_base(self, catalog: PageTable):
        '''
        初始化 state 與 hook ，必須在進入此頁面前進行hook的初始化
        流程：先把 JSON 的資料讀進 state ，再把 state 的值同步到 keyboard_mg.hook_x / hook_y
        '''
        # 指定目前物件隸屬
        self.page_table = catalog

        # 如果沒有指定 json_map（沒有對應 JSON），只初始化 hook_x / hook_y
        # 這樣即使沒有 JSON，也能正確初始化 UI 狀態
        if not self.json_map:
            init_key = self.key_map.get(self.current_operate)
            if init_key is not None:
                keyboard_mg.hook_x = self.state.get(init_key, keyboard_mg.hook_x)
                keyboard_mg.hook_y = self.current_operate
                self.last_hook_x = keyboard_mg.hook_x
            return

        # 將 JSON 中的存檔值載入到 state，讓程式啟動時恢復上次設定
        for state_key, (section, json_key) in self.json_map.items():
            v_list = json_mg.get_json_list('dict', section, json_key)
            v = v_list[0] if v_list else None

            if v is None: continue

            # 若 default 是 int，強制轉成 int（再保險一次）
            if isinstance(self._default_state[state_key], int):
                try:
                    self.state[state_key] = int(v)
                except Exception:
                # 若無法直接轉 int，嘗試把 iterable 的第一項轉 int，最後 fallback 為預設值
                    try:
                        self.state[state_key] = int(v[0])
                    except Exception:
                        self.state[state_key] = self._default_state[state_key]
            else:
                self.state[state_key] = v

        # 藉由 state 初始化 hook_x hook_y，避免後續的 _switch_operation 覆寫 state
        init_key = self.key_map.get(self.current_operate)
        if init_key is not None:
            # 讓 UI 的 X 軸（或數值控制器）與當前 state 同步
            keyboard_mg.hook_x = self.state.get(init_key, keyboard_mg.hook_x)
            # 同步目前 UI 正在操作的欄位(y 軸)
            keyboard_mg.hook_y = self.current_operate
            self.last_hook_x = keyboard_mg.hook_x
        else:
            dbg.log(f'key_map have not {init_key}')

    def on_state_change(self, key: str, value: any):
        '''
         可覆寫的回調，可以在 hook_x 改變時做額外處理
         一般為該頁面的主迴圈，不會寫在此處
        '''
        pass

    def build_json_map(self, section_name: str) -> dict[str, tuple[str, str]]:
        """
        根據 word_dict_data 的指定 section 自動生成 json_map
        section_name: 只生成這個 section 的對應
        return: json_map dict[state_key] = (section, subkey)
        """
        json_map = {}
        section_data = json_mg.word_dict_data.get(section_name, {})

        for subkey in section_data:
            state_key = subkey.lower()  # 可自訂命名規則
            json_map[state_key] = (section_name, subkey)

        return json_map

    def build_default_state(self, section_name: str) -> dict[str, any]:
        """
        從 JSON 的指定 section 建立 default_state
        - 若 JSON 裡有值就拿 JSON 的第一筆
        - 若沒有則給 0 當預設
        """
        default_state = {}
        section_data = json_mg.word_dict_data.get(section_name, {})
        for subkey, value in section_data.items():
            state_key = subkey.lower()
            if isinstance(value, list) and len(value) > 0:
                default_state[state_key] = value[0]
            else:
                default_state[state_key] = 0
        return default_state

    def _switch_operation(self, new_y: int):
        ''' 當 hook_y 改變時切換到新的操作欄位（state_key） '''
        if new_y == self.current_operate: return

        old_key = self.key_map.get(self.current_operate)
        new_key = self.key_map.get(new_y)

        if old_key is not None:
            # 把舊欄位目前的 hook_x 值存回 state，這樣切回去舊欄位時可以恢復之前的值
            self.state[old_key] = keyboard_mg.hook_x
        else:
            dbg.log('old_key is None')

        if new_key is not None:
            # 將新欄位對應的 state 值寫回 hook_x，如果 state 裡沒有該 key，就保留 hook_x 原值
            keyboard_mg.hook_x = self.state.get(new_key, keyboard_mg.hook_x)
        else:
            dbg.log('new_key is None')

        # 更新目前操作索引與 last_hook_x
        self.current_operate = new_y
        self.last_hook_x = keyboard_mg.hook_x

    def _apply_hook_x_change(self, hook_x: any):
        ''' 將 當前 hook_x 的變化 套用到 state，並自動觸發 JSON 儲存與狀態變化回調 '''
        if hook_x == self.last_hook_x:
            return

        temp_key = self.key_map.get(self.current_operate)

        if temp_key is None:
            return

        # 將 hook_x 的新值更新到當前 state 中
        self.state[temp_key] = hook_x

        try:
            self.on_state_change(temp_key, hook_x)
        except Exception:
            dbg.log('on_state_change unable to execute')
        finally:
            self._save()
            self.last_hook_x = hook_x

    ''' ---- JSON helper ---- '''
    @staticmethod
    def _update_json_value(catalog: str, key: str, value: any):
        # 確保 section 存在
        if catalog not in json_mg.word_dict_data:
            json_mg.word_dict_data[catalog] = {}

        # 如果外層已經是 list，就直接覆蓋
        if isinstance(json_mg.word_dict_data[catalog], list):
            json_mg.word_dict_data[catalog] = value
            return

        # 外層是 dict 的然後才是 list 情況
        if isinstance(value, list):
            json_mg.word_dict_data[catalog][key] = value
        else:
            if key in json_mg.word_dict_data[catalog] and isinstance(json_mg.word_dict_data[catalog][key], list):
                json_mg.word_dict_data[catalog][key][0] = value
            else:
                json_mg.word_dict_data[catalog][key] = [value]

    def _save(self):
        ''' 只應儲存json_save寫入檔案 '''
        if not self.json_map:
            dbg.log('json_map is no data')
            return

        for state_key, (catalog, json_key) in self.json_map.items():
            if catalog == self.page_table.value:
                self._update_json_value(catalog, json_key, self.state[state_key])

        json_mg.write_json(PathConfig.json_save, json_mg.word_dict_data, only_keys = [self.page_table.value])

    '''
    功能：
    "SONG": {
        "SELECT_SONG": [
            8
        ],
        "VOLUME": [
            0
        ]
    }

    將上列結構轉乘下方結構，如此一來便能只由keys指接引入路徑而不是要寫兩層
    如：["SONG"]["VOLUME"]->['volume']

    self.json_map = {
            "select_song": ("SONG", "SELECT_SONG"),
            "volume": ("SONG", "VOLUME")
        }
    '''
