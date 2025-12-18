import pygame
from core.debug import dbg
from core.location_layout.variable import BaseParameter
from core.variable import PathConfig, Position


class FontsManager:
    def __init__(self):
        """
        初始化 FontsManager
        屬性：
        - font_map: 儲存渲染好的文字 { (name, size, color) : [pygame.Surface, ...] }
        - static_text: 固定字元，只渲染一次
        - dynamic_text: 動態字元，每幀刷新
        - _font_cache: font cache，避免重複建立 pygame.font.Font
        """
        self.x = 0
        self.y = 0
        self.y_gap = 0
        self.font_map = {}
        self._name_to_keys = {}  # { name: [ (name,font,size,color), ... ] }

        self.static_text = []      # 固定字元
        self.dynamic_text = []     # 動態字元
        self.static_pos = {"x":0, "y":0, "y_gap":0}
        self.dynamic_pos = {"x":0, "y":0, "y_gap":0}

        self._font_cache = {}      # font cache {size: pygame.font.Font}

    def show_texts(self, surface):
        # 固定字元
        for block in self.static_text:
            x_pos = block["pos"]["x"]
            y_pos = block["pos"]["y"]
            for surf in block["lines"]:
                temp = surf.copy()
                temp.set_alpha(block["alpha"])
                if block.get("direction", "vertical") == "vertical":
                    surface.blit(temp, (x_pos, y_pos))
                    y_pos += block["pos"]["y_gap"]
                else:  # horizontal
                    surface.blit(temp, (x_pos, y_pos))
                    x_pos += block["pos"]["x_gap"]

        # 動態字元
        for block in self.dynamic_text:
            x_pos = block["pos"]["x"]
            y_pos = block["pos"]["y"]
            for surf in block["lines"]:
                temp = surf.copy()
                temp.set_alpha(block["alpha"])
                if block.get("direction", "vertical") == "vertical":
                    surface.blit(temp, (x_pos, y_pos))
                    y_pos += block["pos"]["y_gap"]
                else:  # horizontal
                    surface.blit(temp, (x_pos, y_pos))
                    x_pos += block["pos"]["x_gap"]

    def renew_font(
            self,
            category,
            index,
            pos,
            y_gap = BaseParameter.y_gap,
            x_gap = BaseParameter.word,
            fixed = True,
            alpha_pec = 100,
            direction = "vertical"
        ):
        """
        切換文字版本並建立字塊
        - fixed: 是否加入 static_text 或 dynamic_text
        - alpha_pec: 透明度百分比 0~100
        - direction: 排列方向("vertical" 或 "horizontal")
        """
        if category not in self.font_map:
            dbg.log(f"{category} is not building in font_map")
            return

        font_list = self.font_map[category]
        if not (0 <= index < len(font_list)):
            dbg.log(f"{category}[{index}] out of range")
            return

        font_lines = font_list[index]["lines"]

        block = {
            "lines": font_lines,
            "pos": {"x": pos.x, "y": pos.y, "y_gap": y_gap, "x_gap": x_gap},
            "alpha": max(0, min(255, round(alpha_pec * 255 / 100))),
            "direction": direction
        }

        if fixed:
            self.static_text.append(block)
        else:
            self.dynamic_text.append(block)
        # print(f'{index} ---  {font_list[index]["raw_text"]}')

    def rendering_word(
            self,
            page_table,
            lines,
            color,
            size,
            font = PathConfig.font_base,
            start_line = 0,
            end_line = None
        ):
        """
        渲染文字並存入 font_map[name] 的 list
        """
        start_line, end_line = self._clamp_lines(start_line, end_line, lines)
        if start_line == -1 and end_line == -1: return

        font_obj = self._get_font(font, size)
        rendered_word = [font_obj.render(line, True, color) for line in lines[start_line:end_line]]

        # 先確保 font_map[name] 存在，不存在則建議個新的
        if page_table not in self.font_map:
            self.font_map[page_table] = []

        # 把新font塞進 font_map 的list
        self.font_map[page_table].append({
            "size":     size,
            "color":    color,
            "font":     font,
            "lines":    rendered_word,
            "raw_text": lines[start_line:end_line]  # 原始文字(用來debug)
        })

    def current_clear(self, static = True, dynamic = True):
        """
        清空目前動態字元
        """
        if static:
            self.static_text = []
        if dynamic:
            self.dynamic_text = []

    def _get_font(self, font, size):
        """
        取得 font 物件，並使用 _font_cache 做快取
        (針對相同字體 + 相同大小，避免重複建立)
        """
        key = (font, size)
        if key not in self._font_cache:
            self._font_cache[key] = pygame.font.Font(font, size)

        return self._font_cache[key]

    @staticmethod
    def _clamp_lines(start, end, lines):
        """
        限制 start/end 在有效行數範圍內
        - 如果超過範圍，調整成合法值
        - 回傳 (start, end)
        """
        length = len(lines)
        if end is None:
            end = length

        if end < start:
            dbg.log("end_line < start_line")
            return -1, -1

        start   = max(0, start)
        end     = min(length, end)

        return start, end

fonts_mg = FontsManager()
