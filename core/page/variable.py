from enum import Enum

from core.location_layout.main import layout_mg
from core.location_layout.variable import LayoutName
from core.variable import PageTable


class NavigationHandle(str, Enum):
    ENTER = 'ENTER'
    BACKSPACE = 'BACKSPACE'


class GridParameter:
    SINGLE_MENU_LEVEL_ROW = 2
    SINGLE_MENU_LEVEL_COLS = 5

class GridThing:
    LOCK_SWITCH_= 'lock_switch'
    LOCK = 'lock'
    UNLOCK = 'unlock'

class HelpConfig:
    title_items = [
        (LayoutName.HELP_OPTION_TITLE_SL, 0),
        (LayoutName.HELP_OPTION_TITLE_DB, 2),
        (LayoutName.HELP_OPTION_TITLE_EL, 4),
    ]

    # 說明物件與 index 對應
    desc_items = [
        [LayoutName.HELP_OPTION_DESC_SL, 1],
        [LayoutName.HELP_OPTION_DESC_DB, 3],
        [LayoutName.HELP_OPTION_DESC_EL, 5],
    ]

    # hook_x 透明度矩陣
    # 例：title_alpha[hook_x][item_index] 表示對應透明度
    title_alpha = [
        [100, 20, 20],
        [20, 100, 30],
        [20, 20, 100],
    ]

rank_underline = layout_mg.get_item_size(PageTable.RANK, LayoutName.RANK_UNDERLINE)
class RankConfig:
    player_score_pos = rank_underline.width // 30 * (-1)

    extra_pos = {
        0: (0, 0),
        1: (rank_underline.width * 12 // 44, rank_underline.height * 19 // 49),
        2: (rank_underline.width * 26 // 46, rank_underline.height * 21 // 26),
    }

    extra_pos_player = {
        0: (extra_pos[0][0] + rank_underline.width // 20 * (-1), extra_pos[0][1] + rank_underline.height // 40),
        1: (extra_pos[1][0] + rank_underline.width // 20 * (-1), extra_pos[1][1] + rank_underline.height // 40),
        2: (extra_pos[2][0] + rank_underline.width // 20 * (-1), extra_pos[2][1] + rank_underline.height // 40),
    }
