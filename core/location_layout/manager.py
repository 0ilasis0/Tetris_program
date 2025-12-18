from dataclasses import dataclass, field

from core.debug import dbg
from core.location_layout.base import layout_config
from core.location_layout.variable import Position, Size


@dataclass
class LayoutItem:
    category: str       # 分類，例如 'MENU', 'SINGLE' 等
    name: str           # 唯一名稱
    size: Size
    pos: Position = field(default_factory = Position.zero)
    content = None      # 可以是文字、按鈕、圖片等



class LayoutManager:
    def __init__(self, screen_width, screen_height):
        self.screen_size = Size(screen_width, screen_height)
        self.items = {}

    def add_item(self, item: LayoutItem, x = None, y = None):
        ''' 加入 item，可選位置 '''
        # 如果沒有傳入 x, y → 使用 item 原本的座標
        if (x is None or y is None):
            if (item.pos.x is not None) and (item.pos.y is not None):
                (x, y) = (item.pos.x, item.pos.y)
            else:
                dbg.log(f"[add_item] No position for item '{item.category}.{item.name}'")
                return None

        if item.category not in self.items:
            self.items[item.category] = {}

        item.pos = Position(x, y)

        # 如果名字已存在 → 警告
        if item.name in self.items[item.category]:
            dbg.log(f"[add_item] Overwriting item '{item.category}.{item.name}'")

        # 存入 dict
        self.items[item.category][item.name] = item
        return item

    def add_center(self, item: LayoutItem, target = None, gap_x = 0, gap_y = 0):
        ''' 置中 '''
        if target == None:
            item.pos = Position(
                x = (self.screen_size.width - item.size.width + gap_x) // 2,
                y = (self.screen_size.height - item.size.height + gap_y) // 2
            )
        else:
            item.pos = Position(
                x = target.pos.x + (target.size.width - item.size.width) // 2 + gap_x,
                y = target.pos.y + (target.size.height - item.size.height) // 2 + gap_y
            )

        return self.add_item(item)

    def add_symmetric(
            self,
            item: LayoutItem,
            target: LayoutItem,
            axis: str = "vertical",
            gap_x = 0,
            gap_y = 0,
        ):
        """
        讓 item 根據 target 對稱
        "vertical"   → 左右對稱 (以畫面中心垂直線為對稱軸)
        "horizontal" → 上下對稱 (以畫面中心水平線為對稱軸)
        """
        center_x = self.screen_size.width // 2
        center_y = self.screen_size.height // 2

        if axis == "vertical":
            # 左右對稱：X 翻轉，Y 不變
            dx = target.pos.x - center_x
            item_x = center_x - dx - item.size.width
            item_y = target.pos.y
        elif axis == "horizontal":
            # 上下對稱：Y 翻轉，X 不變
            dy = target.pos.y - center_y
            item_y = center_y - dy - item.size.height
            item_x = target.pos.x
        else:
            raise ValueError("axis 只能是 'vertical' 或 'horizontal'")

        item.pos = Position(round(item_x + gap_x), round(item_y + gap_y))
        return self.add_item(item)

    def add_below(
            self,
            item: LayoutItem,
            target,
            gap = layout_config.y_gap,
            align = 'left'
        ):
        '''
        垂直堆疊
        parameter: left center right
        '''
        if align == 'left':
            x = target.pos.x
        elif align == 'center':
            x = target.pos.x + (target.size.width - item.size.width)//2
        elif align == 'right':
            x = target.pos.x + target.size.width - item.size.width
        else:
            raise ValueError(f"align = {align} 無效")

        y = target.pos.y + target.size.height + gap
        item.pos = Position(round(x), round(y))
        return self.add_item(item)

    def add_right_of(
            self,
            item: LayoutItem,
            target,
            gap_x = 0,
            gap_y = 0,
            align = 'top'
            ):
        '''
        水平排列
        parameter: top center bottom
        '''
        if align == 'top':
            y = target.pos.y
        elif align == 'center':
            y = target.pos.y + (target.size.height - item.size.height) // 2
        elif align == 'bottom':
            y = target.pos.y + target.size.height - item.size.height
        else:
            raise ValueError(f"align={align} 無效")

        item.pos = Position(round(target.pos.x + target.size.width + gap_x), round(y + gap_y))
        return self.add_item(item)

    def add_left_of(
            self,
            item: LayoutItem,
            target,
            gap_y = 0,
            gap_x = 0,
            align = 'top'
        ):
        '''
        水平排列
        parameter: top center bottom
        '''
        if align == 'top':
            y = target.pos.y
        elif align == 'center':
            y = target.pos.y + (target.size.height - item.size.height) // 2
        elif align == 'bottom':
            y = target.pos.y + target.size.height - item.size.height
        else:
            raise ValueError(f"align={align} 無效")

        # 跟 add_right_of 相反：放在 target 左邊
        item.pos = Position(round(target.pos.x + gap_x - item.size.width), round(y + gap_y))
        return self.add_item(item)

    def add_inner(
            self,
            item: LayoutItem,
            target,
            align = 'left_tp',
            gap_x = 0,
            gap_y = 0,
    ):
        '''
        內部重疊
        parameter:  left_tp center_tp right_tp
                    left_bt center_bt right_bt
        '''
        if (item.pos is None) or (target.pos is None):
            dbg.log(f'{item.name}->{item.pos} or {target.name}->{target.pos} pos is None')
        horizontal, vertical = align.split("_")

        # 水平
        if horizontal == "left":
            x = target.pos.x
        elif horizontal == "center":
            x = target.pos.x + (target.size.width - item.size.width) // 2
        elif horizontal == "right":
            x = target.pos.x + target.size.width - item.size.width
        else:
            raise ValueError(f"水平對齊 {horizontal} 無效")

        # 垂直
        if vertical == "tp":
            y = target.pos.y
        elif vertical == "bt":
            y = target.pos.y + target.size.height - item.size.height
        else:
            raise ValueError(f"垂直對齊 {vertical} 無效")

        item.pos = Position(round(x + gap_x), round(y + gap_y))
        return self.add_item(item)

    def get_item_pos(self, category, name = None, index = None, extra_x = 0, extra_y = 0):
        """
        透過 category + name 取得 item 的 (x, y) 座標
        如果不存在，回傳 None
          """
        item = self.get_item(category, name, index)

        if item is None:
            dbg.log(f'{category}->{name} get_item is error')
            return None

        item_x, item_y = item.pos.x, item.pos.y

        return Position(item_x + extra_x, item_y + extra_y)

    def get_item_size(self, category, name = None, index = None):
        """
        透過 category + name 取得 item 的 (width, height)
        如果不存在，回傳 None
        """
        item = self.get_item(category, name, index)

        if item is None:
            dbg.log(f'{category}->{name} get_item is error')
            return None

        return Size(item.size.width, item.size.height)

    def get_item(self, category, name = None, index = None):
        """
        取得 LayoutItem
        - 支援用 name 或 index 查
        - 不存在則回傳 None
        """
        if category not in self.items:
            dbg.log(f"{category} 不存在")
            return None

        if name is not None:
            item = self.items.get(category, {}).get(name)
            if not item:
                dbg.log(f"{category} -> {name} 不存在")
                return None
            return item

        elif index is not None:
            items = list(self.items[category].values())
            if not (0 <= index < len(items)):
                dbg.log(f"{category} index {index} 超出範圍")
                return None
            return items[index]

        else:
            dbg.log("get_item 必須提供 name 或 index")
            return None

    def get_items_by_category(
            self,
            category,
            start_index = None,
            end_index = None
            ):
        ''' 透過 category 取得 items，可指定範圍 '''
        items_in_category = list(self.items.get(category, {}).values())

        if (start_index is not None) or (end_index is not None):
            items_in_category = items_in_category[start_index:end_index]

        return items_in_category





''' 此為font_mg的dlc，但目前不會用到也少用 '''
    # def stack_vertical(
    #         self,
    #         items,
    #         start_pos,
    #         gap = layout_config.y_gap,
    #         align = 'left'
    #         ):
    #     '''
    #     批量垂直排列
    #     parameter: left center right
    #     '''
    #     x, y = start_pos.x, start_pos.y
    #     for item in items:
    #         if align == 'left':
    #             item_x = x
    #         elif align == 'center':
    #             item_x = x - item.size.width // 2
    #         elif align == 'right':
    #             item_x = x - item.size.width
    #         else:
    #             raise ValueError(f"align={align} 無效")

    #         item.pos = Position(item_x, y)
    #         self.add_item(item)
    #         y += item.size.height + gap

    # def stack_horizontal(
    #         self,
    #         items,
    #         start_pos,
    #         gap = layout_config.y_gap,
    #         align='top'
    #         ):
    #     '''
    #     批量水平排列
    #     parameter: top center bottom
    #     '''
    #     x, y = start_pos.x, start_pos.y
    #     for item in items:
    #         if align == 'top':
    #             item_y = y
    #         elif align == 'center':
    #             item_y = y - item.size.height // 2
    #         elif align == 'bottom':
    #             item_y = y - item.size.height
    #         else:
    #             raise ValueError(f"align={align} 無效")

    #         item.pos = Position(x, item_y)
    #         self.add_item(item)
    #         x += item.size.width + gap
