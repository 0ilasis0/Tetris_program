from copy import deepcopy

from core.debug import dbg


class Cell:
    """每個格子的資料結構，完全用 keyword arguments 存資料"""
    def __init__(self, **keyword_arguments):
        self.data = keyword_arguments  # 所有資料統一存到 data 字典

    def is_empty(self):
        ''' 未來可以用來快速判斷cell是否有物品 '''
        return not bool(self.data)

    def clear(self):
        self.data.clear()

    def __repr__(self):
        return f"Cell({self.data})"



class GridManager:
    """通用二維格子管理器，支援工作檯、櫃子快照與游標"""
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.storage = {}  # 櫃子快照
        self.cursor_x = 0
        self.cursor_y = 0
        self.max_x = max(cols - 1, 0)
        self.max_y = max(rows - 1, 0)

    # ------------------ 格子操作 ------------------ #
    def set_cell(self, x: int, y: int, **keyword_arguments):
        if 0 <= y < self.rows and 0 <= x < self.cols:
            self.grid[y][x] = Cell(**keyword_arguments)

    def get_cell(self, x: int, y: int) -> Cell:
        if 0 <= y < self.rows and 0 <= x < self.cols:
            return self.grid[y][x]
        dbg.log('x y is over the range')
        return None

    def clear_cell(self, x: int, y: int):
        cell = self.get_cell(x, y)
        if cell:
            cell.clear()

    def clear_grid(self):
        """清理整個工作檯所有格子"""
        for row in self.grid:
            for cell in row:
                cell.clear()

    # ------------------ 快照操作 ------------------ #
    def save(self, key: str):
        """將當前工作檯儲存到櫃子"""
        self.storage[key] = deepcopy(self.grid)

    def load(self, key: str):
        """從櫃子載入到工作檯"""
        if key in self.storage:
            self.grid = deepcopy(self.storage[key])

    def clear_storage(self, key: str):
        """清理指定櫃子格子"""
        if key in self.storage:
            self.storage[key] = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]

    # ------------------ 顯示 / debug ------------------ #
    def print_grid(self):
        for y, row in enumerate(self.grid):
            line = []
            for x, cell in enumerate(row):
                if self.cursor_x == x and self.cursor_y == y:
                    line.append(f"[{cell.data or ' '}]")  # 游標標記
                else:
                    line.append(f" {cell.data or ' '} ")
            print(" ".join(line))
