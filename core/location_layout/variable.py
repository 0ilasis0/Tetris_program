from dataclasses import dataclass
from enum import Enum

from core.screen.variable import ScreenConfig


class BaseParameter:
    zoom            = ScreenConfig.tetris_cell
    zoom_plus       = ScreenConfig.tetris_cell * 4
    word            = ScreenConfig.word
    word_mini       = round(word * 0.5)
    word_big        = round(word * 1.5)
    y_gap           = round(word * 1.5)
    y_gap_mini      = round(word_mini * 1.5)
    y_gap_big       = round(word_big * 1.5)



@dataclass
class Size:
    width: int
    height: int

@dataclass
class Position:
    x: int
    y: int

    @classmethod
    def zero(cls):
        return cls(0,0)



class LayoutName(str, Enum):
    # BASE
    BASE_NUMBER_BIG     = 'base_number_big'

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
