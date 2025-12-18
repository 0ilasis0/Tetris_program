from core.debug import dbg
from core.hmi.grid import GridManager
from core.page.variable import GridParameter, GridThing, NavigationHandle
from core.screen.base import screen_mg
from core.tetris_game.manager import TetrisCore, player1
from core.variable import PageTable


class ToolPageNavigation:
    def __init__(self, keyboard_mg, draw_mg, fonts_mg) -> None:
        self.keyboard_mg = keyboard_mg
        self.draw_mg = draw_mg
        self.fonts_mg = fonts_mg

    def hook_clear(self, current_table, next_table):
        if next_table != current_table:
            self.keyboard_mg.local_clear()

    def window_all_init(
            self,
            draw_sw: bool = True,
            fonts_static_sw: bool = True,
            fonts_dynamic_sw: bool = True,
            ):
        if draw_sw:
            self.draw_mg.current_clear()
        self.fonts_mg.current_clear(fonts_static_sw, fonts_dynamic_sw)



# 處理PageNavigation共通 按鈕 邏輯
class BasePageNavigation(ToolPageNavigation):
    def __init__(self, tree_path_table, page_mg, keyboard_mg, draw_mg, fonts_mg) -> None:
        self.tree_path_table = tree_path_table
        self.page_mg = page_mg
        self.keyboard_mg = keyboard_mg
        self.draw_mg = draw_mg
        self.fonts_mg = fonts_mg

        self.set()

        super().__init__(keyboard_mg, draw_mg, fonts_mg)

    def set(self):

        navigation_base = NavigationList(self)
        navigation_grid = NavigationSingleMenu(self, player1)

        self.keymaps_navigation = {
            PageTable.MENU:{
                NavigationHandle.ENTER: navigation_base.enter_handle
            },
            PageTable.SINGLE_MENU:{
                NavigationHandle.ENTER: navigation_grid.enter_handle
            },
        }

    def handle_enter(self, current_table):
        ''' 處理按下 Enter 的共用邏輯 '''
        if not self.keyboard_mg.enter_enable: return
        self.keyboard_mg.enter_enable = False

        # 分派到對應 handler
        handler = self.keymaps_navigation.get(current_table, {}).get(NavigationHandle.ENTER)
        if handler:
            handler(current_table)
        else:
            dbg.log(f"[handle_enter] {current_table} 沒有對應的 handler")

    def handle_back(self, current_table):
        ''' 處理按下 Back 的共用邏輯 '''
        if self.keyboard_mg.back_enable:
            self.keyboard_mg.back_enable = False

            past_table_key = self.page_mg.history_stack.back(current_table)

            self.switch_page(current_table, past_table_key)

    def switch_page(self, current_table, change_table):
        ''' 用於切換程式中當前的頁面（或分頁） '''
        # 刷新下一個背景
        screen_mg.switch_page(change_table)
        # 決定要進入的下一個 current_page 分頁
        self.page_mg.current_page = change_table
        # 決定要進入的下一個 current_keyboard
        self.keyboard_mg.current_keyboard = change_table
        # 決定下一個誰要載入初始畫面
        self.page_mg.current_boot = change_table
        # 如果換頁面則初始化hook
        self.hook_clear(current_table, self.page_mg.current_page)

    def base_common(self, catalog):
        # 決定是否進入或退出下一分頁
        self.handle_back(catalog)
        self.handle_enter(catalog)



class NavigationList:
    def __init__(self, base_nav: BasePageNavigation) -> None:
        self.base_nav = base_nav

    def enter_handle(self, current_table):
        next_table = self.base_nav.tree_path_table[current_table].family_table

        if self.base_nav.keyboard_mg.hook_y not in next_table:
            dbg.log('no next page')
            return

        self.base_nav.switch_page(current_table, next_table[self.base_nav.keyboard_mg.hook_y])
        # 存入當前分頁至Stack
        self.base_nav.page_mg.history_stack.visit(current_table, next_table[self.base_nav.keyboard_mg.hook_y])


class NavigationSingleMenu:
    def __init__(self, base_nav: BasePageNavigation, player:TetrisCore = player1) -> None:
        self.base_nav = base_nav
        self.player = player

        self.grid_mg = GridManager(GridParameter.SINGLE_MENU_LEVEL_ROW, GridParameter.SINGLE_MENU_LEVEL_COLS)
        self.set()

    def set(self):
        for y in range(GridParameter.SINGLE_MENU_LEVEL_ROW):
            for x in range(GridParameter.SINGLE_MENU_LEVEL_COLS):
                self.grid_mg.set_cell(x, y, **{GridThing.LOCK_SWITCH_: GridThing.UNLOCK})

    def enter_handle(self, current_table):
        # 取得當前 hook 的 cell
        cell = self.grid_mg.get_cell(self.base_nav.keyboard_mg.hook_x, self.base_nav.keyboard_mg.hook_y)
        if cell.is_empty():
            dbg.log("NavigationSingleMenu.enter_handle: cell is empty")
            return

        self.player.level_mg.current_level = (self.base_nav.keyboard_mg.hook_x + self.base_nav.keyboard_mg.hook_y * 5)

        # 讀取 cell 的資料
        lock_state = cell.data.get(GridThing.LOCK_SWITCH_, None)

        if lock_state == GridThing.UNLOCK:
            next_table = PageTable.SINGLE  # 假設要進入 SINGLE 模式，因為所有關卡進入相同頁面
            self.base_nav.switch_page(current_table, next_table)
            self.base_nav.page_mg.history_stack.visit(current_table, next_table)
