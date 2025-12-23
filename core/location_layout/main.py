from core.hmi.song import SongVariable
from core.location_layout.base import LayoutItem, layout_config
from core.location_layout.manager import LayoutManager, LayoutNameManage
from core.location_layout.variable import LayoutName
from core.screen.variable import ScreenConfig
from core.tetris_game.variable import GameVariable
from core.variable import PageTable, Position, Size


# 建立虛擬 Pos Size 的物件
class LayoutCollection:
    def __init__(self, lay_mg: LayoutManager) -> None:
        self.lay_mg = lay_mg  # 將工具存起來供內部使用

        # --- 依序組裝各個頁面 ---
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
        """ 簡化 LayoutItem 的建立 """
        return LayoutItem(
            category = category,
            name = name,
            size = size,
            pos = pos or Position(0, 0)
        )

    def _setup_menu(self):
        # MENU
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
                layout_config.menu_main_size,
            )
        )
        self.menu_rect = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.MENU,
                LayoutName.MENU_RECT,
                Size(self.menu_main.size.width, layout_config.y_gap),
            ),
            target = self.menu_main,
            align = 'left_tp',
            gap_x = layout_config.word * 0.25 * (-1)
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
                    layout_config.zoom_plus * (GameVariable.SINGLE_MENU_WIDTH_BLOCK * 2 - 1),
                    layout_config.zoom_plus * (GameVariable.SINGLE_MENU_HEIGHT_BLOCK * 2 - 1)
                ),
            )
        )
        self.single_menu_rect = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.SINGLE_MENU,
                LayoutName.SINGLE_MENU_RECT,
                Size(layout_config.zoom_plus, layout_config.zoom_plus)
            ),
            target = self.single_menu_main,
            align = 'left_tp',
        )
        # 注意：這裡使用 rect 的 size 進行計算，因為上面已經 add_inner 過了，rect 的 size 是確定的
        self.single_menu_number = self.lay_mg.add_center(
            item = self._create_item(
                PageTable.SINGLE_MENU,
                LayoutName.BASE_NUMBER_BIG,
                Size(layout_config.word_big * 2, layout_config.word_big)
            ),
            target = self.single_menu_rect,
            gap_x = self.single_menu_rect.size.width // 5,
            gap_y = self.single_menu_rect.size.height // 5,
        )

    def _setup_single_game(self):
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
                Size(GameVariable.WIDTH_BLOCK * GameVariable.ZOOM_SIZE,
                     GameVariable.HEIGHT_BLOCK * GameVariable.ZOOM_SIZE),
            )
        )
        self.single_slot = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_SLOT, 0),
                Size(GameVariable.CELL_BLOCK * GameVariable.ZOOM_SIZE,
                     GameVariable.CELL_BLOCK * GameVariable.ZOOM_SIZE),
            ),
            target = self.single_main,
            gap_x = GameVariable.ZOOM_SIZE * 2,
            align = 'top'
        )
        self.single_combo = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_COMBO, 0),
                layout_config.game_combo_size,
            ),
            target = self.single_main,
            gap_x = GameVariable.ZOOM_SIZE * 2,
            align = 'center'
        )
        self.single_score = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_SCORE, 0),
                layout_config.game_score_size,
            ),
            target = self.single_main,
            gap_x = GameVariable.ZOOM_SIZE * 2,
            align = 'bottom'
        )
        self.single_combo_number = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_COMBO_NUMBER, 0),
                Size(layout_config.word_big * 2, layout_config.word_big * 2),
            ),
            target = self.single_combo,
            gap = GameVariable.ZOOM_SIZE,
            align = 'center'
        )
        self.single_score_number = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.BASE_NUMBER_BIG, 0),
                Size(layout_config.word * 3, layout_config.word * 3),
            ),
            target = self.single_score,
            gap = GameVariable.ZOOM_SIZE,
            align = 'center'
        )
        self.single_clock = self.lay_mg.add_left_of(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK, 0),
                Size(ScreenConfig.width // 8.25, ScreenConfig.height // 5),
            ),
            target = self.single_main,
            gap_x = GameVariable.ZOOM_SIZE * (-1),
            align = 'top'
        )
        self.single_clock_min = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK_MIN, 0),
                Size(layout_config.word * 2, layout_config.word * 2)
            ),
            target = self.single_clock,
            gap_x = self.single_clock.size.width // 8,
            gap_y = self.single_clock.size.height // 8 * (-1),
            align = 'left_bt'
        )
        self.single_clock_sec = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK_SEC, 0),
                Size(layout_config.word * 2, layout_config.word * 2)
            ),
            target = self.single_clock,
            gap_x = self.single_clock.size.width // 8 * (-1),
            gap_y = self.single_clock.size.height // 8 * (-1),
            align = 'right_bt'
        )
        self.single_ko = self.lay_mg.add_left_of(
            item = self._create_item(
                PageTable.SINGLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_KO, 0),
                layout_config.game_ko_size,
            ),
            target = self.single_main,
            gap_x = GameVariable.ZOOM_SIZE * (-1),
            gap_y = GameVariable.ZOOM_SIZE,
            align = 'center'
        )

    def _setup_double_game(self):
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
                Size(ScreenConfig.width // 8.25, ScreenConfig.height // 5),
            ),
            gap_y = GameVariable.ZOOM_SIZE * 10,
        )
        self.double_clock_min = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK_MIN, 0),
                Size(layout_config.word * 2, layout_config.word * 2)
            ),
            target = self.double_clock,
            gap_x = self.double_clock.size.width // 8,
            gap_y = self.double_clock.size.height // 8 * (-1),
            align = 'left_bt'
        )
        self.double_clock_sec = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK_SEC, 0),
                Size(layout_config.word * 2, layout_config.word * 2)
            ),
            target = self.double_clock,
            gap_x = self.double_clock.size.width // 8 * (-1),
            gap_y = self.double_clock.size.height // 8 * (-1),
            align = 'right_bt'
        )

        # DOUBLE - Player 1
        self.double_1_main = self.lay_mg.add_item(
            self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_MAIN, 0),
                Size(GameVariable.WIDTH_BLOCK * GameVariable.ZOOM_SIZE,
                     GameVariable.HEIGHT_BLOCK * GameVariable.ZOOM_SIZE),
                Position(ScreenConfig.width * 1 // 7, ScreenConfig.height // 6)
            )
        )
        self.double_1_slot = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_SLOT, 0),
                Size(GameVariable.CELL_BLOCK * GameVariable.ZOOM_SIZE,
                     GameVariable.CELL_BLOCK * GameVariable.ZOOM_SIZE),
            ),
            target = self.double_1_main,
            gap_x = GameVariable.ZOOM_SIZE * 2,
            align = 'top'
        )
        self.double_1_combo = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_COMBO, 0),
                layout_config.game_combo_size,
            ),
            target = self.double_1_main,
            gap_x = GameVariable.ZOOM_SIZE * 2,
            align = 'center'
        )
        self.double_1_score = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_SCORE, 0),
                layout_config.game_score_size,
            ),
            target = self.double_1_main,
            gap_x = GameVariable.ZOOM_SIZE * 2,
            align = 'bottom'
        )
        self.double_1_combo_number = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_COMBO_NUMBER, 0),
                Size(layout_config.word_big * 2, layout_config.word_big * 2),
            ),
            target = self.double_1_combo,
            gap = GameVariable.ZOOM_SIZE,
            align = 'center'
        )
        self.double_1_score_number = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.BASE_NUMBER_BIG, 0),
                Size(layout_config.word * 3, layout_config.word * 3),
            ),
            target = self.double_1_score,
            gap = GameVariable.ZOOM_SIZE,
            align = 'center'
        )
        self.double_1_ko = self.lay_mg.add_left_of(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_KO, 0),
                layout_config.game_ko_size,
            ),
            target = self.double_1_main,
            gap_x = GameVariable.ZOOM_SIZE * (-1),
            gap_y = GameVariable.ZOOM_SIZE,
            align = 'center'
        )

        # DOUBLE - Player 2 (Symmetric to P1)
        # 這裡需要先創建物件，但為了計算 Symmetric 的 gap_x，我們需要先知道 slot 的大小
        # 所以先建立好物件
        p2_slot_size = Size(GameVariable.CELL_BLOCK * GameVariable.ZOOM_SIZE,
                            GameVariable.CELL_BLOCK * GameVariable.ZOOM_SIZE)

        self.double_2_main = self.lay_mg.add_symmetric(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_MAIN, 1),
                Size(GameVariable.WIDTH_BLOCK * GameVariable.ZOOM_SIZE,
                     GameVariable.HEIGHT_BLOCK * GameVariable.ZOOM_SIZE),
            ),
            target = self.double_1_main,
            axis = 'vertical',
            gap_x = (p2_slot_size.width + GameVariable.ZOOM_SIZE * 2) * (-1)
        )
        self.double_2_slot = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_SLOT, 1),
                p2_slot_size,
            ),
            target = self.double_2_main,
            gap_x = GameVariable.ZOOM_SIZE * 2,
            align = 'top'
        )
        self.double_2_combo = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_COMBO, 1),
                layout_config.game_combo_size,
            ),
            target = self.double_2_main,
            gap_x = GameVariable.ZOOM_SIZE * 2,
            align = 'center'
        )
        self.double_2_score = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_SCORE, 1),
                layout_config.game_score_size,
            ),
            target = self.double_2_main,
            gap_x = GameVariable.ZOOM_SIZE * 2,
            align = 'bottom'
        )
        self.double_2_combo_number = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_COMBO_NUMBER, 1),
                Size(layout_config.word_big * 2, layout_config.word_big * 2),
            ),
            target = self.double_2_combo,
            gap = GameVariable.ZOOM_SIZE,
            align = 'center'
        )
        self.double_2_score_number = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.BASE_NUMBER_BIG, 1),
                Size(layout_config.word * 3, layout_config.word * 3),
            ),
            target = self.double_2_score,
            gap = GameVariable.ZOOM_SIZE,
            align = 'center'
        )
        self.double_2_ko = self.lay_mg.add_left_of(
            item = self._create_item(
                PageTable.DOUBLE,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_KO, 1),
                layout_config.game_ko_size,
            ),
            target = self.double_2_main,
            gap_x = GameVariable.ZOOM_SIZE * (-1),
            gap_y = GameVariable.ZOOM_SIZE,
            align = 'center'
        )

    def _setup_endless_game(self):
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
                Size(GameVariable.WIDTH_BLOCK * GameVariable.ZOOM_SIZE,
                     GameVariable.HEIGHT_BLOCK * GameVariable.ZOOM_SIZE),
                Position(ScreenConfig.width // 7, ScreenConfig.height // 7) # add_center 會覆蓋這個 pos，但保留結構
            )
        )
        self.endless_slot = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_SLOT, 0),
                Size(GameVariable.CELL_BLOCK * GameVariable.ZOOM_SIZE,
                     GameVariable.CELL_BLOCK * GameVariable.ZOOM_SIZE),
            ),
            target = self.endless_main,
            gap_x = GameVariable.ZOOM_SIZE * 2,
            align = 'top'
        )
        self.endless_combo = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_COMBO, 0),
                layout_config.game_combo_size,
            ),
            target = self.endless_main,
            gap_x = GameVariable.ZOOM_SIZE * 2,
            align = 'center'
        )
        self.endless_score = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_SCORE, 0),
                layout_config.game_score_size,
            ),
            target = self.endless_main,
            gap_x = GameVariable.ZOOM_SIZE * 2,
            align = 'bottom'
        )
        self.endless_combo_number = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_COMBO_NUMBER, 0),
                Size(layout_config.word_big * 2, layout_config.word_big * 2),
            ),
            target = self.endless_combo,
            gap = GameVariable.ZOOM_SIZE,
            align = 'center'
        )
        self.endless_score_number = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.BASE_NUMBER_BIG, 0),
                Size(layout_config.word * 3, layout_config.word * 3),
            ),
            target = self.endless_score,
            gap = GameVariable.ZOOM_SIZE,
            align = 'center'
        )
        self.endless_clock = self.lay_mg.add_left_of(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK, 0),
                Size(ScreenConfig.width // 8.25, ScreenConfig.height // 5),
            ),
            target = self.endless_main,
            gap_x = GameVariable.ZOOM_SIZE * (-1),
            align = 'top'
        )
        self.endless_clock_min = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK_MIN, 0),
                Size(layout_config.word * 2, layout_config.word * 2)
            ),
            target = self.endless_clock,
            gap_x = self.endless_clock.size.width // 8,
            gap_y = self.endless_clock.size.height // 8 * (-1),
            align = 'left_bt'
        )
        self.endless_clock_sec = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK_SEC, 0),
                Size(layout_config.word * 2, layout_config.word * 2)
            ),
            target = self.endless_clock,
            gap_x = self.endless_clock.size.width // 8 * (-1),
            gap_y = self.endless_clock.size.height // 8 * (-1),
            align = 'right_bt'
        )
        self.endless_ko = self.lay_mg.add_left_of(
            item = self._create_item(
                PageTable.ENDLESS,
                LayoutNameManage.game_suffix_key(LayoutName.GAME_KO, 0),
                layout_config.game_ko_size,
            ),
            target = self.endless_main,
            gap_x = GameVariable.ZOOM_SIZE * (-1),
            gap_y = GameVariable.ZOOM_SIZE,
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
                Position(ScreenConfig.width // 3, ScreenConfig.height // 2)
            )
        )
        self.song_name = self.lay_mg.add_right_of(
            item = self._create_item(
                PageTable.SONG,
                LayoutName.SONG_NAME,
                Size(SongVariable.WIDTH_BLOCK * GameVariable.ZOOM_SIZE,
                     SongVariable.HEIGHT_BLOCK * GameVariable.ZOOM_SIZE),
            ),
            target = self.song_main,
            gap_x = GameVariable.ZOOM_SIZE,
            align = 'top'
        )
        self.song_block = self.lay_mg.add_below(
            item = self._create_item(
                PageTable.SONG,
                LayoutName.SONG_BLOCK,
                Size(SongVariable.WIDTH_BLOCK * GameVariable.ZOOM_SIZE,
                     SongVariable.HEIGHT_BLOCK * GameVariable.ZOOM_SIZE),
            ),
            target = self.song_name,
            gap = GameVariable.ZOOM_SIZE,
            align = 'left'
        )
        self.song_rect = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.SONG,
                LayoutName.SONG_RECT,
                Size(self.song_main.size.width * 0.9, layout_config.y_gap),
            ),
            target = self.song_main,
            align = 'left_tp',
            gap_x = GameVariable.ZOOM_SIZE * 0.35 * (-1),
        )

    def _setup_help(self):
        # HELP
        self.help_bg = self.lay_mg.add_item(
            self._create_item(
                PageTable.HELP,
                LayoutName.HELP_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0),
            )
        )
        self.help_panel = self.lay_mg.add_center(
            item = self._create_item(
                PageTable.HELP,
                LayoutName.HELP_PANEL,
                Size(ScreenConfig.width // 1.359, ScreenConfig.height // 8),
            ),
            gap_y = ScreenConfig.height * 3 // 5 * (-1)
        )
        self.help_lace = self.lay_mg.add_center(
            item = self._create_item(
                PageTable.HELP,
                LayoutName.HELP_LACE,
                Size(ScreenConfig.width // 1.667, ScreenConfig.height // 1.708),
            ),
            gap_y = ScreenConfig.height // 6
        )
        self.help_option_title_sl = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.HELP,
                LayoutName.HELP_OPTION_TITLE_SL,
                layout_config.help_option_sizes[PageTable.SINGLE.value]["title"],
            ),
            target = self.help_panel,
            align = 'left_tp',
            gap_x = self.help_panel.size.width // 12 + layout_config.help_option_sizes[PageTable.SINGLE.value]["title"].width // 4,
            gap_y = self.help_panel.size.height // 11,
        )
        self.help_option_title_db = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.HELP,
                LayoutName.HELP_OPTION_TITLE_DB,
                layout_config.help_option_sizes[PageTable.DOUBLE.value]["title"],
            ),
            target = self.help_panel,
            align = 'center_tp',
            gap_y = self.help_panel.size.height // 11,
        )
        self.help_option_title_el = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.HELP,
                LayoutName.HELP_OPTION_TITLE_EL,
                layout_config.help_option_sizes[PageTable.ENDLESS.value]["title"],
            ),
            target = self.help_panel,
            align = 'right_tp',
            gap_x = (self.help_panel.size.width // 12 + layout_config.help_option_sizes[PageTable.SINGLE.value]["title"].width // 4) * (-1), # 注意這裡原程式是取 sl 的 size 做計算
            gap_y = self.help_panel.size.height // 11,
        )
        self.help_option_desc_sl = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.HELP,
                LayoutName.HELP_OPTION_DESC_SL,
                layout_config.help_option_sizes[PageTable.SINGLE.value]["description"],
            ),
            target = self.help_lace,
            gap_x = self.help_panel.size.width // 16,
            gap_y = self.help_panel.size.height // 3,
        )
        self.help_option_desc_db = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.HELP,
                LayoutName.HELP_OPTION_DESC_DB,
                layout_config.help_option_sizes[PageTable.DOUBLE.value]["description"],
            ),
            target = self.help_lace,
            gap_x = self.help_panel.size.width // 16,
            gap_y = self.help_panel.size.height // 3,
        )
        self.help_option_desc_el = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.HELP,
                LayoutName.HELP_OPTION_DESC_EL,
                layout_config.help_option_sizes[PageTable.ENDLESS.value]["description"],
            ),
            target = self.help_lace,
            gap_x = self.help_panel.size.width // 16,
            gap_y = self.help_panel.size.height // 3,
        )

    def _setup_rank(self):
        # RANK
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
                Size(ScreenConfig.width // 1.335, ScreenConfig.height // 1.747),
            )
        )
        self.rank_frame = self.lay_mg.add_center(
            item = self._create_item(
                PageTable.RANK,
                LayoutName.RANK_FRAME,
                Size(ScreenConfig.width // 1.327, ScreenConfig.height // 1.3432),
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
            gap_y = self.rank_underline.size.height // 8 * (-1),
        )
        self.rank_min = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.RANK,
                LayoutName.RANK_MIN,
                layout_config.rank_min_size,
            ),
            target = self.rank_underline,
            align = 'left_tp',
            gap_x = self.rank_underline.size.width // 6,
            gap_y = self.rank_underline.size.height // 16 * (-1),
        )
        self.rank_sec = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.RANK,
                LayoutName.RANK_SEC,
                layout_config.rank_sec_size,
            ),
            target = self.rank_underline,
            align = 'left_tp',
            gap_x = self.rank_underline.size.width * 2 // 8,
            gap_y = self.rank_underline.size.height // 16 * (-1),
        )
        self.rank_fraction = self.lay_mg.add_inner(
            item = self._create_item(
                PageTable.RANK,
                LayoutName.RANK_FRACTION,
                layout_config.rank_fraction_size,
            ),
            target = self.rank_underline,
            align = 'left_tp',
            gap_x = self.rank_underline.size.width * 3 // 8,
            gap_y = self.rank_underline.size.height // 16 * (-1),
        )

layout_mg = LayoutManager(ScreenConfig.width, ScreenConfig.height)
layout_collection = LayoutCollection(layout_mg)
