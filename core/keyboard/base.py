import pygame

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

# MENU / SINGLE_MENU / SONG / HELP
class KeyboardList(KeyboardBase):
    def __init__(self, manager, min_x, max_x, min_y, max_y) -> None:
        super().__init__(manager)
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def move_up(self):
        self.mg.local_renew(
            renew_y = -1,
            min_x = self.min_x,
            max_x = self.max_x,
            min_y = self.min_y,
            max_y = self.max_y
        )

    def move_down(self):
        self.mg.local_renew(
            renew_y = 1,
            min_x = self.min_x,
            max_x = self.max_x,
            min_y = self.min_y,
            max_y = self.max_y
        )

    def move_left(self):
        self.mg.local_renew(
            renew_x = -1,
            min_x = self.min_x,
            max_x = self.max_x,
            min_y = self.min_y,
            max_y = self.max_y
        )

    def move_right(self):
        self.mg.local_renew(
            renew_x = 1,
            min_x = self.min_x,
            max_x = self.max_x,
            min_y = self.min_y,
            max_y = self.max_y
        )



class KeyboardManager:
    def __init__(self) -> None:
        self.hook_x = 0
        self.hook_y = 0
        self.enter_enable       = False
        self.back_enable        = False
        self.current_keyboard   = None

    def set(self, current_keyboard, player1, player2):
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
            max_x = 10,
            min_y = 0,
            max_y = 1
        )
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
            PageTable.SONG: {
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
        self.hook_x += renew_x
        self.hook_y += renew_y
        if self.hook_x < min_x: self.hook_x = max_x
        if self.hook_x > max_x: self.hook_x = min_x
        if self.hook_y < min_y: self.hook_y = max_y
        if self.hook_y > max_y: self.hook_y = min_y

    def local_clear(self):
        self.hook_x = 0
        self.hook_y = 0

    def imitate_button_event(self, button_event):
        ''' 模擬按下按鈕使pygame.event.get()觸發 '''
        enter_event = pygame.event.Event(pygame.KEYDOWN, key = button_event)
        pygame.event.post(enter_event)

keyboard_mg = KeyboardManager()
