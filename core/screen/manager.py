from pathlib import Path

import pygame
from core.location_layout.main import layout_mg
from core.location_layout.manager import LayoutNameManage
from core.location_layout.variable import LayoutName
from core.screen.variable import ScreenConfig
from core.variable import PageTable, PathBase, PathConfig, Size


class ScreenManager:
    def __init__(self):
        self.window = None

        # 圖片快取 {Path: pygame.Surface}
        self.img_cache: dict[(Path, Size | None), pygame.Surface] = {}

        # 每個 PageTable 對應背景路徑
        self.page_backgrounds: dict[PageTable, Path] = {}
        self.current_page: PageTable = PageTable.MENU

        # 每個 PageTable 的圖片字典： { name: {surface, x, y, z_index(決定圖片先後)} }
        self.page_images_static: dict[PageTable, dict[str, dict]] = {page: {} for page in PageTable}
        self.page_images_dynaic: dict[PageTable, dict[str, dict]] = {page: {} for page in PageTable}

    # ========= 視窗設定 =========
    def reload_setup(self):
        self.window = pygame.display.set_mode((ScreenConfig.width, ScreenConfig.height))
        pygame.display.set_caption(ScreenConfig.title_name)

        # 載入 icon
        icon_surface = pygame.image.load(str(PathBase.icon))
        pygame.display.set_icon(icon_surface)

        # 載入背景
        self.add_image(PageTable.MENU,          LayoutName.MENU_BG,         PathConfig.bg1, layout_mg.get_item_size(PageTable.MENU, LayoutName.MENU_BG))
        self.add_image(PageTable.SINGLE,        LayoutName.SINGLE_BG,       PathConfig.bg1, layout_mg.get_item_size(PageTable.SINGLE, LayoutName.SINGLE_BG))
        self.add_image(PageTable.SINGLE_MENU,   LayoutName.SINGLE_MENU_BG,  PathConfig.bg1, layout_mg.get_item_size(PageTable.SINGLE_MENU, LayoutName.SINGLE_MENU_BG))
        self.add_image(PageTable.DOUBLE,        LayoutName.DOUBLE_BG,       PathConfig.bg1, layout_mg.get_item_size(PageTable.DOUBLE, LayoutName.DOUBLE_BG))
        self.add_image(PageTable.ENDLESS,       LayoutName.ENDLESS_BG,      PathConfig.bg1, layout_mg.get_item_size(PageTable.ENDLESS, LayoutName.ENDLESS_BG))
        self.add_image(PageTable.SONG,          LayoutName.SONG_BG,         PathConfig.bg1, layout_mg.get_item_size(PageTable.SONG, LayoutName.SONG_BG))
        self.add_image(PageTable.HELP,          LayoutName.HELP_BG,         PathConfig.bg1, layout_mg.get_item_size(PageTable.HELP, LayoutName.HELP_BG))
        self.add_image(PageTable.RANK,          LayoutName.RANK_BG,         PathConfig.bg1, layout_mg.get_item_size(PageTable.RANK, LayoutName.RANK_BG))

        # 載入圖片
        name = LayoutNameManage.game_suffix_key(LayoutName.GAME_CLOCK, 0)
        self.add_image(
            PageTable.SINGLE,
            name,
            PathConfig.img_clock,
            layout_mg.get_item_size(PageTable.SINGLE, name)
        )
        self.add_image(
            PageTable.DOUBLE,
            name,
            PathConfig.img_clock,
            layout_mg.get_item_size(PageTable.DOUBLE, name)
        )
        self.add_image(
            PageTable.ENDLESS,
            name,
            PathConfig.img_clock,
            layout_mg.get_item_size(PageTable.ENDLESS,name)
        )
        self.add_image(
            PageTable.RANK,
            LayoutName.RANK_UNDERLINE,
            PathConfig.img_ranking,
            layout_mg.get_item_size(PageTable.RANK, LayoutName.RANK_UNDERLINE)
        )
        self.add_image(
            PageTable.RANK,
            LayoutName.RANK_FRAME,
            PathConfig.img_frame,
            layout_mg.get_item_size(PageTable.RANK, LayoutName.RANK_FRAME)
        )
        self.add_image(
            PageTable.HELP,
            LayoutName.HELP_LACE,
            PathConfig.img_lace,
            layout_mg.get_item_size(PageTable.HELP, LayoutName.HELP_LACE)
        )

    # ========= 圖片 =========
    def add_image(
            self,
            page:
            PageTable,
            name: str,
            file_path: Path,
            size: Size | None = None,
            fix: bool = True
        ):
        # 無縮放原圖cache存儲檢查
        if (file_path, None) not in self.img_cache:
            self.img_cache[(file_path, None)] = pygame.image.load(str(file_path))

        # 決定是否縮放原圖並存入快取
        key = (file_path, size)

        if key not in self.img_cache:
            # 將原圖cache暫存
            raw = self.img_cache[(file_path, None)]
            if size is None:
                self.img_cache[key] = raw
            else:
                self.img_cache[key] = pygame.transform.smoothscale(raw, (size.width, size.height))

        # 更新 page_images
        if fix:
            self.page_images_static[page][name] = self.img_cache[key]
        else:
            self.page_images_dynaic[page][name] = self.img_cache[key]

    def remove_image(self, page: PageTable, name: str):
        """刪除圖片"""
        if name in self.page_images_static[page]:
            del self.page_images_static[page][name]

    def clear_images(self, page: PageTable, static = True, dynamic = True):
        """清空頁面圖片"""
        if static:
            self.page_images_static[page].clear()
        if dynamic:
            self.page_images_dynaic[page].clear()

    # ========= 頁面切換 =========
    def switch_page(self, page: PageTable):
        self.current_page = page

    # ========= 其他工具 =========
    def get_image_size(self, file_path: Path):
        if file_path not in self.img_cache:
            self.img_cache[file_path] = pygame.image.load(str(file_path))
        surface = self.img_cache[file_path]
        width, height= surface.get_size()
        return Size(width, height)


screen_mg = ScreenManager()
