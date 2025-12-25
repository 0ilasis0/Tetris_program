import pygame
from core.base import ClockTimer, central_mg
from core.hmi.rank import rank_mg
from core.keyboard.base import keyboard_mg
from core.tetris_game.manager import TetrisCore, player1
from core.tetris_game.mode.double import main_double
from core.tetris_game.mode.endless import main_endless
from core.tetris_game.mode.single import main_single
from core.tetris_game.variable import GameState
from core.variable import PageTable

# 生成timer
clock_game = ClockTimer()

def main_tetris_game(player: TetrisCore):
    # 若是 STATE_GAMEOVER 自動跳回前一頁面
    if player.state == GameState.STATE_GAMEOVER:
        keyboard_mg.imitate_button_event(pygame.K_BACKSPACE)

    # 遊戲FPS依據
    dt = central_mg.get_dt()
    player.drop_timer += dt

    # 一般機制(掉落、方塊碰撞、分數更新...)
    if player.drop_timer > player.drop_clock:
        if not player.field.check_collision(player.current_tetromino, 0, 1):
            player.current_tetromino.y += 1
        else:
            player.freeze()
        player.drop_timer = 0



class IndividualTetris:
    def __init__(self) -> None:
        # 建立PageTable對TetrisGame映射表map
        self.mode_map = {}
        self._set()

        self.player: TetrisCore = player1
        self.min = 0
        self.sec = 0

    def _set(self):
        for table in PageTable:
            method_name = table.name
            if hasattr(self, method_name):
                self.mode_map[table] = getattr(self, method_name)

    def main_process(self, category, player,  min, sec) -> None:
        self.player = player
        self.min = min
        self.sec = sec

        func = self.mode_map.get(category)
        if func:
            func()
        else:
            raise ValueError(f"未知的 category 模式: {category}")

    def SINGLE(self):
        main_single(self.player, self.sec, self.min)

    def DOUBLE(self):
        main_double()

    def ENDLESS(self):
        main_endless(self.player, self.sec, self.min)

        # 遊戲結束進行排名計算
        if self.player.state == GameState.STATE_GAMEOVER:
            rank_mg.add_score(self.min, int(self.sec), self.player.score)

individual_tetris = IndividualTetris()
