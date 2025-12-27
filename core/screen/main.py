import pygame
from core.font.manager import font_mg
from core.screen.drawing import draw_mg
from core.screen.image import img_mg


def main_screen():
    # 初始化畫面
    img_mg.window.fill((0, 0, 0))

    # 背景/圖片更新
    img_mg.show_image(True)
    img_mg.show_image(False)

    # 更新繪圖draw
    draw_mg.show_draw(img_mg.window, draw_mg.current_draw_dynamic, False)
    draw_mg.show_draw(img_mg.window, draw_mg.current_draw_static, True)

    # 文字更新
    font_mg.show_texts(img_mg.window)

    pygame.display.flip()  # 更新整個畫面
