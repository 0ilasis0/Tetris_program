from core.base import central_mg
from core.debug import dbg
from core.font.manager import font_mg
from core.hmi.config.main import sys_config_mg
from core.hmi.config.variable import ConfigSongVar
from core.hmi.rank import rank_mg
from core.keyboard.base import keyboard_mg
from core.location_layout.main import layout_mg
from core.location_layout.variable import LayoutName, location_config
from core.page.base import page_mg
from core.page.navigation import BasePageNavigation
from core.page.tree_path import tree_path_table
from core.page.variable import HelpConfig, RankConfig
from core.screen.drawing import draw_mg
from core.screen.image import img_mg
from core.tetris_game.main import (TetrisCore, clock_game, individual_tetris,
                                   main_tetris_game)
from core.tetris_game.manager import player1, player2
from core.tetris_game.variable import BaseVar, GameVar, RankVar
from core.variable import (JsonPath, PageTable, PathConfig, Position, Size,
                           colors)


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
        dbg.error(f"no load {page_mg.current_page}")



class PageNavigation(BasePageNavigation):
    def __init__(self) -> None:
        super().__init__(tree_path_table, page_mg, keyboard_mg, draw_mg, font_mg)

    def MENU(self):
        # 初始化螢幕
        self.window_all_init(PageTable.MENU, False, False, True, False)
        draw_mg.clear_map(PageTable.MENU)
        self.base_common(PageTable.MENU)

        # 畫玩家選擇方塊
        menu_rect = layout_mg.get_item(PageTable.MENU, LayoutName.MENU_RECT)

        draw_mg.add_form(
            category  = PageTable.MENU,
            name        = LayoutName.MENU_RECT,
            shape       = 'rect',
            pos         = Position(menu_rect.pos.x, menu_rect.pos.y + keyboard_mg.hook_y * location_config.y_gap),
            size        = layout_mg.get_item_size(PageTable.MENU, LayoutName.MENU_RECT),
            color       = colors[7],
            hollow      = location_config.scale(5),
            fixed       = False,
        )
        draw_mg.current_draw_dynamic = [PageTable.MENU]

    def SINGLE_MENU(self):
        self.window_all_init(PageTable.SINGLE_MENU, False, False, True, False)
        draw_mg.clear_map(PageTable.SINGLE_MENU)
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
        # 初始化螢幕
        # self.window_all_init(PageTable.SINGLE, True, True, True, False)
        # draw_mg.maps_clear(PageTable.SINGLE)
        # self.base_common(PageTable.SINGLE)

    def DOUBLE(self):
        self.game_common(PageTable.DOUBLE, player1)
        self.game_common(PageTable.DOUBLE, player2)

    def ENDLESS(self):
        self.game_common(PageTable.ENDLESS, player1)

    def SYS_CONFIG(self):
        # --------- 核心 ---------
        sys_config_mg.main_process()

        self.window_all_init(PageTable.SYS_CONFIG, True, False, True, False)
        draw_mg.clear_map(PageTable.SYS_CONFIG)
        self.base_common(PageTable.SYS_CONFIG)

        # 畫音量大小方塊
        song_block = layout_mg.get_item(PageTable.SYS_CONFIG, LayoutName.SYS_SONG_BLOCK)
        draw_mg.add_form(
            category  = PageTable.SYS_CONFIG,
            name        = LayoutName.SYS_SONG_BLOCK,
            shape       = 'rect',
            pos         = layout_mg.get_item_pos(PageTable.SYS_CONFIG, LayoutName.SYS_SONG_BLOCK),
            size        = Size(location_config.zoom * sys_config_mg.state.get(JsonPath.SYS_VOLUME.value), song_block.size.height),
            color       = colors[5],
            hollow      = 0,
            fixed       = False,
        )
        # 畫玩家選擇方塊
        song_rect = layout_mg.get_item(PageTable.SYS_CONFIG, LayoutName.SYS_SONG_RECT)
        draw_mg.add_form(
            category  = PageTable.SYS_CONFIG,
            name        = LayoutName.SYS_SONG_RECT,
            shape       = 'rect',
            pos         = Position(song_rect.pos.x, song_rect.pos.y + keyboard_mg.hook_y * location_config.y_gap),
            size        = layout_mg.get_item_size(PageTable.SYS_CONFIG, LayoutName.SYS_SONG_RECT),
            color       = colors[7],
            hollow      = location_config.scale(5),
            fixed       = False,
        )

        # 歌曲名稱
        font_mg.renew_font(
            category    = PageTable.SYS_CONFIG,
            index       = sys_config_mg.state.get(JsonPath.SYS_SELECT_SONG.value) % (sys_config_mg.files_amount + ConfigSongVar.RANDOM_SPACE),
            pos         = layout_mg.get_item_pos(PageTable.SYS_CONFIG, LayoutName.SYS_SONG_NAME),
            fixed       = False
        )

        # 調整視窗大小數值顯示
        font_mg.renew_font(
            category    = PageTable.SYS_CONFIG,
            index       = sys_config_mg.state.get(JsonPath.SYS_WINDOW_SCALE.value) + sys_config_mg.files_amount + ConfigSongVar.RANDOM_SPACE,
            pos         = layout_mg.get_item_pos(PageTable.SYS_CONFIG, LayoutName.SYS_WINDOW_SCALE),
            fixed       = False,
            direction   = "horizontal"
        )

        draw_mg.current_draw_static = [PageTable.SYS_CONFIG]
        draw_mg.current_draw_dynamic = [PageTable.SYS_CONFIG]

    def HELP(self):
        self.window_all_init(PageTable.HELP, True, True, False, False)
        self.base_common(PageTable.HELP)

        # 玩家選擇 img_panel
        name = LayoutName.HELP_PANEL.serial_list[keyboard_mg.hook_x]
        img_mg.add_image(
            PageTable.HELP,
            name,
            PathConfig.img_panel[keyboard_mg.hook_x],
            layout_mg.get_item_size(PageTable.HELP, name),
            False
        )

        # 標題文字
        for i, (layout_name, idx) in enumerate(HelpConfig.title_items):
            font_mg.renew_font(
                category  = PageTable.HELP,
                index     = idx,
                pos       = layout_mg.get_item_pos(PageTable.HELP, layout_name),
                fixed     = False,
                alpha_pec = HelpConfig.title_alpha[keyboard_mg.hook_x][i],
                direction = 'horizontal',
            )

        # 遊戲說明文字
        font_mg.renew_font(
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
            self.window_all_init(category, True, False, True, False)
            draw_mg.clear_map(category)

        self.base_common(category)

        # 共同核心
        main_tetris_game(player = player)
        # timer
        min, sec = clock_game.get_min_sec()
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
            other_x     = player.current_tetromino.x * location_config.zoom,
            other_y     = player.current_tetromino.y * location_config.zoom,
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
        font_mg.renew_font(
            category    = category,
            index       = player.score,
            pos         = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.BASE_NUMBER_BIG)),
            fixed       = False,
        )
        # combo / combo number
        if player.combo > 0:
            font_mg.renew_font(
                category    = category,
                index       = GameVar.MAX_SCORE + GameVar.MAX_COMBO + GameVar.MAX_KO_COUNT,
                pos         = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.GAME_COMBO)),
                fixed       = False,
            )
            font_mg.renew_font(
                category    = category,
                index       = player.combo + GameVar.MAX_SCORE,
                pos         = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.GAME_COMBO_NUMBER)),
                fixed       = False,
            )
        # ko顯示
        if player.attack_mg.ko_counter > 0:
            font_mg.renew_font(
                category    = category,
                index       = GameVar.MAX_SCORE + GameVar.MAX_COMBO + (player.attack_mg.ko_counter - 1),
                pos         = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.GAME_KO)),
                fixed       = False,
            )
        # timer_clock
        if player == player1:
            font_mg.renew_font(
                category    = category,
                index       = min,
                pos         = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.GAME_CLOCK_MIN)),
                fixed       = False,
            )
            font_mg.renew_font(
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
        page_navigation.window_all_init(PageTable.MENU)
        draw_mg.clear_map(PageTable.MENU, True)

        # 目錄文字
        font_mg.renew_font(
            category = PageTable.MENU,
            index   = 0,
            pos     = layout_mg.get_item_pos(PageTable.MENU, LayoutName.MENU_MAIN),
        )

    def SINGLE_MENU(self):
        page_navigation.window_all_init(PageTable.SINGLE_MENU)

        # 畫基本關卡方塊
        single_menu_rect = layout_mg.get_item(PageTable.SINGLE_MENU, LayoutName.SINGLE_MENU_RECT)
        for height_block in range(GameVar.SINGLE_MENU_HEIGHT_BLOCK):
            for width_block in range(GameVar.SINGLE_MENU_WIDTH_BLOCK):
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
                    hollow      = location_config.scale(5),
                )
        # 畫關卡數字
        single_menu_number = layout_mg.get_item(PageTable.SINGLE_MENU, LayoutName.BASE_NUMBER_BIG)
        for height_level in range(GameVar.SINGLE_MENU_HEIGHT_BLOCK):
            for width_level in range(GameVar.SINGLE_MENU_WIDTH_BLOCK):
                font_mg.renew_font(
                    category = PageTable.SINGLE_MENU,
                    index   = width_level + height_level * GameVar.SINGLE_MENU_WIDTH_BLOCK + 1,
                    pos     = Position(
                        single_menu_number.pos.x + (width_level * single_menu_rect.size.width * 2),
                        single_menu_number.pos.y + (height_level * single_menu_rect.size.height * 2)
                    ),
                )

    def SINGLE(self):
        # page_navigation.window_all_init(PageTable.SINGLE)
        # draw_mg.maps_clear(PageTable.SINGLE, True)
        page_navigation.window_all_init(PageTable.SINGLE, True)
        # 初始化遊戲狀態
        player1.reset(attack_sw = True, level_sw = False)
        player1.level_mg.update_level(player = player1, level = player1.level_mg.current_level)

        self.game_common(PageTable.SINGLE, player1)

    def DOUBLE(self):
        page_navigation.window_all_init(PageTable.DOUBLE)
        # 初始化遊戲狀態
        player1.reset()
        player2.reset()
        self.game_common(PageTable.DOUBLE, player1)
        self.game_common(PageTable.DOUBLE, player2)
        player1.attack_mg.enabled = True
        player2.attack_mg.enabled = True

    def ENDLESS(self):
        page_navigation.window_all_init(PageTable.ENDLESS)
        # 初始化遊戲狀態
        player1.reset()
        self.game_common(PageTable.ENDLESS, player1)

    def SYS_CONFIG(self):
        page_navigation.window_all_init(PageTable.SYS_CONFIG)
        draw_mg.clear_map(PageTable.SYS_CONFIG, True)
        sys_config_mg.boot_base(PageTable.SYS_CONFIG)

        # 選項
        font_mg.renew_font(
            category    = PageTable.SYS_CONFIG,
            index       = sys_config_mg.files_amount + ConfigSongVar.RANDOM_SPACE + sys_config_mg.window_scale_amount,
            pos         = layout_mg.get_item_pos(PageTable.SYS_CONFIG, LayoutName.SYS_SONG_MAIN),
        )

        # 音量網格線
        player1.draw.draw_grid(
            draw_mgr        = draw_mg,
            category        = PageTable.SYS_CONFIG,
            pos             = layout_mg.get_item_pos(PageTable.SYS_CONFIG, LayoutName.SYS_SONG_BLOCK),
            width_block     = ConfigSongVar.WIDTH_BLOCK,
            height_block    = ConfigSongVar.HEIGHT_BLOCK,
        )

    def HELP(self):
        page_navigation.window_all_init(PageTable.HELP)

    def RANK(self):
        page_navigation.window_all_init(PageTable.RANK)

        rank_data = rank_mg.get_rank()
        for i, (extra_x, extra_y) in RankConfig.extra_pos.items():
            # 名次 分 秒 分數
            font_mg.renew_font(
                category    = PageTable.RANK,
                index       = BaseVar.NUMBER_MAX + i,
                pos         = layout_mg.get_item_pos(
                    category = PageTable.RANK,
                    name = LayoutName.RANK_RANKING,
                    extra_x = extra_x,
                    extra_y = extra_y,
                ),
            )
            font_mg.renew_font(
                category    = PageTable.RANK,
                index       = BaseVar.NUMBER_MAX + RankVar.RANK_TOTAL + 0,
                pos         = layout_mg.get_item_pos(
                    category = PageTable.RANK,
                    name = LayoutName.RANK_MIN,
                    extra_x = extra_x,
                    extra_y = extra_y,
                ),
            )
            font_mg.renew_font(
                category    = PageTable.RANK,
                index       = BaseVar.NUMBER_MAX + RankVar.RANK_TOTAL + 1,
                pos         = layout_mg.get_item_pos(
                    category = PageTable.RANK,
                    name = LayoutName.RANK_SEC,
                    extra_x = extra_x,
                    extra_y = extra_y,
                    ),
            )
            font_mg.renew_font(
                category    = PageTable.RANK,
                index       = BaseVar.NUMBER_MAX + RankVar.RANK_TOTAL + 2,
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
            font_mg.renew_font(
                category    = PageTable.RANK,
                index       = rank_data[i][0],
                pos         = layout_mg.get_item_pos(
                    category = PageTable.RANK,
                    name = LayoutName.RANK_MIN,
                    extra_x = extra_x,
                    extra_y = extra_y,
                    ),
            )
            font_mg.renew_font(
                category    = PageTable.RANK,
                index       = rank_data[i][1],
                pos         = layout_mg.get_item_pos(
                    category = PageTable.RANK,
                    name = LayoutName.RANK_SEC,
                    extra_x = extra_x,
                    extra_y = extra_y,
                ),
            )
            font_mg.renew_font(
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
            draw_mg.clear_map(category, True)
            clock_game.reset()
            clock_game.start()

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
            width_block     = GameVar.CELL_BLOCK,
            height_block    = GameVar.CELL_BLOCK,
        )
        # score
        font_mg.renew_font(
            category    = category,
            index       = GameVar.MAX_SCORE + GameVar.MAX_COMBO + GameVar.MAX_KO_COUNT + 1,
            pos         = layout_mg.get_item_pos(category, player.suffix_key(LayoutName.GAME_SCORE)),
        )

page_boot = PageBoot()
