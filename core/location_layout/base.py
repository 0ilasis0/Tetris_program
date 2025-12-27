from dataclasses import dataclass, field

from core.debug import dbg
from core.font.variable import RenderingWord
from core.json.manager import json_mg
from core.location_layout.variable import location_config
from core.variable import PageTable, Position, Size


@dataclass
class LayoutItem:
    category: str       # 分類，例如 'MENU', 'SINGLE' 等
    name: str           # 唯一名稱
    size: Size
    pos: Position = field(default_factory = Position.zero)
    other: list = None


class LayoutConfig():
    def __init__(self) -> None:
        self.reload_setup()

    def reload_setup(self):
        """ 讀取來源資料 """
        # Menu
        menu_lines = json_mg.get_data('list', PageTable.MENU)
        self.menu_main_size = self._measure_text(content = menu_lines, shrink_map = {'!':0.5})

        # GAME
        self.game_score_size = self._measure_text(RenderingWord.SCORE.value, location_config.word_mini, location_config.word_mini)
        self.game_combo_size = self._measure_text(RenderingWord.COMBO.value)
        self.game_ko_size    = self._measure_text(RenderingWord.KO.value, location_config.word_mini, location_config.word_mini)

        # SYS_CONFIG
        song_lines = json_mg.get_data('list', PageTable.SYS_CONFIG)
        self.song_main_size = self._measure_text(content = song_lines)
        self.window_scale_size = self._measure_text(RenderingWord.WINDOW_SCALE_NUMBER.value)

        # HELP
        self.help_option_sizes = {}
        for mode in [PageTable.SINGLE.value, PageTable.DOUBLE.value, PageTable.ENDLESS.value]:
            title = json_mg.get_data('dict', PageTable.HELP.value, mode, 'title')
            description = json_mg.get_data('dict', PageTable.HELP.value, mode, 'description')
            self.help_option_sizes[mode] = {
                "title": self._measure_text(content = title),
                "description": self._measure_text(content = description)
            }

        # RANK
        self.rank_ranking_size = self._measure_text(
            content = RenderingWord.RANKING.value,
            line_height = location_config.word_big,
            word_width = location_config.word_big
        )
        self.rank_sec_size = self._measure_text(RenderingWord.SEC.value)
        self.rank_min_size = self._measure_text(RenderingWord.MIN.value)
        self.rank_fraction_size = self._measure_text(RenderingWord.FRACTION.value)


    @staticmethod
    def _measure_text(
            content,
            line_height = None,
            word_width = None,
            shrink_map = None,
            direction = "vertical"
        ):
        '''
        文字量測函式
        - content: 文字內容，可為 str 或 list
        - line_height: 行高
        - word_width: 一般字寬
        - shrink_map: 特殊字元縮放比例
        - direction: vertical 或 horizontal
        '''
        line_height = line_height if line_height is not None else location_config.word
        word_width = word_width if word_width is not None else location_config.word

        # 如果是 list，轉成單個字串並用換行分行
        if isinstance(content, list):
            lines = content
        elif isinstance(content, str):
            lines = content.split("\n")
        else:
            dbg.error(f"_measure_text: content type {type(content)} not supported")
            return Size(0,0)

        if direction == "vertical":
            max_length = 0
            for line in lines:
                length = len(line)
                if shrink_map:
                    for key, ratio in shrink_map.items():
                        length -= int(line.count(key) * (1 - ratio))
                max_length = max(max_length, length)
            width = max_length * word_width
            height = len(lines) * line_height

        elif direction == "horizontal":
            total_length = sum(len(line) for line in lines)
            if shrink_map:
                for line in lines:
                    for key, ratio in shrink_map.items():
                        total_length -= int(line.count(key) * (1 - ratio))
            width = total_length * word_width
            height = line_height

        return Size(width, height)

    def dict_to_layout_items(self, data):
        """
        遞迴轉換字典內容為 LayoutItem 物件
        - data: 傳入的原始字典或列表
        - category_key: 當子層沒提供 category 時，預設使用的標籤
        """
        # 如果是字典，檢查是否包含 LayoutItem 的特徵 Key
        if isinstance(data, dict):
            # 判斷標準：只要有 name, size, pos 就視為目標物件
            if all(k in data for k in ("name", "size", "pos")):
                return LayoutItem(
                    # 如果資料內有 category 就用它，否則用父層的 Key (例如 'SINGLE')
                    category = PageTable.SINGLE,
                    name     = data["name"],
                    size     = Size(*data["size"]),
                    pos      = Position(*data["pos"]),
                    other    = data.get("other")
                )
            else:
                # 如果不是目標物件，繼續往更深層遞迴
                # 並將目前的 Key 作為潛在的 category (parent_key) 傳下去
                return {k: self.dict_to_layout_items(v) for k, v in data.items()}

        # 如果是列表，處理列表中的每個元素
        elif isinstance(data, list):
            return [self.dict_to_layout_items(i) for i in data]

        # 基本資料型別直接回傳
        return data

layout_config = LayoutConfig()
