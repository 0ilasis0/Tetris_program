import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


@dataclass(frozen = True)
class Size:
    width: int
    height: int

@dataclass(frozen = True)
class Position:
    x: int
    y: int

    @classmethod
    def zero(cls):
        return cls(0,0)

#
# 路徑
#
PATH_ROOT = Path(__file__).resolve().parent.parent

def resource_path(relative_path):
    """
    取得外部資源路徑：
    - 打包成 exe 時：使用 exe 同目錄
    - 開發模式：使用專案根目錄
    """
    if getattr(sys, "frozen", False):
        # exe 打包後使用的路徑
        base_path = Path(sys.executable).parent
    else:
        # 開發環境使用的路徑
        base_path = PATH_ROOT
    return base_path / relative_path

class PathBase:
    background = resource_path("background")
    img        = resource_path("img")
    icon       = resource_path("images.ico")
    json       = resource_path("data")
    song       = resource_path("song")
    font       = resource_path("font")



class PathConfig:
    bg1         = PathBase.background / "background1.jpg"
    img_clock   = PathBase.img / "clock.jpg"
    img_panel   = [
        PathBase.img / "panel1.png",
        PathBase.img / "panel2.png",
        PathBase.img / "panel3.png"
    ]
    img_lace    = PathBase.img / "lace.png"
    img_ranking = PathBase.img / "ranking.png"
    img_frame   = PathBase.img / "frame.png"

    font_base   = PathBase.font / 'NotoSansTC-VariableFont_wght.ttf'
    font_eng    = PathBase.font / 'PressStart2P-Regular.ttf'
    font_eng2   = PathBase.font / 'Audiowide-Regular.ttf'

    json_save   = PathBase.json / "save.json"
    json_display= PathBase.json / "display.json"
    json_help   = PathBase.json / "help.json"



#
# 顏色
#
colors = [
    [255, 215, 0],      #0 Gold
    [255, 255, 255],    #1 White
    [128, 128, 128],    #2 Grey
    [0, 0, 0],          #3 Black
    [80, 134, 22],      #4 Green
    [30, 30, 255],      #5 Light Blue
    [120, 37, 179],     #6 Purple
    [180, 34, 22],      #7 Red
    [255, 165, 0],      #8 Orange
    [100, 179, 179],    #9 Cyan
    [80, 34, 22],       #10 Dark Brown
    [180, 34, 122],     #11 Magenta
    [255, 105, 180],    #12 Hot Pink
    [135, 206, 235],    #13 Sky Blue
    [144, 238, 144],    #14 Light Green
    [255, 140, 0],      #15 Dark Orange
    [186, 85, 211],     #16 Orchid
]



#
# JSON檔案內路徑
#
class JsonPath(Enum):
    # SONG
    SONG = 'SONG'
    VOLUME = 'volume'
    SELECT_SONG = 'select_song'



#
# 目錄標籤
#
class PageTable(Enum):
    # catolog
    MENU        = 'MENU'
    SINGLE      = 'SINGLE'
    SINGLE_MENU = 'SINGLE_MENU'
    DOUBLE      = 'DOUBLE'
    ENDLESS     = 'ENDLESS'
    SONG        = 'SONG'
    HELP        = 'HELP'
    RANK        = 'RANK'
    EXIT        = 'EXIT'
