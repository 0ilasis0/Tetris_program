from core.hmi.song import SongVariable
from core.location_layout.base import layout_config
from core.location_layout.manager import LayoutItem, LayoutManager
from core.location_layout.variable import LayoutName, Position, Size
from core.screen.base import screen_mg
from core.screen.variable import ScreenConfig
from core.tetris_game.variable import GameVariable
from core.variable import PageTable, PathConfig

layout_mg = LayoutManager(ScreenConfig.width, ScreenConfig.height)


# 建立虛擬 Pos Size 的物件
class LayoutCollection:
    def __init__(self) -> None:
        # MENU
        self.menu_main = LayoutItem(
            category = PageTable.MENU,
            name = LayoutName.MENU_MAIN,
            size = layout_config.menu_main_size,
        )
        self.menu_rect = LayoutItem(
            category = PageTable.MENU,
            name = LayoutName.MENU_RECT,
            size = Size(self.menu_main.size.width, layout_config.y_gap),
        )

        # SINGLE_MENU
        self.single_menu_main = LayoutItem(
            category = PageTable.SINGLE_MENU,
            name = LayoutName.SINGLE_MENU_MAIN,
            size = Size(
                layout_config.zoom_plus * (GameVariable.SINGLE_MENU_WIDTH_BLOCK * 2 - 1),
                layout_config.zoom_plus * (GameVariable.SINGLE_MENU_HEIGHT_BLOCK * 2 - 1)),
        )
        self.single_menu_rect = LayoutItem(
            category = PageTable.SINGLE_MENU,
            name = LayoutName.SINGLE_MENU_RECT,
            size = Size(layout_config.zoom_plus, layout_config.zoom_plus)
        )
        self.single_menu_number = LayoutItem(
            category = PageTable.SINGLE_MENU,
            name = LayoutName.BASE_NUMBER_BIG,
            size = Size(layout_config.word_big * 2, layout_config.word_big)
        )

        # SINGLE
        self.single_main = LayoutItem(
            category = PageTable.SINGLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_MAIN, 0),
            size = Size(GameVariable.WIDTH_BLOCK * GameVariable.ZOOM_SIZE,
                        GameVariable.HEIGHT_BLOCK * GameVariable.ZOOM_SIZE),
        )
        self.single_slot = LayoutItem(
            category = PageTable.SINGLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_SLOT, 0),
            size = Size(GameVariable.CELL_BLOCK * GameVariable.ZOOM_SIZE,
                        GameVariable.CELL_BLOCK * GameVariable.ZOOM_SIZE),
        )
        self.single_combo = LayoutItem(
            category = PageTable.SINGLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_COMBO, 0),
            size = layout_config.game_combo_size,
        )
        self.single_score = LayoutItem(
            category = PageTable.SINGLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_SCORE, 0),
            size = layout_config.game_score_size,
        )
        self.single_combo_number = LayoutItem(
            category = PageTable.SINGLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_COMBO_NUMBER, 0),
            size = Size(layout_config.word_big * 2, layout_config.word_big * 2),
        )
        self.single_score_number = LayoutItem(
            category = PageTable.SINGLE,
            name = LayoutName.game_suffix_key(LayoutName.BASE_NUMBER_BIG, 0),
            size = Size(layout_config.word * 3, layout_config.word * 3),
        )
        self.single_clock = LayoutItem(
            category = PageTable.SINGLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_CLOCK, 0),
            size = screen_mg.get_image_size(PathConfig.img_clock)
        )
        self.single_clock_min = LayoutItem(
            category = PageTable.SINGLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_CLOCK_MIN, 0),
            size = Size(layout_config.word * 2, layout_config.word * 2)
        )
        self.single_clock_sec = LayoutItem(
            category = PageTable.SINGLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_CLOCK_SEC, 0),
            size = Size(layout_config.word * 2, layout_config.word * 2)
        )
        self.single_ko = LayoutItem(
            category = PageTable.SINGLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_KO, 0),
            size = layout_config.game_ko_size,
        )

        # DOUBLE
        self.double_clock = LayoutItem(
            category = PageTable.DOUBLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_CLOCK, 0),
            size = screen_mg.get_image_size(PathConfig.img_clock)
        )
        self.double_clock_min = LayoutItem(
            category = PageTable.DOUBLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_CLOCK_MIN, 0),
            size = Size(layout_config.word * 2, layout_config.word * 2)
        )
        self.double_clock_sec = LayoutItem(
            category = PageTable.DOUBLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_CLOCK_SEC, 0),
            size = Size(layout_config.word * 2, layout_config.word * 2)
        )

        self.double_1_main = LayoutItem(
            category = PageTable.DOUBLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_MAIN, 0),
            size = Size(GameVariable.WIDTH_BLOCK * GameVariable.ZOOM_SIZE,
                        GameVariable.HEIGHT_BLOCK * GameVariable.ZOOM_SIZE),
            pos  = Position(ScreenConfig.width * 1 // 7, ScreenConfig.height // 6)
        )
        self.double_1_slot = LayoutItem(
            category = PageTable.DOUBLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_SLOT, 0),
            size = Size(GameVariable.CELL_BLOCK * GameVariable.ZOOM_SIZE,
                        GameVariable.CELL_BLOCK * GameVariable.ZOOM_SIZE),
        )
        self.double_1_combo = LayoutItem(
            category = PageTable.DOUBLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_COMBO, 0),
            size = layout_config.game_combo_size,
        )
        self.double_1_score = LayoutItem(
            category = PageTable.DOUBLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_SCORE, 0),
            size = layout_config.game_score_size,
        )
        self.double_1_combo_number = LayoutItem(
            category = PageTable.DOUBLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_COMBO_NUMBER, 0),
            size = Size(layout_config.word_big * 2, layout_config.word_big * 2),
        )
        self.double_1_score_number = LayoutItem(
            category = PageTable.DOUBLE,
            name = LayoutName.game_suffix_key(LayoutName.BASE_NUMBER_BIG, 0),
            size = Size(layout_config.word * 3, layout_config.word * 3),
        )
        self.double_1_ko = LayoutItem(
            category = PageTable.DOUBLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_KO, 0),
            size = layout_config.game_ko_size,
        )

        self.double_2_main = LayoutItem(
            category = PageTable.DOUBLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_MAIN, 1),
            size = Size(GameVariable.WIDTH_BLOCK * GameVariable.ZOOM_SIZE,
                        GameVariable.HEIGHT_BLOCK * GameVariable.ZOOM_SIZE),
        )
        self.double_2_slot = LayoutItem(
            category = PageTable.DOUBLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_SLOT, 1),
            size = Size(GameVariable.CELL_BLOCK * GameVariable.ZOOM_SIZE,
                        GameVariable.CELL_BLOCK * GameVariable.ZOOM_SIZE),
        )
        self.double_2_combo = LayoutItem(
            category = PageTable.DOUBLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_COMBO, 1),
            size = layout_config.game_combo_size,
        )
        self.double_2_score = LayoutItem(
            category = PageTable.DOUBLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_SCORE, 1),
            size = layout_config.game_score_size,
        )
        self.double_2_combo_number = LayoutItem(
            category = PageTable.DOUBLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_COMBO_NUMBER, 1),
            size = Size(layout_config.word_big * 2, layout_config.word_big * 2),
        )
        self.double_2_score_number = LayoutItem(
            category = PageTable.DOUBLE,
            name = LayoutName.game_suffix_key(LayoutName.BASE_NUMBER_BIG, 1),
            size = Size(layout_config.word * 3, layout_config.word * 3),
        )
        self.double_2_ko = LayoutItem(
            category = PageTable.DOUBLE,
            name = LayoutName.game_suffix_key(LayoutName.GAME_KO, 1),
            size = layout_config.game_ko_size,
        )

        # ENDLESS
        self.endless_main = LayoutItem(
            category = PageTable.ENDLESS,
            name = LayoutName.game_suffix_key(LayoutName.GAME_MAIN, 0),
            size = Size(GameVariable.WIDTH_BLOCK * GameVariable.ZOOM_SIZE,
                        GameVariable.HEIGHT_BLOCK * GameVariable.ZOOM_SIZE),
            pos = Position(ScreenConfig.width // 7, ScreenConfig.height // 7)
        )
        self.endless_slot = LayoutItem(
            category = PageTable.ENDLESS,
            name = LayoutName.game_suffix_key(LayoutName.GAME_SLOT, 0),
            size = Size(GameVariable.CELL_BLOCK * GameVariable.ZOOM_SIZE,
                        GameVariable.CELL_BLOCK * GameVariable.ZOOM_SIZE),
        )
        self.endless_combo = LayoutItem(
            category = PageTable.ENDLESS,
            name = LayoutName.game_suffix_key(LayoutName.GAME_COMBO, 0),
            size = layout_config.game_combo_size,
        )
        self.endless_score = LayoutItem(
            category = PageTable.ENDLESS,
            name = LayoutName.game_suffix_key(LayoutName.GAME_SCORE, 0),
            size = layout_config.game_score_size,
        )
        self.endless_combo_number = LayoutItem(
            category = PageTable.ENDLESS,
            name = LayoutName.game_suffix_key(LayoutName.GAME_COMBO_NUMBER, 0),
            size = Size(layout_config.word_big * 2, layout_config.word_big * 2),
        )
        self.endless_score_number = LayoutItem(
            category = PageTable.ENDLESS,
            name = LayoutName.game_suffix_key(LayoutName.BASE_NUMBER_BIG, 0),
            size = Size(layout_config.word * 3, layout_config.word * 3),
        )
        self.endless_clock = LayoutItem(
            category = PageTable.ENDLESS,
            name = LayoutName.game_suffix_key(LayoutName.GAME_CLOCK, 0),
            size = screen_mg.get_image_size(PathConfig.img_clock)
        )
        self.endless_clock_min = LayoutItem(
            category = PageTable.ENDLESS,
            name = LayoutName.game_suffix_key(LayoutName.GAME_CLOCK_MIN, 0),
            size = Size(layout_config.word * 2, layout_config.word * 2)
        )
        self.endless_clock_sec = LayoutItem(
            category = PageTable.ENDLESS,
            name = LayoutName.game_suffix_key(LayoutName.GAME_CLOCK_SEC, 0),
            size = Size(layout_config.word * 2, layout_config.word * 2)
        )
        self.endless_ko = LayoutItem(
            category = PageTable.ENDLESS,
            name = LayoutName.game_suffix_key(LayoutName.GAME_KO, 0),
            size = layout_config.game_ko_size,
        )

        # SONG
        self.song_main = LayoutItem(
            category = PageTable.SONG,
            name = LayoutName.SONG_MAIN,
            size = layout_config.song_main_size,
            pos = Position(ScreenConfig.width // 3, ScreenConfig.height // 2)
        )
        self.song_rect = LayoutItem(
            category = PageTable.SONG,
            name = LayoutName.SONG_RECT,
            size = Size(self.song_main.size.width * 0.9, layout_config.y_gap)
        )
        self.song_name = LayoutItem(
            category = PageTable.SONG,
            name = LayoutName.SONG_NAME,
            size = Size(SongVariable.WIDTH_BLOCK * GameVariable.ZOOM_SIZE,
                        SongVariable.HEIGHT_BLOCK * GameVariable.ZOOM_SIZE)
        )
        self.song_block = LayoutItem(
            category = PageTable.SONG,
            name = LayoutName.SONG_BLOCK,
            size = Size(SongVariable.WIDTH_BLOCK * GameVariable.ZOOM_SIZE,
                        SongVariable.HEIGHT_BLOCK * GameVariable.ZOOM_SIZE)
        )

        # HELP
        self.help_panel = LayoutItem(
            category = PageTable.HELP,
            name = LayoutName.HELP_PANEL,
            size = screen_mg.get_image_size(PathConfig.img_panel[0]),
        )
        self.help_lace = LayoutItem(
            category = PageTable.HELP,
            name = LayoutName.HELP_LACE,
            size = screen_mg.get_image_size(PathConfig.img_lace),
        )
        self.help_option_title_sl = LayoutItem(
            category = PageTable.HELP,
            name = LayoutName.HELP_OPTION_TITLE_SL,
            size = layout_config.help_option_sizes[PageTable.SINGLE.value]["title"],
        )
        self.help_option_title_db = LayoutItem(
            category = PageTable.HELP,
            name = LayoutName.HELP_OPTION_TITLE_DB,
            size = layout_config.help_option_sizes[PageTable.DOUBLE.value]["title"],
        )
        self.help_option_title_el = LayoutItem(
            category = PageTable.HELP,
            name = LayoutName.HELP_OPTION_TITLE_EL,
            size = layout_config.help_option_sizes[PageTable.ENDLESS.value]["title"],
        )
        self.help_option_desc_sl = LayoutItem(
            category = PageTable.HELP,
            name = LayoutName.HELP_OPTION_DESC_SL,
            size = layout_config.help_option_sizes[PageTable.SINGLE.value]["description"],
        )
        self.help_option_desc_db = LayoutItem(
            category = PageTable.HELP,
            name = LayoutName.HELP_OPTION_DESC_DB,
            size = layout_config.help_option_sizes[PageTable.DOUBLE.value]["description"],
        )
        self.help_option_desc_el = LayoutItem(
            category = PageTable.HELP,
            name = LayoutName.HELP_OPTION_DESC_EL,
            size = layout_config.help_option_sizes[PageTable.ENDLESS.value]["description"],
        )

        # RANK
        self.rank_underline = LayoutItem(
            category = PageTable.RANK,
            name = LayoutName.RANK_UNDERLINE,
            size = screen_mg.get_image_size(PathConfig.img_ranking),
        )
        self.rank_frame = LayoutItem(
            category = PageTable.RANK,
            name = LayoutName.RANK_FRAME,
            size = screen_mg.get_image_size(PathConfig.img_frame),
        )
        self.rank_ranking = LayoutItem(
            category = PageTable.RANK,
            name = LayoutName.RANK_RANKING,
            size = layout_config.rank_ranking_size,
        )
        self.rank_sec = LayoutItem(
            category = PageTable.RANK,
            name = LayoutName.RANK_SEC,
            size = layout_config.rank_sec_size,
        )
        self.rank_min = LayoutItem(
            category = PageTable.RANK,
            name = LayoutName.RANK_MIN,
            size = layout_config.rank_min_size,
        )
        self.rank_fraction = LayoutItem(
            category = PageTable.RANK,
            name = LayoutName.RANK_FRACTION,
            size = layout_config.rank_fraction_size,
        )

layout_collection = LayoutCollection()



# MENU
layout_collection.menu_main = layout_mg.add_center(layout_collection.menu_main)
layout_collection.menu_rect = layout_mg.add_inner(
    item    = layout_collection.menu_rect,
    target  = layout_collection.menu_main,
    align   = 'left_tp',
    gap_x   = layout_config.word * 0.25 * (-1)
)

# SINGLE_MENU
layout_collection.single_menu_main = layout_mg.add_center(layout_collection.single_menu_main)
layout_collection.single_menu_rect = layout_mg.add_inner(
    item    = layout_collection.single_menu_rect,
    target  = layout_collection.single_menu_main,
    align   = 'left_tp',
)
layout_collection.single_menu_number = layout_mg.add_center(
    item    = layout_collection.single_menu_number,
    target  = layout_collection.single_menu_rect,
    gap_x   = layout_collection.single_menu_number.size.width // 5,
    gap_y   = layout_collection.single_menu_number.size.height // 5,
)

# SINGLE
layout_collection.single_main = layout_mg.add_center(layout_collection.single_main)
layout_collection.single_slot = layout_mg.add_right_of(
    item    = layout_collection.single_slot,
    target  = layout_collection.single_main,
    gap_x   = GameVariable.ZOOM_SIZE * 2,
    align   = 'top'
)
layout_collection.single_combo = layout_mg.add_right_of(
    item    = layout_collection.single_combo,
    target  = layout_collection.single_main,
    gap_x   = GameVariable.ZOOM_SIZE * 2,
    align   = 'center'
)
layout_collection.single_score = layout_mg.add_right_of(
    item    = layout_collection.single_score,
    target  = layout_collection.single_main,
    gap_x   = GameVariable.ZOOM_SIZE * 2,
    align   = 'bottom'
)
layout_collection.single_combo_number = layout_mg.add_below(
    item    = layout_collection.single_combo_number,
    target  = layout_collection.single_combo,
    gap     = GameVariable.ZOOM_SIZE,
    align   = 'center'
)
layout_collection.single_score_number = layout_mg.add_below(
    item    = layout_collection.single_score_number,
    target  = layout_collection.single_score,
    gap     = GameVariable.ZOOM_SIZE,
    align   = 'center'
)
layout_collection.single_clock = layout_mg.add_left_of(
    item    = layout_collection.single_clock,
    target  = layout_collection.single_main,
    gap_x   = GameVariable.ZOOM_SIZE * (-1),
    align   = 'top'
)
layout_collection.single_clock_min = layout_mg.add_inner(
    item    = layout_collection.single_clock_min,
    target  = layout_collection.single_clock,
    gap_x   = layout_collection.single_clock.size.width // 8,
    gap_y   = layout_collection.single_clock.size.height // 8 * (-1),
    align   = 'left_bt'
)
layout_collection.single_clock_sec = layout_mg.add_inner(
    item    = layout_collection.single_clock_sec,
    target  = layout_collection.single_clock,
    gap_x   = layout_collection.single_clock.size.width // 8 * (-1),
    gap_y   = layout_collection.single_clock.size.height // 8 * (-1),
    align   = 'right_bt'
)
layout_collection.single_ko = layout_mg.add_left_of(
    item    = layout_collection.single_ko,
    target  = layout_collection.single_main,
    gap_x   = GameVariable.ZOOM_SIZE * (-1),
    gap_y   = GameVariable.ZOOM_SIZE,
    align   = 'center'
)

# DOUBLE
layout_collection.double_clock = layout_mg.add_center(
    item    = layout_collection.double_clock,
    gap_y   = GameVariable.ZOOM_SIZE * 10,
)
layout_collection.double_clock_min = layout_mg.add_inner(
    item    = layout_collection.double_clock_min,
    target  = layout_collection.double_clock,
    gap_x   = layout_collection.double_clock.size.width // 8,
    gap_y   = layout_collection.double_clock.size.height // 8 * (-1),
    align   = 'left_bt'
)
layout_collection.double_clock_sec = layout_mg.add_inner(
    item    = layout_collection.double_clock_sec,
    target  = layout_collection.double_clock,
    gap_x   = layout_collection.double_clock.size.width // 8 * (-1),
    gap_y   = layout_collection.double_clock.size.height // 8 * (-1),
    align   = 'right_bt'
)

layout_collection.double_1_main = layout_mg.add_item(layout_collection.double_1_main)
layout_collection.double_1_slot = layout_mg.add_right_of(
    item    = layout_collection.double_1_slot,
    target  = layout_collection.double_1_main,
    gap_x   = GameVariable.ZOOM_SIZE * 2,
    align   = 'top'
)
layout_collection.double_1_combo = layout_mg.add_right_of(
    item    = layout_collection.double_1_combo,
    target  = layout_collection.double_1_main,
    gap_x   = GameVariable.ZOOM_SIZE * 2,
    align   = 'center'
)
layout_collection.double_1_score = layout_mg.add_right_of(
    item    = layout_collection.double_1_score,
    target  = layout_collection.double_1_main,
    gap_x   = GameVariable.ZOOM_SIZE * 2,
    align   = 'bottom'
)
layout_collection.double_1_combo_number = layout_mg.add_below(
    item    = layout_collection.double_1_combo_number,
    target  = layout_collection.double_1_combo,
    gap     = GameVariable.ZOOM_SIZE,
    align   = 'center'
)
layout_collection.double_1_score_number = layout_mg.add_below(
    item    = layout_collection.double_1_score_number,
    target  = layout_collection.double_1_score,
    gap     = GameVariable.ZOOM_SIZE,
    align   = 'center'
)
layout_collection.double_1_ko = layout_mg.add_left_of(
    item    = layout_collection.double_1_ko,
    target  = layout_collection.double_1_main,
    gap_x   = GameVariable.ZOOM_SIZE * (-1),
    gap_y   = GameVariable.ZOOM_SIZE,
    align   = 'center'
)

layout_collection.double_2_main = layout_mg.add_symmetric(
    item = layout_collection.double_2_main,
    target = layout_collection.double_1_main,
    axis = 'vertical',
    gap_x = (layout_collection.double_2_slot.size.width + GameVariable.ZOOM_SIZE * 2) * (-1)
)
layout_collection.double_2_slot = layout_mg.add_right_of(
    item    = layout_collection.double_2_slot,
    target  = layout_collection.double_2_main,
    gap_x   = GameVariable.ZOOM_SIZE * 2,
    align   = 'top'
)
layout_collection.double_2_combo = layout_mg.add_right_of(
    item    = layout_collection.double_2_combo,
    target  = layout_collection.double_2_main,
    gap_x   = GameVariable.ZOOM_SIZE * 2,
    align   = 'center'
)
layout_collection.double_2_score = layout_mg.add_right_of(
    item    = layout_collection.double_2_score,
    target  = layout_collection.double_2_main,
    gap_x   = GameVariable.ZOOM_SIZE * 2,
    align   = 'bottom'
)
layout_collection.double_2_combo_number = layout_mg.add_below(
    item    = layout_collection.double_2_combo_number,
    target  = layout_collection.double_2_combo,
    gap     = GameVariable.ZOOM_SIZE,
    align   = 'center'
)
layout_collection.double_2_score_number = layout_mg.add_below(
    item    = layout_collection.double_2_score_number,
    target  = layout_collection.double_2_score,
    gap     = GameVariable.ZOOM_SIZE,
    align   = 'center'
)
layout_collection.double_2_ko = layout_mg.add_left_of(
    item    = layout_collection.double_2_ko,
    target  = layout_collection.double_2_main,
    gap_x   = GameVariable.ZOOM_SIZE * (-1),
    gap_y   = GameVariable.ZOOM_SIZE,
    align   = 'center'
)

# ENDLESS
layout_collection.endless_main = layout_mg.add_center(layout_collection.endless_main)
layout_collection.endless_slot = layout_mg.add_right_of(
    item    = layout_collection.endless_slot,
    target  = layout_collection.endless_main,
    gap_x   = GameVariable.ZOOM_SIZE * 2,
    align   = 'top'
)
layout_collection.endless_combo = layout_mg.add_right_of(
    item    = layout_collection.endless_combo,
    target  = layout_collection.endless_main,
    gap_x   = GameVariable.ZOOM_SIZE * 2,
    align   = 'center'
)
layout_collection.endless_score = layout_mg.add_right_of(
    item    = layout_collection.endless_score,
    target  = layout_collection.endless_main,
    gap_x   = GameVariable.ZOOM_SIZE * 2,
    align   = 'bottom'
)
layout_collection.endless_combo_number = layout_mg.add_below(
    item    = layout_collection.endless_combo_number,
    target  = layout_collection.endless_combo,
    gap     = GameVariable.ZOOM_SIZE,
    align   = 'center'
)
layout_collection.endless_score_number = layout_mg.add_below(
    item    = layout_collection.endless_score_number,
    target  = layout_collection.endless_score,
    gap     = GameVariable.ZOOM_SIZE,
    align   = 'center'
)
layout_collection.endless_clock = layout_mg.add_left_of(
    item    = layout_collection.endless_clock,
    target  = layout_collection.endless_main,
    gap_x   = GameVariable.ZOOM_SIZE * (-1),
    align   = 'top'
)
layout_collection.endless_clock_min = layout_mg.add_inner(
    item    = layout_collection.endless_clock_min,
    target  = layout_collection.endless_clock,
    gap_x   = layout_collection.endless_clock.size.width // 8,
    gap_y   = layout_collection.endless_clock.size.height // 8 * (-1),
    align   = 'left_bt'
)
layout_collection.endless_clock_sec = layout_mg.add_inner(
    item    = layout_collection.endless_clock_sec,
    target  = layout_collection.endless_clock,
    gap_x   = layout_collection.endless_clock.size.width // 8 * (-1),
    gap_y   = layout_collection.endless_clock.size.height // 8 * (-1),
    align   = 'right_bt'
)
layout_collection.endless_ko = layout_mg.add_left_of(
    item    = layout_collection.endless_ko,
    target  = layout_collection.endless_main,
    gap_x   = GameVariable.ZOOM_SIZE * (-1),
    gap_y   = GameVariable.ZOOM_SIZE,
    align   = 'center'
)

# SONG
song_main = layout_mg.add_item(layout_collection.song_main)
song_name = layout_mg.add_right_of(
    item    = layout_collection.song_name,
    target  = song_main,
    gap_x   = GameVariable.ZOOM_SIZE,
    align   = 'top'
)
song_block = layout_mg.add_below(
    item    = layout_collection.song_block,
    target  = song_name,
    gap     = GameVariable.ZOOM_SIZE,
    align   = 'left'
)
song_rect = layout_mg.add_inner(
    item    = layout_collection.song_rect,
    target  = song_main,
    align   = 'left_tp',
    gap_x   = GameVariable.ZOOM_SIZE * 0.35 * (-1),
)

# HELP
help_panel = layout_mg.add_center(
    item = layout_collection.help_panel,
    gap_y = ScreenConfig.height * 3 // 5 * (-1)
    )
help_lace = layout_mg.add_center(
    item = layout_collection.help_lace,
    gap_y = ScreenConfig.height // 6
    )
help_option_title_sl = layout_mg.add_inner(
    item = layout_collection.help_option_title_sl,
    target = help_panel,
    align = 'left_tp',
    gap_x = layout_collection.help_panel.size.width // 12 + layout_collection.help_option_title_sl.size.width // 4,
    gap_y = layout_collection.help_panel.size.height // 11,
    )
help_option_title_db = layout_mg.add_inner(
    item = layout_collection.help_option_title_db,
    target = help_panel,
    align = 'center_tp',
    gap_y = layout_collection.help_panel.size.height // 11,
    )
help_option_title_el = layout_mg.add_inner(
    item = layout_collection.help_option_title_el,
    target = help_panel,
    align = 'right_tp',
    gap_x = (layout_collection.help_panel.size.width // 12 + layout_collection.help_option_title_sl.size.width // 4) * (-1),
    gap_y = layout_collection.help_panel.size.height // 11,
    )
help_option_desc_sl = layout_mg.add_inner(
    item = layout_collection.help_option_desc_sl,
    target = help_lace,
    gap_x = layout_collection.help_panel.size.width // 16,
    gap_y = layout_collection.help_panel.size.height // 3,
    )
help_option_desc_db = layout_mg.add_inner(
    item = layout_collection.help_option_desc_db,
    target = help_lace,
    gap_x = layout_collection.help_panel.size.width // 16,
    gap_y = layout_collection.help_panel.size.height // 3,
    )
help_option_desc_el = layout_mg.add_inner(
    item = layout_collection.help_option_desc_el,
    target = help_lace,
    gap_x = layout_collection.help_panel.size.width // 16,
    gap_y = layout_collection.help_panel.size.height // 3,
    )

# RANK
rank_underline = layout_mg.add_center(item = layout_collection.rank_underline)
rank_frame = layout_mg.add_center(item = layout_collection.rank_frame)
rank_ranking = layout_mg.add_inner(
    item = layout_collection.rank_ranking,
    target = rank_underline,
    align = 'left_tp',
    gap_x = 0,
    gap_y = rank_underline.size.height // 8 * (-1),
)
rank_min = layout_mg.add_inner(
    item = layout_collection.rank_min,
    target = rank_underline,
    align = 'left_tp',
    gap_x = rank_underline.size.width // 6,
    gap_y = rank_underline.size.height // 16 * (-1),
)
rank_sec = layout_mg.add_inner(
    item = layout_collection.rank_sec,
    target = rank_underline,
    align = 'left_tp',
    gap_x = rank_underline.size.width * 2 // 8,
    gap_y = rank_underline.size.height // 16 * (-1),
)
rank_fraction = layout_mg.add_inner(
    item = layout_collection.rank_fraction,
    target = rank_underline,
    align = 'left_tp',
    gap_x = rank_underline.size.width * 3 // 8,
    gap_y = rank_underline.size.height // 16 * (-1),
)
