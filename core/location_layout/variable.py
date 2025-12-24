from enum import Enum

from core.screen.variable import ScreenConfig


class LocationConfig:
    def __init__(self) -> None:
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
        if val == 0: return 0
        return int(val * ScreenConfig.RATIO)

location_config = LocationConfig()



class LayoutName(str, Enum):
    # BASE
    BASE_NUMBER_BIG     = 'base_number_big'

    # BACKGROUND
    MENU_BG             = 'menu_bg'
    SINGLE_BG           = 'single_bg'
    SINGLE_MENU_BG      = 'single_menu_bg'
    DOUBLE_BG           = 'double_bg'
    ENDLESS_BG          = 'endless_bg'
    SONG_BG             = 'song_bg'
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

    # SONG
    SONG_MAIN           = 'song_main'
    SONG_RECT           = 'song_rect'
    SONG_NAME           = 'song_name'
    SONG_BLOCK          = 'song_block'

    # HELP
    HELP_PANEL          = 'help_panel'
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


    def game_suffix_key(base, player_index: int) -> str:
        """回傳例如 game_main_1, game_main_2"""
        return f"{base.value}_{player_index + 1}"
