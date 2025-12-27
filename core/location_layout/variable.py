from enum import Enum
from typing import TYPE_CHECKING

from core.screen.variable import ScreenConfig


class LocationConfig:
    def __init__(self) -> None:
        self.reload_setup()

    def reload_setup(self):
        self.zoom       = self.scale(32)
        self.zoom_plus  = self.scale(128)
        self.word       = self.scale(38)
        self.word_mini  = self.scale(19)
        self.word_big   = self.scale(57)
        self.y_gap      = self.scale(57)
        self.y_gap_mini = self.scale(29)
        self.y_gap_big  = self.scale(86)

    def scale(self, val: int) -> int:
        """ 將設計稿數值 (1980x1080) 轉換為當前螢幕數值 """
        return int(val * ScreenConfig.RATIO)

location_config = LocationConfig()


class LayoutName(str, Enum):
    """
        自定義的 Enum，支援自動產生序列名稱
        定義格式: 名稱 = ('字串值', 數量)
        如果沒有寫數量，預設為 1
    """
    # 這段 "給 VS Code 看的" 宣告，實際不會跑
    if TYPE_CHECKING:
        serial_list: list[str]
        count: int

    def __new__(cls, content, count = 1):
        # 建立字串物件 (這一步保證了它依然是 str)
        obj = str.__new__(cls, content)

        # 設定 Enum 的實際值 (必須是字串)
        obj._value_ = content

        # 將數量存為這個成員的屬性
        obj.count = count

        # 順便直接生成 list 存起來，這樣以後直接讀屬性就好，不用再運算
        if count > 1:
            obj.serial_list = [f"{content}_{i}" for i in range(count)]
        else:
            obj.serial_list = [content]

        return obj

    ''' --- 定義區域 ---  '''
    # BASE
    BASE_NUMBER_BIG     = 'base_number_big'


    # BACKGROUND
    MENU_BG             = 'menu_bg'
    SINGLE_BG           = 'single_bg'
    SINGLE_MENU_BG      = 'single_menu_bg'
    DOUBLE_BG           = 'double_bg'
    ENDLESS_BG          = 'endless_bg'
    SYS_CONFIG_BG       = 'sys_config_bg'
    HELP_BG             = 'help_bg'
    RANK_BG             = 'rank_bg'

    # MENU
    MENU_MAIN           = 'menu_main'
    MENU_RECT           = 'menu_rect'

    # GAME
    SINGLE_MENU_MAIN    = 'single_menu_main'
    SINGLE_MENU_RECT    = 'single_menu_rect'

    GAME_MAIN           = "game_main"
    GAME_SLOT           = "game_slot"
    GAME_COMBO          = "game_combo"
    GAME_SCORE          = "game_score"
    GAME_COMBO_NUMBER   = "game_combo_number"
    GAME_CLOCK          = "game_clock"
    GAME_CLOCK_MIN      = "game_clock_min"
    GAME_CLOCK_SEC      = "game_clock_sec"
    GAME_KO             = "game_ko"

    # SYS_CONFIG
    SYS_SONG_MAIN           = 'sys_song_main'
    SYS_SONG_RECT           = 'sys_song_rect'
    SYS_SONG_NAME           = 'sys_song_name'
    SYS_SONG_BLOCK          = 'sys_song_block'
    SYS_WINDOW_SCALE        = 'sys_window_scale'

    # HELP
    HELP_PANEL          = ('help_panel', 3)
    HELP_LACE           = 'help_lace'
    HELP_OPTION_TITLE_SL= 'help_option_title_sl'
    HELP_OPTION_TITLE_DB= 'help_option_title_db'
    HELP_OPTION_TITLE_EL= 'help_option_title_el'
    HELP_OPTION_DESC_SL = 'help_option_desc_sl'
    HELP_OPTION_DESC_DB = 'help_option_desc_db'
    HELP_OPTION_DESC_EL = 'help_option_desc_el'

    # RANK
    RANK_UNDERLINE      = 'rank_underline'
    RANK_FRAME          = 'rank_frame'
    RANK_RANKING        = 'rank_ranking'
    RANK_SEC            = 'rank_sec'
    RANK_MIN            = 'rank_min'
    RANK_FRACTION       = 'rank_fraction'
