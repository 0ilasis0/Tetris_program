import pygame
from core.base import central_mg
from core.debug import dbg
from core.keyboard.base import keyboard_mg


def main_keyboard(event):
    # 按鍵被按下時觸發一次
    if event.type == pygame.KEYDOWN:
        current_page_temp = keyboard_mg.keymaps_base.get(keyboard_mg.current_keyboard, {})
        if not current_page_temp:
            dbg.log("current_page is None, keymaps not set correctly")
            return

        handler = current_page_temp.get(event.key)

        if handler:
            handler()
        elif event.key != 1073742050:
            dbg.log(f"event.key = {event.key}, key name = {pygame.key.name(event.key)}, unicode = '{event.unicode}'")
