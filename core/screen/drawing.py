import pygame
from core.variable import Position, Size


class DrawManager():
    def __init__(self):
        self.draw_static_maps = {}          # 靜態畫布儲存map
        self.draw_dynamic_maps = {}         # 動態畫布儲存map
        self.current_draw_static = []       # 靜態畫布
        self.current_draw_dynamic = []      # 動態畫布

    def add_form(
            self,
            category,
            name,
            shape,
            pos:Position,
            size: Size,
            color,
            hollow = 1,
            fixed = True,
            ):
        '''
        pos 為x0 y0 座標
        size 為 width height 長寬
        '''
        target_map = self.draw_static_maps if fixed else self.draw_dynamic_maps

        if category not in target_map:
            target_map[category] = []

        target_map[category].append({
            "name": name,
            "shape": shape,
            "place_x": round(pos.x),
            "place_y": round(pos.y),
            "size_x": round(size.width),
            "size_y": round(size.height),
            "color": color,
            "hollow": hollow
        })

    def show_picture(self, screen, page_tables, fixed):
        target_map = self.draw_static_maps if fixed else self.draw_dynamic_maps

        if not isinstance(page_tables, list):
            page_tables = [page_tables]

        for category in page_tables:
            if category not in target_map:
                continue
            for form in target_map[category]:
                if form["shape"] == "rect":
                    rect = pygame.Rect(form["place_x"], form["place_y"], form["size_x"], form["size_y"])
                    pygame.draw.rect(screen, form["color"], rect, form["hollow"])
                elif form["shape"] == "circle":
                    pygame.draw.circle(screen, form["color"], (form["place_x"], form["place_y"]), form["size_x"], form["hollow"])

    def maps_clear(self, category, fixed = False):
        """清除某頁的某類型畫布"""
        target_map = self.draw_static_maps if fixed else self.draw_dynamic_maps
        target_map[category] = []

    def current_clear(self):
        '''clear 畫布'''
        self.current_draw_dynamic = []
        self.current_draw_static = []

draw_mg = DrawManager()
