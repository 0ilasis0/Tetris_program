class ScreenConfig:
    title_name = 'Tetris'

    # 實際執行時的解析度 (可變動)
    width  = 1980
    height = 1080

    # --- 新增：設計稿基準解析度 (固定不動) ---
    DESIGN_WIDTH  = 1980
    DESIGN_HEIGHT = 1080

    # 計算縮放倍率 (ScreenRatio)
    RATIO = width / DESIGN_WIDTH
