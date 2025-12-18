from pathlib import Path

import pygame

from core.location_layout.variable import LayoutName, Size
from core.screen.variable import ScreenConfig
from core.variable import PageTable, PathBase, PathConfig


class ScreenManager:
    def __init__(self):
        self.window = None

        # 背景快取 {Path: pygame.Surface}
        self.bg_cache: dict[Path, pygame.Surface] = {}

        # 每個 PageTable 對應背景路徑
        self.page_backgrounds: dict[PageTable, Path] = {}
        self.current_page: PageTable = PageTable.MENU

        # 每個 PageTable 的圖片字典： { name: {surface, x, y, z_index(決定圖片先後)} }
        self.page_images: dict[PageTable, dict[str, dict]] = {page: {} for page in PageTable}

    # ========= 視窗設定 =========
    def set(self):
        self.window = pygame.display.set_mode((ScreenConfig.width, ScreenConfig.height))
        pygame.display.set_caption(ScreenConfig.title_name)

        # 載入 icon
        icon_surface = pygame.image.load(str(PathBase.icon))
        pygame.display.set_icon(icon_surface)

        # 載入背景
        self.set_background(PageTable.MENU, PathConfig.bg1)
        self.set_background(PageTable.SINGLE, PathConfig.bg1)
        self.set_background(PageTable.SINGLE_MENU, PathConfig.bg1)
        self.set_background(PageTable.DOUBLE, PathConfig.bg1)
        self.set_background(PageTable.ENDLESS, PathConfig.bg1)
        self.set_background(PageTable.SONG, PathConfig.bg1)
        self.set_background(PageTable.HELP, PathConfig.bg1)
        self.set_background(PageTable.RANK, PathConfig.bg1)

        # 載入圖片
        self.add_image(PageTable.SINGLE, LayoutName.game_suffix_key(LayoutName.GAME_CLOCK, 0), PathConfig.img_clock)
        self.add_image(PageTable.DOUBLE, LayoutName.game_suffix_key(LayoutName.GAME_CLOCK, 0), PathConfig.img_clock)
        self.add_image(PageTable.ENDLESS, LayoutName.game_suffix_key(LayoutName.GAME_CLOCK, 0), PathConfig.img_clock)
        self.add_image(PageTable.RANK, LayoutName.RANK_UNDERLINE, PathConfig.img_ranking)
        self.add_image(PageTable.RANK, LayoutName.RANK_FRAME, PathConfig.img_frame)

    # ========= 背景 =========
    def set_background(self, page: PageTable, file_path: Path):
        """設定 page 背景路徑"""
        self.page_backgrounds[page] = file_path
        if file_path not in self.bg_cache:
            self.bg_cache[file_path] = pygame.image.load(str(file_path))

    def _get_background_surface(self):
        """取得當前頁面的背景 surface"""
        file_path = self.page_backgrounds.get(self.current_page)
        if not file_path:
            return None
        return self.bg_cache[file_path]

    # ========= 圖片 =========
    def add_image(self, page: PageTable, name: str, file_path: Path):
        if file_path not in self.bg_cache:
            self.bg_cache[file_path] = pygame.image.load(str(file_path))
        self.page_images[page][name] = self.bg_cache[file_path]

    def remove_image(self, page: PageTable, name: str):
        """刪除圖片"""
        if name in self.page_images[page]:
            del self.page_images[page][name]

    def clear_images(self, page: PageTable):
        """清空頁面圖片"""
        self.page_images[page].clear()

    # ========= 頁面切換 =========
    def switch_page(self, page: PageTable):
        self.current_page = page

    # ========= 其他工具 =========
    def get_image_size(self, file_path: Path):
        if file_path not in self.bg_cache:
            self.bg_cache[file_path] = pygame.image.load(str(file_path))
        surface = self.bg_cache[file_path]
        width, height= surface.get_size()
        return Size(width, height)


screen_mg = ScreenManager()
