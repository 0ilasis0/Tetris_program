import os

from core.base import central_mg
from core.font.rendering import rendering_reload_setup
from core.location_layout.base import layout_config
from core.location_layout.main import layout_collection
from core.location_layout.variable import location_config
from core.page.base import page_mg
from core.page.variable import RankConfig
from core.screen.image import img_mg
from core.screen.variable import ScreenConfig


def reload_sys_window_scale():
    if central_mg.sys_window_scale_pending is not None:
        # 將螢幕移回正中間，已顯示右上角符號
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        # 需要從新進入boot一次
        page_mg.current_boot = page_mg.current_page

        ScreenConfig.set_resolution_ratio(central_mg.sys_window_scale_pending)
        location_config.reload_setup()
        layout_config.reload_setup()
        layout_collection.reload_setup()
        rendering_reload_setup()
        RankConfig.reload_setup()
        img_mg.reload_setup()

        central_mg.sys_window_scale_pending = None
