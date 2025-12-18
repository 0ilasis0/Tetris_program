from core.tetris_game.manager import TetrisCore


def main_single(player: TetrisCore, sec: int, min: int):
    total_time = sec + min * 60

    # 第一次觸發初始化
    if not getattr(player.level_mg, "last_time", -1):
        player.level_mg.last_time = total_time

    # 判斷是否超過間隔
    if total_time - player.level_mg.last_time >= player.level_mg.get_raise_interval():
        player.attack_mg.raise_bottom(player, player.level_mg.get_raise_lines())
        player.level_mg.last_time = total_time   # 更新觸發時間
