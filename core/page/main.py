from core.base import central_mg
from core.debug import dbg
from core.font.font_manager import fonts_mg
from core.hmi.rank import rank_mg
from core.hmi.song import song_mg
from core.hmi.variable import SongVariable
from core.keyboard.base import keyboard_mg
from core.location_layout.base import layout_config
from core.location_layout.main import layout_mg
from core.location_layout.variable import LayoutName, Position, Size
from core.page.base import page_mg
from core.page.navigation import BasePageNavigation
from core.page.tree_path import tree_path_table
from core.page.variable import HelpConfig, RankConfig
from core.screen.base import screen_mg
from core.screen.drawing import draw_mg
from core.tetris_game.main import (TetrisCore, game_clock, individual_tetris,
                                   main_tetris_game)
from core.tetris_game.manager import player1, player2
from core.tetris_game.variable import BaseVariable, GameVariable, RankVariable
from core.variable import JsonPath, PageTable, PathConfig, colors


def main_page():
    page_function = page_mg.keymaps[page_mg.current_page]

    # 決定是否載入當前boot
    if page_mg.current_boot == page_mg.current_page:
        page_mg.boot_page(page_mg.current_boot)
        page_mg.current_boot = None

    # 執行當前頁面主循環
    if page_function is not None:
        page_function()
    else:
        dbg.log(f"no load {page_mg.current_page}")



class PageNavigation(BasePageNavigation):
    def __init__(self) -> None:
        super().__init__(tree_path_table, page_mg, keyboard_mg, draw_mg, fonts_mg)

    def MENU(self):
        # 初始化螢幕
        self.window_all_init(True, False)
        draw_mg.maps_clear(PageTable.MENU)
        self.base_common(PageTable.MENU)

        # 畫玩家選擇方塊
        menu_rect = layout_mg.get_item(PageTable.MENU, LayoutName.MENU_RECT)

        draw_mg.add_form(
            category  = PageTable.MENU,
            name        = LayoutName.MENU_RECT,
            shape       = 'rect',
            pos         = Position(menu_rect.pos.x, menu_rect.pos.y + keyboard_mg.hook_y * layout_config.y_gap),
            size        = layout_mg.get_item_size(PageTable.MENU, LayoutName.MENU_RECT),
            color       = colors[7],
            hollow      = 5,
            fixed       = False,
        )
        draw_mg.current_draw_dynamic = [PageTable.MENU]

    def SINGLE_MENU(self):
        self.window_all_init(True, False)
        draw_mg.maps_clear(PageTable.SINGLE_MENU)
        self.base_common(PageTable.SINGLE_MENU)

        # 畫玩家選擇關卡方塊
        single_menu_rect = layout_mg.get_item(PageTable.SINGLE_MENU, LayoutName.SINGLE_MENU_RECT)

        draw_mg.add_form(
            category  = PageTable.SINGLE_MENU,
            name        = LayoutName.SINGLE_MENU_RECT,
            shape       = 'rect',
            pos         = Position(
                single_menu_rect.pos.x + (keyboard_mg.hook_x * single_menu_rect.size.width * 2),
                single_menu_rect.pos.y + (keyboard_mg.hook_y * single_menu_rect.size.width * 2)
            ),
            size        = layout_mg.get_item_size(PageTable.SINGLE_MENU, LayoutName.SINGLE_MENU_RECT),
            color       = colors[12],
            hollow      = 0,
            fixed       = False,
        )

        draw_mg.current_draw_static = [PageTable.SINGLE_MENU]
        draw_mg.current_draw_dynamic = [PageTable.SINGLE_MENU]

    def SINGLE(self):
        self.game_common(PageTable.SINGLE, player1)

    def DOUBLE(self):
        self.game_common(PageTable.DOUBLE, player1)
        self.game_common(PageTable.DOUBLE, player2)

    def ENDLESS(self):
        self.game_common(PageTable.ENDLESS, player1)

    def SONG(self):
        # --------- 核心 ---------
        song_mg.main_process()

        self.window_all_init(True, False)
        draw_mg.maps_clear(PageTable.SONG)
        self.base_common(PageTable.SONG)

        # 畫音量大小方塊
        song_block = layout_mg.get_item(PageTable.SONG, LayoutName.SONG_BLOCK)
        draw_mg.add_form(
            category  = PageTable.SONG,
            name        = LayoutName.SONG_BLOCK,
            shape       = 'rect',
            pos         = layout_mg.get_item_pos(PageTable.SONG, LayoutName.SONG_BLOCK),
            size        = Size(layout_config.zoom * song_mg.state.get(JsonPath.VOLUME.value), song_block.size.height),
            color       = colors[5],
            hollow      = 0,
            fixed       = False,
        )
        # 畫玩家選擇方塊
        song_rect = layout_mg.get_item(PageTable.SONG, LayoutName.SONG_RECT)
        draw_mg.add_form(
            category  = PageTable.SONG,
            name        = LayoutName.SONG_RECT,
            shape       = 'rect',
            pos         = Position(song_rect.pos.x, song_rect.pos.y + keyboard_mg.hook_y * layout_config.y_gap),
            size        = layout_mg.get_item_size(PageTable.SONG, LayoutName.SONG_RECT),
            color       = colors[7],
            hollow      = 5,
            fixed       = False,
        )

        # 歌曲名稱
        fonts_mg.renew_font(
            category    = PageTable.SONG,
            index       = song_mg.state.get(JsonPath.SELECT_SONG.value) % (song_mg.files_length + SongVariable.RANDOM_SPACE),
            pos         = layout_mg.get_item_pos(PageTable.SONG, LayoutName.SONG_NAME),
            fixed       = False
        )

        draw_mg.current_draw_static = [PageTable.SONG]
        draw_mg.current_draw_dynamic = [PageTable.SONG]

    def HELP(self):
        self.window_all_init(True, False, True)
        self.base_common(PageTable.HELP)

        # 玩家選擇 img_panel
        screen_mg.add_image(PageTable.HELP, LayoutName.HELP_PANEL, PathConfig.img_panel[keyboard_mg.hook_x])

        # 標題文字
        for i, (layout_name, idx) in enumerate(HelpConfig.title_items):
            fonts_mg.renew_font(
                category  = PageTable.HELP,
                index     = idx,
                pos       = layout_mg.get_item_pos(PageTable.HELP, layout_name),
                fixed     = False,
                alpha_pec = HelpConfig.title_alpha[keyboard_mg.hook_x][i],
                direction = 'horizontal',
            )

        # 遊戲說明文字
        fonts_mg.renew_font(
            category  = PageTable.HELP,
            index     = HelpConfig.desc_items[keyboard_mg.hook_x][1],
            pos       = layout_mg.get_item_pos(PageTable.HELP, HelpConfig.desc_items[keyboard_mg.hook_x][0]),
            fixed     = False,
        )

    def RANK(self):
        self.base_common(PageTable.RANK)

    def EXIT(self):
        central_mg.running = False

    def game_common(self, category, player: TetrisCore = player1):
        ''' 統一使用SINGLE '''
        if player == player1:
            self.window_all_init(True, False)
            draw_mg.maps_clear(category)

        self.base_common(category)

        # 共同核心
        main_tetris_game(player = player)
        # timer
        min, sec = game_clock.get_min_sec()
        # 不同mode的核心
        individual_tetris.main_process(category, player, min, sec)


        # 畫場地內固定方塊
        player.draw.draw_cells(
            draw_mgr    = draw_mg,
            category    = category,
            cells       = player.field.grid,
            pos         = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.GAME_MAIN)),
            fixed       = False,
            )
        # 畫player移動方塊
        player.draw.draw_cells(
            draw_mgr    = draw_mg,
            category    = category,
            cells       = player.current_tetromino.tetromino_to_matrix(player.current_tetromino),
            pos         = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.GAME_MAIN)),
            other_x     = player.current_tetromino.x * player.field.zoom,
            other_y     = player.current_tetromino.y * player.field.zoom,
            fixed       = False,
        )
        # 畫player暫存方塊
        player.draw.draw_cells(
            draw_mgr    = draw_mg,
            category    = category,
            cells       = player.current_tetromino.tetromino_to_matrix(player.store_slot.current_slot),
            pos         = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.GAME_SLOT)),
            fixed       = False,
        )
        # score number
        fonts_mg.renew_font(
            category    = category,
            index       = player.score,
            pos         = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.BASE_NUMBER_BIG)),
            fixed       = False,
        )
        # combo / combo number
        if player.combo > 0:
            fonts_mg.renew_font(
                category    = category,
                index       = GameVariable.MAX_SCORE + GameVariable.MAX_COMBO + GameVariable.MAX_KO_COUNT,
                pos         = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.GAME_COMBO)),
                fixed       = False,
            )
            fonts_mg.renew_font(
                category    = category,
                index       = player.combo + GameVariable.MAX_SCORE,
                pos         = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.GAME_COMBO_NUMBER)),
                fixed       = False,
            )
        # ko顯示
        if player.attack_mg.ko_counter > 0:
            fonts_mg.renew_font(
                category    = category,
                index       = GameVariable.MAX_SCORE + GameVariable.MAX_COMBO + (player.attack_mg.ko_counter - 1),
                pos         = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.GAME_KO)),
                fixed       = False,
            )
        # timer_clock
        if player == player1:
            fonts_mg.renew_font(
                category    = category,
                index       = min,
                pos         = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.GAME_CLOCK_MIN)),
                fixed       = False,
            )
            fonts_mg.renew_font(
                category    = category,
                index       = int(sec),
                pos         = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.GAME_CLOCK_SEC)),
                fixed       = False,
            )

        draw_mg.current_draw_static = [category]
        draw_mg.current_draw_dynamic = [category]

page_navigation = PageNavigation()





class PageBoot():
    ''' 只會在初次進入當前頁面時載入一次下次刷屏不會進來，但下次進入頁面又會進來 '''
    def MENU(self):
        page_navigation.window_all_init()
        draw_mg.maps_clear(PageTable.MENU, True)

        # 目錄文字
        fonts_mg.renew_font(
            category = PageTable.MENU,
            index   = 0,
            pos     = layout_mg.get_item_pos(PageTable.MENU, LayoutName.MENU_MAIN),
        )

    def SINGLE_MENU(self):
        page_navigation.window_all_init()

        # 畫基本關卡方塊
        single_menu_rect = layout_mg.get_item(PageTable.SINGLE_MENU, LayoutName.SINGLE_MENU_RECT)
        for height_block in range(GameVariable.SINGLE_MENU_HEIGHT_BLOCK):
            for width_block in range(GameVariable.SINGLE_MENU_WIDTH_BLOCK):
                draw_mg.add_form(
                    category  = PageTable.SINGLE_MENU,
                    name        = LayoutName.SINGLE_MENU_RECT,
                    shape       = 'rect',
                    pos         = Position(
                        single_menu_rect.pos.x + (width_block * single_menu_rect.size.width * 2),
                        single_menu_rect.pos.y + (height_block * single_menu_rect.size.height * 2)
                    ),
                    size        = layout_mg.get_item_size(PageTable.SINGLE_MENU, LayoutName.SINGLE_MENU_RECT),
                    color       = colors[3],
                    hollow      = 5,
                )
        # 畫關卡數字
        single_menu_number = layout_mg.get_item(PageTable.SINGLE_MENU, LayoutName.BASE_NUMBER_BIG)
        for height_level in range(GameVariable.SINGLE_MENU_HEIGHT_BLOCK):
            for width_level in range(GameVariable.SINGLE_MENU_WIDTH_BLOCK):
                fonts_mg.renew_font(
                    category = PageTable.SINGLE_MENU,
                    index   = width_level + height_level * GameVariable.SINGLE_MENU_WIDTH_BLOCK + 1,
                    pos     = Position(
                        single_menu_number.pos.x + (width_level * single_menu_rect.size.width * 2),
                        single_menu_number.pos.y + (height_level * single_menu_rect.size.height * 2)
                    ),
                )

    def SINGLE(self):
        page_navigation.window_all_init()
        # 初始化遊戲狀態
        player1.reset(attack_sw = True, level_sw = False)
        player1.level_mg.update_level(player = player1, level = player1.level_mg.current_level)

        self.game_common(PageTable.SINGLE, player1)

    def DOUBLE(self):
        page_navigation.window_all_init()
        # 初始化遊戲狀態
        player1.reset()
        player2.reset()
        self.game_common(PageTable.DOUBLE, player1)
        self.game_common(PageTable.DOUBLE, player2)
        player1.attack_mg.enabled = True
        player2.attack_mg.enabled = True

    def ENDLESS(self):
        page_navigation.window_all_init()
        # 初始化遊戲狀態
        player1.reset()
        self.game_common(PageTable.ENDLESS, player1)

    def SONG(self):
        page_navigation.window_all_init()
        draw_mg.maps_clear(PageTable.SONG, True)
        song_mg.boot_base(PageTable.SONG)

        # 選項
        fonts_mg.renew_font(
            category    = PageTable.SONG,
            index       = song_mg.files_length + 1,
            pos         = layout_mg.get_item_pos(PageTable.SONG, LayoutName.SONG_MAIN),
        )

        # 音量網格線
        player1.draw.draw_grid(
            draw_mgr        = draw_mg,
            category        = PageTable.SONG,
            pos             = layout_mg.get_item_pos(PageTable.SONG, LayoutName.SONG_BLOCK),
            width_block     = SongVariable.WIDTH_BLOCK,
            height_block    = SongVariable.HEIGHT_BLOCK,
        )

    def HELP(self):
        page_navigation.window_all_init()

        # 加入 lace 邊框
        screen_mg.add_image(PageTable.HELP, LayoutName.HELP_LACE, PathConfig.img_lace)

    def RANK(self):
        page_navigation.window_all_init()

        rank_data = rank_mg.get_rank()
        for i, (extra_x, extra_y) in RankConfig.extra_pos.items():
            # 名次 分 秒 分數
            fonts_mg.renew_font(
                category    = PageTable.RANK,
                index       = BaseVariable.NUMBER_MAX + i,
                pos         = layout_mg.get_item_pos(
                    category = PageTable.RANK,
                    name = LayoutName.RANK_RANKING,
                    extra_x = extra_x,
                    extra_y = extra_y,
                ),
            )
            fonts_mg.renew_font(
                category    = PageTable.RANK,
                index       = BaseVariable.NUMBER_MAX + RankVariable.RANK_TOTAL + 0,
                pos         = layout_mg.get_item_pos(
                    category = PageTable.RANK,
                    name = LayoutName.RANK_MIN,
                    extra_x = extra_x,
                    extra_y = extra_y,
                ),
            )
            fonts_mg.renew_font(
                category    = PageTable.RANK,
                index       = BaseVariable.NUMBER_MAX + RankVariable.RANK_TOTAL + 1,
                pos         = layout_mg.get_item_pos(
                    category = PageTable.RANK,
                    name = LayoutName.RANK_SEC,
                    extra_x = extra_x,
                    extra_y = extra_y,
                    ),
            )
            fonts_mg.renew_font(
                category    = PageTable.RANK,
                index       = BaseVariable.NUMBER_MAX + RankVariable.RANK_TOTAL + 2,
                pos         = layout_mg.get_item_pos(
                    category = PageTable.RANK,
                    name = LayoutName.RANK_FRACTION,
                    extra_x = extra_x,
                    extra_y = extra_y,
                ),
            )

        for i, (extra_x, extra_y) in RankConfig.extra_pos_player.items():
            if rank_data[i][2] == 0: break

            # 玩家實際 分 秒 分數
            fonts_mg.renew_font(
                category    = PageTable.RANK,
                index       = rank_data[i][0],
                pos         = layout_mg.get_item_pos(
                    category = PageTable.RANK,
                    name = LayoutName.RANK_MIN,
                    extra_x = extra_x,
                    extra_y = extra_y,
                    ),
            )
            fonts_mg.renew_font(
                category    = PageTable.RANK,
                index       = rank_data[i][1],
                pos         = layout_mg.get_item_pos(
                    category = PageTable.RANK,
                    name = LayoutName.RANK_SEC,
                    extra_x = extra_x,
                    extra_y = extra_y,
                ),
            )
            fonts_mg.renew_font(
                category    = PageTable.RANK,
                index       = rank_data[i][2],
                pos         = layout_mg.get_item_pos(
                    category = PageTable.RANK,
                    name = LayoutName.RANK_FRACTION,
                    extra_x = extra_x + RankConfig.player_score_pos,
                    extra_y = extra_y,
                ),
            )

    def game_common(self, category, player: TetrisCore = player1):
        if player == player1:
            draw_mg.maps_clear(category, True)
            game_clock.reset()
            game_clock.start()

        # 主體網格線
        player.draw.draw_grid(
            draw_mgr        = draw_mg,
            category        = category,
            pos             = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.GAME_MAIN)),
            width_block     = player.field.width_block,
            height_block    = player.field.height_block,
        )
        # 暫存格網格線
        player.draw.draw_grid(
            draw_mgr        = draw_mg,
            category        = category,
            pos             = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.GAME_SLOT)),
            width_block     = GameVariable.CELL_BLOCK,
            height_block    = GameVariable.CELL_BLOCK,
        )
        # score
        fonts_mg.renew_font(
            category    = category,
            index       = GameVariable.MAX_SCORE + GameVariable.MAX_COMBO + GameVariable.MAX_KO_COUNT + 1,
            pos         = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.GAME_SCORE)),
        )

page_boot = PageBoot()
