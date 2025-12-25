from core.hmi.song import SongVariable
from core.location_layout.base import LayoutItem, layout_config
from core.location_layout.manager import LayoutManager, LayoutNameManage
from core.location_layout.variable import LayoutName, location_config
from core.screen.variable import ScreenConfig
from core.tetris_game.variable import GameVariable
from core.variable import PageTable, Position, Size


# 建立虛擬 Pos Size 的物件
class LayoutCollection:
    def __init__(self, lay_mg: LayoutManager) -> None:
        self.lay_mg = lay_mg
        self.reload_setup()

    def reload_setup(self):
        self.lay_mg.clear_items()
        self.lay_mg.update_screen_size(ScreenConfig.width, ScreenConfig.height)

        self._setup_menu()
        self._setup_single_menu()
        self._setup_single_game()
        self._setup_double_game()
        self._setup_endless_game()
        self._setup_song()
        self._setup_help()
        self._setup_rank()

    @staticmethod
    def _create_item(category, name, size, pos = None):
        return LayoutItem(
            category = category,
            name = name,
            size = size,
            pos = pos or Position(0, 0)
        )

    def _setup_menu(self):
        # MENU
        # 背景：維持全螢幕，不縮放
        self.menu_bg = self.lay_mg.add_item(
            self._create_item(
                PageTable.MENU,
                LayoutName.MENU_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0),
            )
        )
        self.menu_main = self.lay_mg.add_center(
            self._create_item(
                PageTable.MENU,
                LayoutName.MENU_MAIN,
                layout_config.menu_main_size, # 文字大小通常由 font module 決定，這裡維持原樣
            )
        )
        self.menu_rect = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.MENU,
                LayoutName.MENU_RECT,
                Size(self.menu_main.size.width, location_config.y_gap),
            ),
            target = self.menu_main,
            align = 'left_tp',
            gap_x = location_config.scale(-10)
        )

    def _setup_single_menu(self):
        # SINGLE_MENU
        self.single_menu_bg = self.lay_mg.add_item(
            self._create_item(
                PageTable.SINGLE_MENU,
                LayoutName.SINGLE_MENU_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0),
            )
        )
        self.single_menu_main = self.lay_mg.add_center(
            self._create_item(
                PageTable.SINGLE_MENU,
                LayoutName.SINGLE_MENU_MAIN,
                Size(
                    location_config.zoom_plus * (GameVariable.SINGLE_MENU_WIDTH_BLOCK * 2 - 1),
                    location_config.zoom_plus * (GameVariable.SINGLE_MENU_HEIGHT_BLOCK * 2 - 1)
                ),
            )
        )
        self.single_menu_rect = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.SINGLE_MENU,
                LayoutName.SINGLE_MENU_RECT,
                Size(location_config.zoom_plus, location_config.zoom_plus)
            ),
            target = self.single_menu_main,
            align = 'left_tp',
        )
        self.single_menu_number = self.lay_mg.add_center(
            item = self._create_item(
                PageTable.SINGLE_MENU,
                LayoutName.BASE_NUMBER_BIG,
                Size(location_config.word_big * 2, location_config.word_big)
            ),
            target = self.single_menu_rect,
            gap_x = location_config.scale(26),
            gap_y = location_config.scale(26),
        )

    def _setup_single_game(self):
        # SINGLE - Standard Items
        self.single_bg = self.lay_mg.add_item(
            self._create_item(
                PageTable.SINGLE,
                LayoutName.SINGLE_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0),
            )
        )
        self.single_main = self.lay_mg.add_center(
            self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_MAIN, 0),
                Size(GameVariable.WIDTH_BLOCK * location_config.zoom,
                     GameVariable.HEIGHT_BLOCK * location_config.zoom),
            )
        )

        # 假設 ZOOM_SIZE 是 32
        zoom_val = location_config.zoom
        zoom_x2  = location_config.zoom * 2

        self.single_slot = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_SLOT, 0),
                Size(GameVariable.CELL_BLOCK * zoom_val,
                     GameVariable.CELL_BLOCK * zoom_val),
            ),
            target = self.single_main,
            gap_x = zoom_x2,
            align = 'top'
        )
        self.single_combo = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_COMBO, 0),
                layout_config.game_combo_size,
            ),
            target = self.single_main,
            gap_x = zoom_x2,
            align = 'center'
        )
        self.single_score = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_SCORE, 0),
                layout_config.game_score_size,
            ),
            target = self.single_main,
            gap_x = zoom_x2,
            align = 'bottom'
        )
        self.single_combo_number = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_COMBO_NUMBER, 0),
                Size(location_config.word_big * 2, location_config.word_big * 2),
            ),
            target = self.single_combo,
            gap = zoom_val,
            align = 'center'
        )
        self.single_score_number = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.BASE_NUMBER_BIG, 0),
                Size(location_config.word * 3, location_config.word * 3),
            ),
            target = self.single_score,
            gap = zoom_val,
            align = 'center'
        )

        clock_size = Size(location_config.scale(240), location_config.scale(216))
        clock_w_div_8 = location_config.scale(30)
        clock_h_div_8 = location_config.scale(27)

        self.single_clock = self.lay_mg.add_left_of(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK, 0),
                clock_size,
            ),
            target = self.single_main,
            gap_x = zoom_val * (-1),
            align = 'top'
        )
        self.single_clock_min = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK_MIN, 0),
                Size(location_config.word * 2, location_config.word * 2)
            ),
            target = self.single_clock,
            gap_x = clock_w_div_8,
            gap_y = clock_h_div_8 * (-1),
            align = 'left_bt'
        )
        self.single_clock_sec = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK_SEC, 0),
                Size(location_config.word * 2, location_config.word * 2)
            ),
            target = self.single_clock,
            gap_x = clock_w_div_8 * (-1),
            gap_y = clock_h_div_8 * (-1),
            align = 'right_bt'
        )
        self.single_ko = self.lay_mg.add_left_of(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_KO, 0),
                layout_config.game_ko_size,
            ),
            target = self.single_main,
            gap_x = zoom_val * (-1),
            gap_y = zoom_val,
            align = 'center'
        )

    def _setup_double_game(self):
        zoom_val = location_config.zoom
        zoom_x2  = location_config.zoom * 2
        clock_size = Size(location_config.scale(240), location_config.scale(216))
        clock_w_div_8 = location_config.scale(30)
        clock_h_div_8 = location_config.scale(27)

        # DOUBLE - Common
        self.double_bg = self.lay_mg.add_item(
            self._create_item(
                PageTable.DOUBLE,
                LayoutName.DOUBLE_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0),
            )
        )
        self.double_clock = self.lay_mg.add_center(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK, 0),
                clock_size,
            ),
            gap_y = location_config.scale(320),
        )
        self.double_clock_min = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK_MIN, 0),
                Size(location_config.word * 2, location_config.word * 2)
            ),
            target = self.double_clock,
            gap_x = clock_w_div_8,
            gap_y = clock_h_div_8 * (-1),
            align = 'left_bt'
        )
        self.double_clock_sec = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK_SEC, 0),
                Size(location_config.word * 2, location_config.word * 2)
            ),
            target = self.double_clock,
            gap_x = clock_w_div_8 * (-1),
            gap_y = clock_h_div_8 * (-1),
            align = 'right_bt'
        )

        # DOUBLE - Player 1
        self.double_1_main = self.lay_mg.add_item(
            self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_MAIN, 0),
                Size(GameVariable.WIDTH_BLOCK * zoom_val,
                     GameVariable.HEIGHT_BLOCK * zoom_val),
                Position(location_config.scale(282), location_config.scale(180))
            )
        )
        self.double_1_slot = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_SLOT, 0),
                Size(GameVariable.CELL_BLOCK * zoom_val,
                     GameVariable.CELL_BLOCK * zoom_val),
            ),
            target = self.double_1_main,
            gap_x = zoom_x2,
            align = 'top'
        )
        self.double_1_combo = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_COMBO, 0),
                layout_config.game_combo_size,
            ),
            target = self.double_1_main,
            gap_x = zoom_x2,
            align = 'center'
        )
        self.double_1_score = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_SCORE, 0),
                layout_config.game_score_size,
            ),
            target = self.double_1_main,
            gap_x = zoom_x2,
            align = 'bottom'
        )
        self.double_1_combo_number = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_COMBO_NUMBER, 0),
                Size(location_config.word_big * 2, location_config.word_big * 2),
            ),
            target = self.double_1_combo,
            gap = zoom_val,
            align = 'center'
        )
        self.double_1_score_number = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.BASE_NUMBER_BIG, 0),
                Size(location_config.word * 3, location_config.word * 3),
            ),
            target = self.double_1_score,
            gap = zoom_val,
            align = 'center'
        )
        self.double_1_ko = self.lay_mg.add_left_of(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_KO, 0),
                layout_config.game_ko_size,
            ),
            target = self.double_1_main,
            gap_x = zoom_val * (-1),
            gap_y = zoom_val,
            align = 'center'
        )

        # DOUBLE - Player 2
        p2_slot_size = Size(GameVariable.CELL_BLOCK * zoom_val,
                            GameVariable.CELL_BLOCK * zoom_val)

        self.double_2_main = self.lay_mg.add_symmetric(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_MAIN, 1),
                Size(GameVariable.WIDTH_BLOCK * zoom_val,
                     GameVariable.HEIGHT_BLOCK * zoom_val),
            ),
            target = self.double_1_main,
            axis = 'vertical',
            gap_x = (p2_slot_size.width + zoom_x2) * (-1)
        )
        self.double_2_slot = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_SLOT, 1),
                p2_slot_size,
            ),
            target = self.double_2_main,
            gap_x = zoom_x2,
            align = 'top'
        )
        self.double_2_combo = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_COMBO, 1),
                layout_config.game_combo_size,
            ),
            target = self.double_2_main,
            gap_x = zoom_x2,
            align = 'center'
        )
        self.double_2_score = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_SCORE, 1),
                layout_config.game_score_size,
            ),
            target = self.double_2_main,
            gap_x = zoom_x2,
            align = 'bottom'
        )
        self.double_2_combo_number = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_COMBO_NUMBER, 1),
                Size(location_config.word_big * 2, location_config.word_big * 2),
            ),
            target = self.double_2_combo,
            gap = zoom_val,
            align = 'center'
        )
        self.double_2_score_number = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.BASE_NUMBER_BIG, 1),
                Size(location_config.word * 3, location_config.word * 3),
            ),
            target = self.double_2_score,
            gap = zoom_val,
            align = 'center'
        )
        self.double_2_ko = self.lay_mg.add_left_of(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_KO, 1),
                layout_config.game_ko_size,
            ),
            target = self.double_2_main,
            gap_x = zoom_val * (-1),
            gap_y = zoom_val,
            align = 'center'
        )

    def _setup_endless_game(self):
        zoom_val = location_config.zoom
        zoom_x2  = location_config.zoom * 2
        clock_size = Size(location_config.scale(240), location_config.scale(216))
        clock_w_div_8 = location_config.scale(30)
        clock_h_div_8 = location_config.scale(27)

        # ENDLESS
        self.endless_bg = self.lay_mg.add_item(
            self._create_item(
                PageTable.ENDLESS,
                LayoutName.ENDLESS_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0),
            )
        )
        self.endless_main = self.lay_mg.add_center(
            self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_MAIN, 0),
                Size(GameVariable.WIDTH_BLOCK * zoom_val,
                     GameVariable.HEIGHT_BLOCK * zoom_val),
                Position(location_config.scale(282), location_config.scale(154))
            )
        )
        self.endless_slot = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_SLOT, 0),
                Size(GameVariable.CELL_BLOCK * zoom_val,
                     GameVariable.CELL_BLOCK * zoom_val),
            ),
            target = self.endless_main,
            gap_x = zoom_x2,
            align = 'top'
        )
        self.endless_combo = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_COMBO, 0),
                layout_config.game_combo_size,
            ),
            target = self.endless_main,
            gap_x = zoom_x2,
            align = 'center'
        )
        self.endless_score = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_SCORE, 0),
                layout_config.game_score_size,
            ),
            target = self.endless_main,
            gap_x = zoom_x2,
            align = 'bottom'
        )
        self.endless_combo_number = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_COMBO_NUMBER, 0),
                Size(location_config.word_big * 2, location_config.word_big * 2),
            ),
            target = self.endless_combo,
            gap = zoom_val,
            align = 'center'
        )
        self.endless_score_number = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.BASE_NUMBER_BIG, 0),
                Size(location_config.word * 3, location_config.word * 3),
            ),
            target = self.endless_score,
            gap = zoom_val,
            align = 'center'
        )
        self.endless_clock = self.lay_mg.add_left_of(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK, 0),
                clock_size,
            ),
            target = self.endless_main,
            gap_x = zoom_val * (-1),
            align = 'top'
        )
        self.endless_clock_min = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK_MIN, 0),
                Size(location_config.word * 2, location_config.word * 2)
            ),
            target = self.endless_clock,
            gap_x = clock_w_div_8,
            gap_y = clock_h_div_8 * (-1),
            align = 'left_bt'
        )
        self.endless_clock_sec = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK_SEC, 0),
                Size(location_config.word * 2, location_config.word * 2)
            ),
            target = self.endless_clock,
            gap_x = clock_w_div_8 * (-1),
            gap_y = clock_h_div_8 * (-1),
            align = 'right_bt'
        )
        self.endless_ko = self.lay_mg.add_left_of(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_KO, 0),
                layout_config.game_ko_size,
            ),
            target = self.endless_main,
            gap_x = zoom_val * (-1),
            gap_y = zoom_val,
            align = 'center'
        )

    def _setup_song(self):
        # SONG
        self.song_bg = self.lay_mg.add_item(
            self._create_item(
                PageTable.SONG,
                LayoutName.SONG_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0),
            )
        )
        self.song_main = self.lay_mg.add_item(
            self._create_item(
                PageTable.SONG,
                LayoutName.SONG_MAIN,
                layout_config.song_main_size,
                Position(location_config.scale(660), location_config.scale(540))
            )
        )
        self.song_name = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.SONG,
                LayoutName.SONG_NAME,
                Size(SongVariable.WIDTH_BLOCK * location_config.zoom,
                     SongVariable.HEIGHT_BLOCK * location_config.zoom),
            ),
            target = self.song_main,
            gap_x = location_config.zoom,
            align = 'top'
        )
        self.song_block = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.SONG,
                LayoutName.SONG_BLOCK,
                Size(SongVariable.WIDTH_BLOCK * location_config.zoom,
                     SongVariable.HEIGHT_BLOCK * location_config.zoom),
            ),
            target = self.song_name,
            gap = location_config.zoom,
            align = 'left'
        )
        self.song_rect = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.SONG,
                LayoutName.SONG_RECT,
                Size(self.song_main.size.width * 0.9, location_config.y_gap),
            ),
            target = self.song_main,
            align = 'left_tp',
            gap_x = location_config.scale(-11),
        )

    def _setup_help(self):
        # HELP
        panel_w = location_config.scale(1457)
        panel_h = location_config.scale(135)

        self.help_bg = self.lay_mg.add_item(
            self._create_item(
                PageTable.HELP,
                LayoutName.HELP_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0),
            )
        )
        for i, name in enumerate(LayoutName.HELP_PANEL.serial_list):
            added_item = self.lay_mg.add_center(
                item = self._create_item(
                    PageTable.HELP,
                    name,
                    Size(panel_w, panel_h),
                ),
                gap_y = location_config.scale(-648)
            )
            if i == 0:
                self.help_panel = added_item
        # self.help_panel = self.lay_mg.add_center(
        #     item = self._create_item(
        #         PageTable.HELP,
        #         LayoutName.HELP_PANEL,
        #         Size(panel_w, panel_h),
        #     ),
        #     gap_y = location_config.scale(-648)
        # )
        self.help_lace = self.lay_mg.add_center(
            item = self._create_item(
                PageTable.HELP,
                LayoutName.HELP_LACE,
                Size(location_config.scale(1188), location_config.scale(632)),
            ),
            gap_y = location_config.scale(180)
        )


        gap_x_base = location_config.scale(121)
        gap_y_val = location_config.scale(12)

        self.help_option_title_sl = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.HELP,
                LayoutName.HELP_OPTION_TITLE_SL,
                layout_config.help_option_sizes[PageTable.SINGLE.value]["title"],
            ),
            target = self.help_panel,
            align = 'left_tp',
            gap_x = gap_x_base + layout_config.help_option_sizes[PageTable.SINGLE.value]["title"].width // 4,
            gap_y = gap_y_val,
        )
        self.help_option_title_db = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.HELP,
                LayoutName.HELP_OPTION_TITLE_DB,
                layout_config.help_option_sizes[PageTable.DOUBLE.value]["title"],
            ),
            target = self.help_panel,
            align = 'center_tp',
            gap_y = gap_y_val,
        )
        self.help_option_title_el = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.HELP,
                LayoutName.HELP_OPTION_TITLE_EL,
                layout_config.help_option_sizes[PageTable.ENDLESS.value]["title"],
            ),
            target = self.help_panel,
            align = 'right_tp',
            gap_x = (gap_x_base + layout_config.help_option_sizes[PageTable.SINGLE.value]["title"].width // 4) * (-1),
            gap_y = gap_y_val,
        )

        # Desc Gaps
        desc_gap_x = location_config.scale(91)
        desc_gap_y = location_config.scale(45)

        self.help_option_desc_sl = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.HELP,
                LayoutName.HELP_OPTION_DESC_SL,
                layout_config.help_option_sizes[PageTable.SINGLE.value]["description"],
            ),
            target = self.help_lace,
            gap_x = desc_gap_x,
            gap_y = desc_gap_y,
        )
        self.help_option_desc_db = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.HELP,
                LayoutName.HELP_OPTION_DESC_DB,
                layout_config.help_option_sizes[PageTable.DOUBLE.value]["description"],
            ),
            target = self.help_lace,
            gap_x = desc_gap_x,
            gap_y = desc_gap_y,
        )
        self.help_option_desc_el = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.HELP,
                LayoutName.HELP_OPTION_DESC_EL,
                layout_config.help_option_sizes[PageTable.ENDLESS.value]["description"],
            ),
            target = self.help_lace,
            gap_x = desc_gap_x,
            gap_y = desc_gap_y,
        )

    def _setup_rank(self):
        # RANK
        underline_w = location_config.scale(1483)
        underline_h = location_config.scale(618)

        self.rank_bg = self.lay_mg.add_item(
            self._create_item(
                PageTable.RANK,
                LayoutName.RANK_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0),
            )
        )
        self.rank_underline = self.lay_mg.add_center(
            item = self._create_item(
                PageTable.RANK,
                LayoutName.RANK_UNDERLINE,
                Size(underline_w, underline_h),
            )
        )
        self.rank_frame = self.lay_mg.add_center(
            item = self._create_item(
                PageTable.RANK,
                LayoutName.RANK_FRAME,
                Size(location_config.scale(1492), location_config.scale(804)),
            )
        )
        self.rank_ranking = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.RANK,
                LayoutName.RANK_RANKING,
                layout_config.rank_ranking_size,
            ),
            target = self.rank_underline,
            align = 'left_tp',
            gap_x = 0,
            gap_y = location_config.scale(77) * (-1),
        )

        gap_y_common = location_config.scale(39) * (-1)

        self.rank_min = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.RANK,
                LayoutName.RANK_MIN,
                layout_config.rank_min_size,
            ),
            target = self.rank_underline,
            align = 'left_tp',
            gap_x = location_config.scale(247), # 1483 / 6
            gap_y = gap_y_common,
        )
        self.rank_sec = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.RANK,
                LayoutName.RANK_SEC,
                layout_config.rank_sec_size,
            ),
            target = self.rank_underline,
            align = 'left_tp',
            gap_x = location_config.scale(370), # 1483 * 2 / 8
            gap_y = gap_y_common,
        )
        self.rank_fraction = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.RANK,
                LayoutName.RANK_FRACTION,
                layout_config.rank_fraction_size,
            ),
            target = self.rank_underline,
            align = 'left_tp',
            gap_x = location_config.scale(556), # 1483 * 3 / 8
            gap_y = gap_y_common,
        )

layout_mg = LayoutManager(ScreenConfig.width, ScreenConfig.height)
layout_collection = LayoutCollection(layout_mg)
