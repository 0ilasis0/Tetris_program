import pygame

from core.debug import dbg
from core.font.font_manager import fonts_mg
from core.location_layout.main import layout_mg
from core.screen.base import ScreenManager, screen_mg
from core.screen.drawing import draw_mg


def main_screen():
    # 初始化畫面
    screen_mg.window.fill((0, 0, 0))

    # 背景圖片更新
    show_draw(screen_mg)

    # 更新繪圖draw
    draw_mg.show_picture(screen_mg.window, draw_mg.current_draw_dynamic, False)
    draw_mg.show_picture(screen_mg.window, draw_mg.current_draw_static, True)

    # 文字更新
    fonts_mg.show_texts(screen_mg.window)

    pygame.display.flip()  # 更新整個畫面


def show_draw(screen_mg: ScreenManager):
    # 背景
    bg_surface = screen_mg._get_background_surface()
    if bg_surface:
        screen_mg.window.blit(bg_surface, (0, 0))

    # 畫每個圖片
    images = screen_mg.page_images.get(screen_mg.current_page, {})
    for name, surface in images.items():
        layout_item = layout_mg.get_item(screen_mg.current_page, name)
        if not layout_item:
            dbg.log(f'{layout_item} is not in {images}')
            continue

        x, y = layout_item.pos.x, layout_item.pos.y
        width, height = layout_item.size.width, layout_item.size.height

        # 如果大小不同 → 縮放
        if (width, height) != surface.get_size():
            surface_to_draw = pygame.transform.scale(surface, (width, height))
        else:
            surface_to_draw = surface

        screen_mg.window.blit(surface_to_draw, (x, y))
