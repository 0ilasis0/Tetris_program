import pprint

import pygame
from core.base import Stack
from core.json.build import build_json
from core.json.manager import json_mg
from core.font.rendering import rendering
from core.hmi.song import song_mg
from core.keyboard.base import keyboard_mg
from core.page.base import page_mg
from core.page.main import page_boot, page_navigation
from core.page.tree_path import genealogy_table, tree_path_table
from core.screen.main import screen_mg
from core.tetris_game.manager import player1, player2
from core.variable import PageTable

page_maps = {page: getattr(page_navigation, page.name) for page in PageTable}
# 等同下方
# page_maps = {
#     PageTable.MENU:     page_navigation.MENU,
#     PageTable.SINGLE:   page_navigation.SINGLE,
#     PageTable.DOUBLE:   page_navigation.DOUBLE,
#     ......
#     PageTable.TETRIS_SINGLE:   page_navigation.TETRIS_SINGLE,
# }

# build_json()



#
# 初始化set
#
''' base '''
pygame.init()

''' screen '''
screen_mg.setup()

''' keyboard '''
keyboard_mg.setup(
    current_keyboard = PageTable.MENU,
    player1 = player1,
    player2 = player2,
    )

''' page '''
#註冊 Callback
for page in PageTable:
    # 檢查 PageInit 是否有對應方法
    if hasattr(page_boot, page.name):
        fcn = getattr(page_boot, page.name)
        page_mg.register_init_fcn(page, fcn)

page_mg.setup(
    stack = Stack(PageTable.MENU, genealogy_table),
    keymaps = page_maps,
    page_map = tree_path_table[PageTable.MENU].family_table,
    current_page = PageTable.MENU
)

''' song '''
pygame.mixer.init()
song_mg.setup()



#
# other
#
''' font '''
rendering()
# 如果找 read_list_json 直接去 json_manager __init__進行設定

''' page '''
# 對第一次的MENU做BOOT
page_mg.boot_page(page_mg.current_page)

# 確認 word_list_data / word_dict_data 清單
print('------------------')
print('---------word_list_data---------')
pprint.pprint(json_mg.word_list_data)
print('---------word_dict_data---------')
pprint.pprint(json_mg.word_dict_data)
print('------------------')
