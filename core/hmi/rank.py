from core.font.json_manager import json_mg
from core.hmi.list import BaseManager
from core.variable import PageTable, PathConfig


class RankManager(BaseManager):
    def __init__(self):
        # 預設一個排行榜狀態
        super().__init__({PageTable.RANK.value: []})
        self.page_table = PageTable.RANK
        self.load_rank()

    def load_rank(self):
        """讀取 JSON 中的排行榜"""
        self.state[PageTable.RANK.value] = json_mg.get_json_list("dict", PageTable.RANK.value)

    def add_score(self, min: int, sec: int, score: int):
        new_entry = [min, sec, score]
        rank_list = self.state[PageTable.RANK.value]

        # 檢查是否已經有完全相同的分數和時間
        if new_entry in rank_list:
            return  # 已存在，不加入

        # 新條目加入排行榜
        rank_list.append(new_entry)

        # 排序：分數高 → 時間短
        rank_list.sort(key=lambda x: (-x[2], x[0]*60 + x[1]))

        # 保留前 3 名
        self.state[PageTable.RANK.value] = rank_list[:3]

        # 存回 JSON
        self._update_json_value(PageTable.RANK.value, PageTable.RANK.value, self.state[PageTable.RANK.value])
        json_mg.write_json(PathConfig.json_save, json_mg.word_dict_data, only_keys=[PageTable.RANK.value])

    def get_rank(self):
        """取得排行榜資料"""
        return self.state[PageTable.RANK.value]

rank_mg = RankManager()
