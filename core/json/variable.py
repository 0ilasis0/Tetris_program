from dataclasses import dataclass

from core.json.default_data import RenewJSON
from core.variable import PathConfig


@dataclass
class JsonConfig():
    build_enable = False

    # 格式: (目標檔案路徑, 對應的生成函式)
    build_tasks = [
        # 未來如果有新的，直接加在下面，例如：
        # (PathConfig.json_single, RenewJSON.single_object),
        # (PathConfig.json_save, RenewJSON.save_data),
    ]
