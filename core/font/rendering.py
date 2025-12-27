from core.font.manager import font_mg
from core.font.variable import RenderingWord
from core.hmi.config.main import sys_config_mg
from core.json.manager import json_mg
from core.location_layout.variable import location_config
from core.tetris_game.variable import GameVar, RankVar
from core.variable import PageTable, PathConfig, colors


def rendering_reload_setup():
    font_mg.clear_map()
    rendering()

def rendering():
    ''' 變動文本渲染 '''
    # BASE
    for i in range(GameVar.MAX_SCORE):
        font_mg.rendering_word(
            page_table  = 'BASE',
            lines = [str(i)],
            color = colors[3],
            size  = location_config.word,
            font  = PathConfig.font_eng
        )

    # GAME
    font_mg.font_map[PageTable.SINGLE] = font_mg.font_map['BASE'][:]

    for i in range(GameVar.MAX_COMBO // 4):
        for j in range(GameVar.MAX_COMBO // 5):
            font_mg.rendering_word(
                page_table  = PageTable.SINGLE,
                lines = [str(j + i * (GameVar.MAX_COMBO // 5))],
                color = colors[i + 3],
                size  = location_config.word_big,
                font  = PathConfig.font_eng
            )
    for i in range(GameVar.MAX_KO_COUNT):
        font_mg.rendering_word(
            page_table  = PageTable.SINGLE,
            lines = [RenderingWord.KO.value + str(i + 1)],
            color = colors[7],
            size  = location_config.word_mini,
            font  = PathConfig.font_eng
        )

    # SYS_CONFIG
    for file_name in sys_config_mg.files_name:
        font_mg.rendering_word(
            page_table    = PageTable.SYS_CONFIG,
            lines   = [file_name],
            color   = colors[3],
            size    = location_config.word,
            font    = PathConfig.font_base
        )
    font_mg.rendering_word(
        page_table    = PageTable.SYS_CONFIG,
        lines   = [RenderingWord.SHUFFLE.value],
        color   = colors[13],
        size    = location_config.word,
        font    = PathConfig.font_base
    )
    for lines in RenderingWord.WINDOW_SCALE_NUMBER.value:
        font_mg.rendering_word(
            page_table    = PageTable.SYS_CONFIG,
            lines   = lines,
            color   = colors[3],
            size    = location_config.word,
            font    = PathConfig.font_base
        )


    ''' 固定文本渲染 '''
    # MENU
    font_mg.rendering_word(
        page_table    = PageTable.MENU,
        lines   = json_mg.word_list_data.get(PageTable.MENU, []),
        color   = colors[3],
        size    = location_config.word,
        font    = PathConfig.font_base
    )

    # GAME
    font_mg.rendering_word(
        page_table    = PageTable.SINGLE,
        lines   = [RenderingWord.COMBO.value],
        color   = colors[3],
        size    = location_config.word,
        font    = PathConfig.font_eng2
    )
    font_mg.rendering_word(
        page_table    = PageTable.SINGLE,
        lines   = [RenderingWord.SCORE.value],
        color   = colors[3],
        size    = location_config.word,
        font    = PathConfig.font_eng2
    )

    # SINGLE_MENU
    font_mg.font_map[PageTable.SINGLE_MENU] = font_mg.font_map[PageTable.SINGLE][:]

    # ENDLESS
    font_mg.font_map[PageTable.ENDLESS] = font_mg.font_map[PageTable.SINGLE][:]

    # DOUBLE
    font_mg.font_map[PageTable.DOUBLE] = font_mg.font_map[PageTable.SINGLE][:]

    # SYS_CONFIG
    font_mg.rendering_word(
        page_table    = PageTable.SYS_CONFIG,
        lines   = json_mg.word_list_data.get(PageTable.SYS_CONFIG, []),
        color   = colors[3],
        size    = location_config.word,
        font    = PathConfig.font_base
    )

    # HELP
    for _, content in json_mg.word_dict_data[PageTable.HELP.value].items():
        # 把 title 當主標題，description 當內文
        font_mg.rendering_word(
            page_table = PageTable.HELP,
            lines      = content["title"],
            color      = colors[3],
            size       = location_config.word,
            font       = PathConfig.font_base
        )

        font_mg.rendering_word(
            page_table = PageTable.HELP,
            lines      = content["description"],
            color      = colors[3],
            size       = location_config.word,
            font       = PathConfig.font_base
        )

    # RANK
    font_mg.font_map[PageTable.RANK] = font_mg.font_map['BASE'][:]

    for number in range(RankVar.RANK_TOTAL):
        font_mg.rendering_word(
            page_table    = PageTable.RANK,
            lines   = [RenderingWord.RANKING.value + f'{number + 1}'],
            color   = colors[8],
            size    = location_config.word_big,
            font    = PathConfig.font_base
        )
    font_mg.rendering_word(
        page_table    = PageTable.RANK,
        lines   = [RenderingWord.MIN.value],
        color   = colors[3],
        size    = location_config.word,
        font    = PathConfig.font_base
    )
    font_mg.rendering_word(
        page_table    = PageTable.RANK,
        lines   = [RenderingWord.SEC.value],
        color   = colors[3],
        size    = location_config.word,
        font    = PathConfig.font_base
    )
    font_mg.rendering_word(
        page_table    = PageTable.RANK,
        lines   = [RenderingWord.FRACTION.value],
        color   = colors[3],
        size    = location_config.word,
        font    = PathConfig.font_base
    )
