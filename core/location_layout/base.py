from core.debug import dbg
from core.font.json_manager import json_mg
from core.font.variable import RenderingWord
from core.location_layout.variable import BaseParameter, Size
from core.variable import PageTable


class LayoutConfig(BaseParameter):
    def __init__(self) -> None:
        """ 讀取來源資料 """
        # Menu
        menu_lines = json_mg.get_json_list('list', PageTable.MENU)
        self.menu_main_size = self._measure_text(content = menu_lines, shrink_map={'!':0.5})

        # GAME
        self.game_score_size = self._measure_text(RenderingWord.SCORE.value, self.word_mini, self.word_mini)
        self.game_combo_size = self._measure_text(RenderingWord.COMBO.value)
        self.game_ko_size    = self._measure_text(RenderingWord.KO.value, self.word_mini, self.word_mini)

        # SONG
        song_lines = json_mg.get_json_list('list', PageTable.SONG)
        self.song_main_size = self._measure_text(content = song_lines)

        # HELP
        self.help_option_sizes = {}
        for mode in [PageTable.SINGLE.value, PageTable.DOUBLE.value, PageTable.ENDLESS.value]:
            title = json_mg.get_json_list('dict', PageTable.HELP.value, mode, 'title')
            description = json_mg.get_json_list('dict', PageTable.HELP.value, mode, 'description')

            self.help_option_sizes[mode] = {
                "title": self._measure_text(content=title),
                "description": self._measure_text(content=description)
            }

        # RANK
        self.rank_ranking_size = self._measure_text(
            content = RenderingWord.RANKING.value,
            line_height = BaseParameter.word_big,
            word_width = BaseParameter.word_big
        )
        self.rank_sec_size = self._measure_text(RenderingWord.SEC.value)
        self.rank_min_size = self._measure_text(RenderingWord.MIN.value)
        self.rank_fraction_size = self._measure_text(RenderingWord.FRACTION.value)


    @staticmethod
    def _measure_text(
            content,
            line_height = BaseParameter.word,
            word_width = BaseParameter.word,
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
        # 如果是 list，轉成單個字串並用換行分行
        if isinstance(content, list):
            lines = content
        elif isinstance(content, str):
            lines = content.split("\n")
        else:
            dbg.log(f"_measure_text: content type {type(content)} not supported")
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

layout_config = LayoutConfig()
