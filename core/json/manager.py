import json

from core.debug import dbg
from core.json.variable import JsonConfig
from core.variable import PageTable, PathConfig


class JsonManager:
    def __init__(self) -> None:
        self.base  = 'utf-8'
        self.word_list_data = {}
        self.word_dict_data = {}

        if JsonConfig.build_enable:
            self.build_json()

        self.setup()

    def setup(self):
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
                dbg.error(f"Warning: JSON key '{key}' 沒有對應的 PageTable enum，將使用字串 key")
                enum_key = key  # fallback 用字串 key

            # 存入 word_list_data
            self.word_list_data[enum_key] = lines

    def read_dict_json(self, file_path):
        """
        讀取巢狀 dict JSON，並存到 word_dict_data
        """
        if not file_path.exists():
            dbg.error(f"檔案不存在：{file_path}")
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

    def delete_data(self, data_type, *keys):
        """
        刪除指定資料
        - data_type: 'dict' 或 'list'
        - *keys: 要刪除的路徑 (例如  PageTable.HELP.value, PageTable.SINGLE.value)
        - return: bool
        """
        if not keys:
            dbg.error("刪除失敗：未提供 Key")
            return False

        # 決定資料源
        if data_type == 'dict':
            data = self.word_dict_data
        elif data_type == 'list':
            data = self.word_list_data
        else:
            dbg.error(f"刪除失敗：不支援的型別 {data_type}")
            return False

        # 依照路徑尋找父節點
        try:
            # 我們要導航到「倒數第二個」節點
            target_parent = data
            for key in keys[:-1]:
                target_parent = target_parent[key]

            # 3. 執行刪除最後一個 key
            last_key = keys[-1]
            if last_key in target_parent:
                del target_parent[last_key]
                dbg.log(f"成功刪除 {data_type} 中的路徑: {keys}")
                return True
            else:
                dbg.error(f"刪除失敗：Key '{last_key}' 不存在於路徑 {keys[:-1]} 中")
                return False

        except (KeyError, TypeError) as e:
            dbg.error(f"刪除失敗：路徑錯誤 {keys} ({e})")
            return False

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
            json.dump(data_to_write, f, ensure_ascii = False, indent = indent)

    def get_data(self, data_type, *keys):
        """
        通用取得原始資料片段 (不強制轉型)
        - data_type: 'dict' 或 'list'
        - *keys: JSON 層級路徑
        """
        data = self.word_dict_data if data_type == 'dict' else self.word_list_data

        try:
            for key in keys:
                data = data[key]
            return data
        except (KeyError, TypeError):
            dbg.error(f"keys:{keys} or key:{key} is error")
            return None

    def build_json(self):
        """
        建置方法：讀取 JsonConfig 中的任務清單並執行
        """
        if not hasattr(JsonConfig, 'build_tasks') or not JsonConfig.build_tasks:
            dbg.log("沒有設定 build_tasks ，跳過建置流程")
            return

        dbg.log("--- 開始執行 JSON 建置流程 ---")

        for file_path, builder_func in JsonConfig.build_tasks:
            try:
                data = {}

                # 呼叫外部定義的函式來填充資料 (builder_func 就是 RenewJSON.single_object)
                builder_func(data)
                self.write_json(file_path, data, mode='w', encoding=None, indent=4)

                dbg.log(f"已建置: {file_path}")

            except Exception as e:
                dbg.error(f"建置失敗 {file_path}: {e}")

json_mg = JsonManager()
