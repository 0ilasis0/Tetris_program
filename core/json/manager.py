import json

from core.debug import dbg
from core.variable import PageTable, PathConfig


class JsonManager:
    def __init__(self) -> None:
        self.base  = 'utf-8'
        self.word_list_data = {}
        self.word_dict_data = {}

        # 初始化json內容
        self.read_dict_json(PathConfig.json_save)
        self.read_dict_json(PathConfig.json_help)
        self.read_list_json(PathConfig.json_display)

    def read_list_json(self, file_path):
        """
        讀 JSON 並存到 word_list_data
        - key 統一轉成 PageTable enum
        """
        with open(file_path, "r", encoding=self.base) as f:
            data = json.load(f)

        for key, lines in data.items():
            # 嘗試把 JSON key 轉成 PageTable enum
            try:
                enum_key = PageTable[key]
            except KeyError:
                dbg.log(f"Warning: JSON key '{key}' 沒有對應的 PageTable enum，將使用字串 key")
                enum_key = key  # fallback 用字串 key

            # 存入 word_list_data
            self.word_list_data[enum_key] = lines

    def read_dict_json(self, file_path):
        """
        讀取巢狀 dict JSON，並存到 word_dict_data
        """
        if not file_path.exists():
            dbg.log(f"檔案不存在：{file_path}")
            return

        with open(file_path, "r", encoding = self.base) as f:
            data = json.load(f)

        # 將巢狀 dict 直接存入 word_data
        for page_key, page_data in data.items():
            self.word_dict_data[page_key] = page_data

    @staticmethod
    def _read_existing(file_path, encoding):
        """讀取舊有 JSON 檔案，若失敗則回傳空 dict"""
        try:
            with open(file_path, "r", encoding=encoding) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def write_json(self, file_path, data, mode = "w", encoding = None, indent = 4, only_keys = None):
        """
        將資料寫入 JSON 檔案
        - mode='w': 覆蓋
        - mode='a': 附加（dict → 合併，list → 延伸）
        - only_keys: 只更新指定 key，不會洗掉其他 key
        """
        if encoding is None:
            encoding = self.base

        existing_data = {}

        # 只有 append 模式 或 only_keys 指定時，才需要先讀取舊檔
        if mode == "a" or only_keys is not None:
            existing_data = self._read_existing(file_path, encoding)
            if not isinstance(existing_data, (dict, list)):
                existing_data = {}  # 非法格式強制重置

        # --- only_keys 更新邏輯 ---
        if only_keys is not None:
            if not isinstance(existing_data, dict):
                existing_data = {}
            for k in only_keys:
                if k in data:
                    existing_data[k] = data[k]
            data_to_write = existing_data
        else:
            data_to_write = data

        # --- 附加模式 ---
        if mode == "a":
            if isinstance(existing_data, dict) and isinstance(data_to_write, dict):
                existing_data.update(data_to_write)
                data_to_write = existing_data
            elif isinstance(existing_data, list) and isinstance(data_to_write, list):
                data_to_write = existing_data + data_to_write
            else:
                raise ValueError("無法附加不同型別的 JSON 資料")

        # --- 寫回檔案 ---
        with open(file_path, "w", encoding=encoding) as f:
            json.dump(data_to_write, f, ensure_ascii=False, indent=indent)

    def get_json_list(self, data_type, *keys):
        """
        通用取得 list
        - data_type: 'dict' 或 'list'，決定要用 word_dict_data 或 word_list_data
        - *keys: JSON 層級 key，最上層到最底層
        """
        if data_type == 'dict':
            data = self.word_dict_data
        elif data_type == 'list':
            data = self.word_list_data
        else:
            dbg.log(f'{data_type} is not dict or list')
            return []

        try:
            for key in keys:
                data = data[key]
        except (KeyError, TypeError):
            return []

        # 轉成 list
        if isinstance(data, list):
            return data
        elif isinstance(data, str):
            return [data]

json_mg = JsonManager()


