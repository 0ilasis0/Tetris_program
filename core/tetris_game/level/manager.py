from core.debug import dbg
from core.tetris_game.level.variable import LevelParameter
from core.tetris_game.variable import GameVar


class LevelManager:
    def __init__(
            self,
            difficult_table: dict = LevelParameter.difficult_table,
            max_level: int = LevelParameter.MAX_LEVEL
        ):
        self.difficult_table = difficult_table
        self.max_level = max_level
        self.current_level = -1
        self.last_time = None
        # 初始時同步 current_difficult
        self.current_difficult = self.difficult_table.get(self.current_level, self.difficult_table[self.max_level])

    def update_level(self, player, score = None, level = None):
        """
        根據分數更新等級
        可以用線性、權重或分數門檻決定升級
        """
        if score is not None:
            new_level = max(lvl for s, lvl in LevelParameter.level_table.items() if score >= s)
        elif level is not None:
            new_level = min(level, self.max_level)
        else:
            dbg.error('score and level is None')
            return

        if new_level > self.current_level or level is not None:
            self.current_level = new_level

            # 同步 current_difficult
            self.current_difficult = self.difficult_table.get(self.current_level, self.difficult_table[self.max_level])
            player.drop_clock = self._get_drop_clock()

    def _get_drop_clock(self):
        return self.current_difficult["drop_clock"]

    def get_raise_lines(self):
        return self.current_difficult["raise_lines"]

    def get_raise_interval(self):
        return self.current_difficult["raise_interval"]

    def reset(self, player):
        player.drop_clock = GameVar.DROP_CLOCK
        self.current_level = -1
