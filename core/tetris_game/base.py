import random

from core.location_layout.variable import Position, Size
from core.tetris_game.variable import GameVariable, figures


class Tetromino:
    def __init__(
            self,
            x = GameVariable.WIDTH_BLOCK // 2 - GameVariable.CELL_BLOCK + 1,
            y = 0,
            type_name   = None,
            color       = None,
            cell        = None,
            rotation    = 0
        ):
        '''Tetromino.x, Tetromino.y = 方塊 4×4 bounding box 的左上角位置 (場地座標系統裡)'''
        # 隨機挑選一個方塊類型
        self.type_name = type_name or random.choice(list(figures.keys()))
        self.x = x
        self.y = y
        # 初始旋轉狀態
        self.rotation = rotation
        # 該方塊的顏色與方塊旋轉所占格子
        self.color = color or figures[self.type_name]["color"]
        self.cell  = cell or figures[self.type_name]["rotations"]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.cell)

    def get_cell_position(self, idx):
        """
        得到cell的實體方塊位在地圖中的位置
        輸入: idx (0~3) -> 第幾個方塊
        輸出: (x, y) -> 在場地中的座標
        """
        grid_idx = self.get_shape()[idx]   # 0~15 (4x4)
        offset_x = grid_idx % GameVariable.CELL_BLOCK            # 橫向偏移
        offset_y = grid_idx // GameVariable.CELL_BLOCK           # 縱向偏移
        return (self.x + offset_x, self.y + offset_y)

    def get_shape(self):
        return self.cell[self.rotation]

    def tetromino_to_matrix(self, tetromino_cell):
        ''' 將[1,2,6,7]此格式轉成完整的4*4 cells 含顏色'''
        # 如果是空的回傳1*1透明矩陣
        if tetromino_cell is None: return [[None]]

        # 建立一個 None 組成的矩陣
        matrix = [[None for _ in range(GameVariable.CELL_BLOCK)] for _ in range(GameVariable.CELL_BLOCK)]
        shape = tetromino_cell.get_shape()
        color = tetromino_cell.color
        for idx in shape:
            row = idx // GameVariable.CELL_BLOCK
            col = idx % GameVariable.CELL_BLOCK
            matrix[row][col] = color
        return matrix

    def clone(self):
        """回傳此 Tetromino 的完整複製（同屬性但獨立物件）"""
        return Tetromino(
            x = self.x,
            y = self.y,
            type_name = self.type_name,
            color = self.color,
            cell = self.cell,
            rotation = self.rotation
        )


class Field:
    def __init__(
            self,
            width_block,
            height_block,
            zoom = GameVariable.ZOOM_SIZE
        ):
        self.width_block = width_block
        self.height_block = height_block
        self.grid = [[GameVariable.EMPTY_COLOR for _ in range(width_block)] for _ in range(height_block)]

        # 顯示用位置與方塊單位大小
        self.zoom = zoom

    def check_collision(self, tetromino: Tetromino, dx = 0, dy = 0):
        """
        檢查 tetromino 移動 dx/dy 後是否碰撞，不修改 grid
        return:True(碰撞)/False(沒問題)
        """
        for i in range(GameVariable.CELL_BLOCK):
            for j in range(GameVariable.CELL_BLOCK):
                idx = i * GameVariable.CELL_BLOCK + j
                if idx in tetromino.get_shape():
                    x = int(tetromino.x + j + dx)
                    y = int(tetromino.y + i + dy)
                    if x < 0 or x >= self.width_block or y >= self.height_block:
                        return True
                    if y >= 0 and self.grid[y][x] != GameVariable.EMPTY_COLOR:
                        return True
        return False

    def freeze(self, tetromino: Tetromino):
        '''
        把 tetromino 固定到 grid 上
        '''
        for i in range(GameVariable.CELL_BLOCK):
            for j in range(GameVariable.CELL_BLOCK):
                idx = i * GameVariable.CELL_BLOCK + j
                if idx in tetromino.get_shape():
                    x = tetromino.x + j
                    y = tetromino.y + i
                    if 0 <= x < self.width_block and 0 <= y < self.height_block:
                        self.grid[y][x] = tetromino.color

    def clear_lines(self, empty_color = GameVariable.EMPTY_COLOR, mine_color = GameVariable.MINE_COLOR):
        """
        檢查是否需要消行
        如果要則消除整行並補空行在最上面0的位置
        return：消行數
        """
        new_grid = []
        for row in self.grid:
            # 判斷這行是不是滿格
            is_full = all(cell != empty_color for cell in row)
            # 判斷這行有沒有地雷
            has_mine = any(cell == mine_color for cell in row)

            # 只有「滿格且沒有地雷」才要清掉
            if is_full and not has_mine:
                continue  # 跳過，不放進 new_grid（等於刪行）

            new_grid.append(row)

        lines_cleared = self.height_block - len(new_grid)
        for _ in range(lines_cleared):
            new_grid.insert(0, [empty_color]*self.width_block)

        # 將新的 grid 搬到原先的 grid
        self.grid[:] = new_grid
        return lines_cleared



class TetrisRenderer:
    def __init__(self, grid, width_block, height_block, zoom) -> None:
        self.grid           = grid
        self.width_block    = width_block
        self.height_block   = height_block
        self.zoom           = zoom

    def draw_grid(
            self,
            draw_mgr,
            category,
            pos: Position,
            width_block,
            height_block,
            fixed = True,
        ):
        ''' 畫整個網格線 '''
        # 畫垂直線
        for x in range(width_block + 1):
            draw_mgr.add_form(
                category = category,
                name = f"vline_{x}",
                shape = "rect",
                pos = Position(pos.x + x * self.zoom, pos.y),
                size = Size(1, height_block * self.zoom),
                color = GameVariable.GRID_COLOR,
                hollow = 0,
                fixed = fixed
            )
        # 畫水平線
        for y in range(height_block + 1):
            draw_mgr.add_form(
                category = category,
                name = f"hline_{y}",
                shape = "rect",
                pos = Position(pos.x, pos.y + y * self.zoom),
                size = Size(width_block * self.zoom, 1),
                color = GameVariable.GRID_COLOR,
                hollow = 0,
                fixed = fixed
            )

    def draw_cells(
            self,
            draw_mgr,
            category,
            cells, pos: Position,
            other_x = 0,
            other_y = 0,
            fixed = True
            ):
        # 支援位置列表 [(x,y),...] 或二維矩陣
        if isinstance(cells, list) and cells and isinstance(cells[0], tuple):
            for x, y in cells:
                draw_mgr.add_form(
                    category = category,
                    name = f"{category}_cell_{x}_{y}",
                    shape = "rect",
                    pos = Position(pos.x + x * self.zoom + other_x, pos.y + y * self.zoom + other_y),
                    size = Size(self.zoom, self.zoom),
                    color = self.grid[y][x] if 0<=y<self.height_block and 0<=x<self.width_block else GameVariable.EMPTY_COLOR,
                    hollow = 0,
                    fixed = fixed
                )
        else:
            # 二維陣列處理
            for y, row in enumerate(cells):
                for x, color in enumerate(row):
                    if color is None: continue

                    draw_mgr.add_form(
                        category = category,
                        name = f"{category}_cell_{x}_{y}",
                        shape = "rect",
                        pos = Position(pos.x + x * self.zoom + other_x, pos.y + y * self.zoom + other_y),
                        size = Size(self.zoom, self.zoom),
                        color = color,
                        hollow = 0,
                        fixed = fixed
                    )

