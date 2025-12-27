import pygame
from core.debug import dbg
from core.keyboard.variable import MaxLimits
from core.variable import PageTable


# 基礎鍵盤操作 (共用方法)
class KeyboardBase:
    def __init__(self, manager) -> None:
        self.mg = manager

    def move_backspace(self):
        self.mg.back_enable = True

    def move_enter(self):
        self.mg.enter_enable = True



# SINGLE / DOUBLE / ENDLESS
class KeyboardGame(KeyboardBase):
    def __init__(self, manager, player) -> None:
        super().__init__(manager)
        self.player = player

    def move_up(self):
        self.player.rotate()

    def move_down(self):
        self.player.move_down()

    def move_left(self):
        self.player.move_side(-1)

    def move_right(self):
        self.player.move_side(1)

    def move_space(self):
        self.player.go_space()

    def move_crtl_left(self):
        self.player.store_action()

# MENU / SINGLE_MENU / SYS_CONFIG / HELP
class KeyboardList(KeyboardBase):
    def __init__(
            self,
            manager,
            min_x,
            max_x,
            min_y,
            max_y,
            name_map: dict[int, str] | None = None
        ) -> None:

        super().__init__(manager)

        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.name_map = name_map

    def _resolve_limit(self, limit_obj, check_axis_val: int) -> int:
        """
        通用解析函式：
        limit_obj: 可能是 int (固定值) 或 dict (動態值)
        check_axis_val: 參考軸的數值 (例如要查 max_x，通常是依據目前的 hook_y)
        """
        # 如果是純數字，直接回傳(用於沒有傳入dict而是只有單層list的)
        if isinstance(limit_obj, int):
            return limit_obj

        # 如果是字典，開始查找
        if isinstance(limit_obj, dict):
            # 優先嘗試用「名稱」查找
            if self.name_map:
                key_name = self.name_map.get(check_axis_val) # int -> str
                if key_name in limit_obj:
                    return limit_obj[key_name]

            # 其次嘗試用「索引」查找
            if check_axis_val in limit_obj:
                dbg.error(f"名稱{limit_obj}輸入錯誤")
                return limit_obj[check_axis_val]

        dbg.error(f"名稱{limit_obj}與索引{check_axis_val}輸入錯誤")
        return 0

    def move_up(self):
        # Y 軸移動限制通常依賴 X 軸 (每行的直列長度可能不同)
        # 這裡依據 hook_x 來決定 Y 的範圍
        cur_min_y = self._resolve_limit(self.min_y, self.mg.hook_x)
        cur_max_y = self._resolve_limit(self.max_y, self.mg.hook_x)

        self.mg.local_renew(
            renew_y = -1,
            # 移動 Y 時，暫時不需要檢查 X 範圍 (或填 0)
            min_x = 0, max_x = 0,
            min_y = cur_min_y,
            max_y = cur_max_y
        )

    def move_down(self):
        cur_min_y = self._resolve_limit(self.min_y, self.mg.hook_x)
        cur_max_y = self._resolve_limit(self.max_y, self.mg.hook_x)

        self.mg.local_renew(
            renew_y = 1,
            min_x = 0, max_x = 0,
            min_y = cur_min_y,
            max_y = cur_max_y
        )

    def move_left(self):
        # X 軸移動限制依賴 Y 軸 (每一行的長度不同)
        cur_min_x = self._resolve_limit(self.min_x, self.mg.hook_y)
        cur_max_x = self._resolve_limit(self.max_x, self.mg.hook_y)

        # 為了保持 Y 軸不變，這裡的 Y 範圍也要查一次 (確保 local_renew 邊界正確)
        cur_min_y = self._resolve_limit(self.min_y, self.mg.hook_x)
        cur_max_y = self._resolve_limit(self.max_y, self.mg.hook_x)

        self.mg.local_renew(
            renew_x = -1,
            min_x = cur_min_x,
            max_x = cur_max_x,
            min_y = cur_min_y,
            max_y = cur_max_y
        )

    def move_right(self):
        cur_min_x = self._resolve_limit(self.min_x, self.mg.hook_y)
        cur_max_x = self._resolve_limit(self.max_x, self.mg.hook_y)
        cur_min_y = self._resolve_limit(self.min_y, self.mg.hook_x)
        cur_max_y = self._resolve_limit(self.max_y, self.mg.hook_x)

        self.mg.local_renew(
            renew_x = 1,
            min_x = cur_min_x,
            max_x = cur_max_x,
            min_y = cur_min_y,
            max_y = cur_max_y
        )

    # def move_up(self):
    #     self.mg.local_renew(
    #         renew_y = -1,
    #         min_x = self.min_x,
    #         max_x = self.max_x,
    #         min_y = self.min_y,
    #         max_y = self.max_y
    #     )

    # def move_down(self):
    #     self.mg.local_renew(
    #         renew_y = 1,
    #         min_x = self.min_x,
    #         max_x = self.max_x,
    #         min_y = self.min_y,
    #         max_y = self.max_y
    #     )

    # def move_left(self):
    #     self.mg.local_renew(
    #         renew_x = -1,
    #         min_x = self.min_x,
    #         max_x = self.max_x,
    #         min_y = self.min_y,
    #         max_y = self.max_y
    #     )

    # def move_right(self):
    #     self.mg.local_renew(
    #         renew_x = 1,
    #         min_x = self.min_x,
    #         max_x = self.max_x,
    #         min_y = self.min_y,
    #         max_y = self.max_y
    #     )



class KeyboardManager:
    def __init__(self) -> None:
        self.hook_x = 0
        self.hook_y = 0
        self.enter_enable       = False
        self.back_enable        = False
        self.current_keyboard   = None

    def setup(self, song_mg, current_keyboard, player1, player2):
        self.current_keyboard   = current_keyboard

        menu = KeyboardList(
            self,
            min_x = 0,
            max_x = 0,
            min_y = 0,
            max_y = 6,
        )
        single_menu = KeyboardList(
            self,
            min_x = 0,
            max_x = 4,
            min_y = 0,
            max_y = 1
        )
        player1_keyboard = KeyboardGame(self, player1)
        player2_keyboard = KeyboardGame(self, player2)
        song = KeyboardList(
            self,
            min_x = 0,
            max_x = MaxLimits.SYS_SONG, # 傳入字典
            min_y = 0,
            max_y = 2,
            name_map = song_mg.key_map # song_mg 的映射表
        )
        # song = KeyboardList(
        #     self,
        #     min_x = 0,
        #     max_x = 10,
        #     min_y = 0,
        #     max_y = 2
        # )
        help = KeyboardList(
            self,
            min_x = 0,
            max_x = 2,
            min_y = 0,
            max_y = 0
        )
        rank = KeyboardList(
            self,
            min_x = 0,
            max_x = 0,
            min_y = 0,
            max_y = 0
        )


        self.keymaps_base = {
            PageTable.MENU: {
                pygame.K_UP:        menu.move_up,
                pygame.K_DOWN:      menu.move_down,
                pygame.K_BACKSPACE: menu.move_backspace,
                pygame.K_RETURN:    menu.move_enter,
            },
            PageTable.SINGLE_MENU: {
                pygame.K_UP:        single_menu.move_up,
                pygame.K_DOWN:      single_menu.move_down,
                pygame.K_LEFT:      single_menu.move_left,
                pygame.K_RIGHT:     single_menu.move_right,
                pygame.K_BACKSPACE: single_menu.move_backspace,
                pygame.K_RETURN:    single_menu.move_enter,
            },
            PageTable.SINGLE: {
                pygame.K_UP:        player1_keyboard.move_up,
                pygame.K_DOWN:      player1_keyboard.move_down,
                pygame.K_LEFT:      player1_keyboard.move_left,
                pygame.K_RIGHT:     player1_keyboard.move_right,
                pygame.K_SPACE:     player1_keyboard.move_space,
                pygame.K_LCTRL:     player1_keyboard.move_crtl_left,
                pygame.K_BACKSPACE: player1_keyboard.move_backspace,
            },
            PageTable.DOUBLE: {
                # 玩家1
                pygame.K_w:         player1_keyboard.move_up,
                pygame.K_s:         player1_keyboard.move_down,
                pygame.K_a:         player1_keyboard.move_left,
                pygame.K_d:         player1_keyboard.move_right,
                pygame.K_LSHIFT:    player1_keyboard.move_space,
                pygame.K_LCTRL:     player1_keyboard.move_crtl_left,
                # 玩家2
                pygame.K_UP:        player2_keyboard.move_up,
                pygame.K_DOWN:      player2_keyboard.move_down,
                pygame.K_LEFT:      player2_keyboard.move_left,
                pygame.K_RIGHT:     player2_keyboard.move_right,
                pygame.K_RSHIFT:    player2_keyboard.move_space,
                pygame.K_RCTRL:     player2_keyboard.move_crtl_left,
                # 共用
                pygame.K_BACKSPACE: player2_keyboard.move_backspace,
            },
            PageTable.ENDLESS: {
                pygame.K_UP:        player1_keyboard.move_up,
                pygame.K_DOWN:      player1_keyboard.move_down,
                pygame.K_LEFT:      player1_keyboard.move_left,
                pygame.K_RIGHT:     player1_keyboard.move_right,
                pygame.K_SPACE:     player1_keyboard.move_space,
                pygame.K_LCTRL:     player1_keyboard.move_crtl_left,
                pygame.K_BACKSPACE: player1_keyboard.move_backspace,
            },
            PageTable.SYS_CONFIG: {
                pygame.K_UP:        song.move_up,
                pygame.K_DOWN:      song.move_down,
                pygame.K_LEFT:      song.move_left,
                pygame.K_RIGHT:     song.move_right,
                pygame.K_BACKSPACE: song.move_backspace,
            },
            PageTable.HELP: {
                pygame.K_UP:        help.move_up,
                pygame.K_DOWN:      help.move_down,
                pygame.K_LEFT:      help.move_left,
                pygame.K_RIGHT:     help.move_right,
                pygame.K_BACKSPACE: help.move_backspace,
            },
            PageTable.RANK: {
                pygame.K_BACKSPACE: rank.move_backspace,
            }
        }

    def local_renew(self, renew_x = 0, renew_y = 0, min_x = 0, max_x = 0, min_y = 0, max_y = 0):
        if renew_x != 0:
            self.hook_x += renew_x
            if self.hook_x < min_x: self.hook_x = max_x
            if self.hook_x > max_x: self.hook_x = min_x

        elif renew_y != 0:
            self.hook_y += renew_y
            if self.hook_y < min_y: self.hook_y = max_y
            if self.hook_y > max_y: self.hook_y = min_y

    def clear_local(self):
        self.hook_x = 0
        self.hook_y = 0

    def imitate_button_event(self, button_event):
        ''' 模擬按下按鈕使pygame.event.get()觸發 '''
        enter_event = pygame.event.Event(pygame.KEYDOWN, key = button_event)
        pygame.event.post(enter_event)

keyboard_mg = KeyboardManager()
