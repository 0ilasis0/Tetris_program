from core.font.font_manager import fonts_mg
from core.font.json_manager import json_mg
from core.font.variable import RenderingWord
from core.hmi.song import song_mg
from core.location_layout.variable import BaseParameter
from core.tetris_game.variable import GameVariable, RankVariable
from core.variable import PageTable, PathConfig, colors


def rendering():
    ''' 變動文本渲染 '''
    # BASE
    for i in range(GameVariable.MAX_SCORE):
        fonts_mg.rendering_word(
            page_table  = 'BASE',
            lines = [str(i)],
            color = colors[3],
            size  = BaseParameter.word,
            font  = PathConfig.font_eng
        )

    # GAME
    fonts_mg.font_map[PageTable.SINGLE] = fonts_mg.font_map['BASE'][:]

    for i in range(GameVariable.MAX_COMBO // 4):
        for j in range(GameVariable.MAX_COMBO // 5):
            fonts_mg.rendering_word(
                page_table  = PageTable.SINGLE,
                lines = [str(j + i * (GameVariable.MAX_COMBO // 5))],
                color = colors[i + 3],
                size  = BaseParameter.word_big,
                font  = PathConfig.font_eng
            )
    for i in range(GameVariable.MAX_KO_COUNT):
        fonts_mg.rendering_word(
            page_table  = PageTable.SINGLE,
            lines = [RenderingWord.KO.value + str(i + 1)],
            color = colors[7],
            size  = BaseParameter.word_mini,
            font  = PathConfig.font_eng
        )

    # SONG
    for file_name in song_mg.files_name:
        fonts_mg.rendering_word(
            page_table    = PageTable.SONG,
            lines   = [file_name],
            color   = colors[3],
            size    = BaseParameter.word,
            font    = PathConfig.font_base
        )
    fonts_mg.rendering_word(
        page_table    = PageTable.SONG,
        lines   = [RenderingWord.SHUFFLE.value],
        color   = colors[13],
        size    = BaseParameter.word,
        font    = PathConfig.font_base
    )



    ''' 固定文本渲染 '''
    # MENU
    fonts_mg.rendering_word(
        page_table    = PageTable.MENU,
        lines   = json_mg.word_list_data.get(PageTable.MENU, []),
        color   = colors[3],
        size    = BaseParameter.word,
        font    = PathConfig.font_base
    )

    # GAME
    fonts_mg.rendering_word(
        page_table    = PageTable.SINGLE,
        lines   = [RenderingWord.COMBO.value],
        color   = colors[3],
        size    = BaseParameter.word,
        font    = PathConfig.font_eng2
    )
    fonts_mg.rendering_word(
        page_table    = PageTable.SINGLE,
        lines   = [RenderingWord.SCORE.value],
        color   = colors[3],
        size    = BaseParameter.word,
        font    = PathConfig.font_eng2
    )

    # SINGLE_MENU
    fonts_mg.font_map[PageTable.SINGLE_MENU] = fonts_mg.font_map[PageTable.SINGLE][:]

    # ENDLESS
    fonts_mg.font_map[PageTable.ENDLESS] = fonts_mg.font_map[PageTable.SINGLE][:]

    # DOUBLE
    fonts_mg.font_map[PageTable.DOUBLE] = fonts_mg.font_map[PageTable.SINGLE][:]

    # SONG
    fonts_mg.rendering_word(
        page_table    = PageTable.SONG,
        lines   = json_mg.word_list_data.get(PageTable.SONG, []),
        color   = colors[3],
        size    = BaseParameter.word,
        font    = PathConfig.font_base
    )

    # HELP
    for _, content in json_mg.word_dict_data[PageTable.HELP.value].items():
        # 把 title 當主標題，description 當內文
        fonts_mg.rendering_word(
            page_table = PageTable.HELP,
            lines      = content["title"],
            color      = colors[3],
            size       = BaseParameter.word,
            font       = PathConfig.font_base
        )

        fonts_mg.rendering_word(
            page_table = PageTable.HELP,
            lines      = content["description"],
            color      = colors[3],
            size       = BaseParameter.word,
            font       = PathConfig.font_base
        )

    # RANK
    fonts_mg.font_map[PageTable.RANK] = fonts_mg.font_map['BASE'][:]

    for number in range(RankVariable.RANK_TOTAL):
        fonts_mg.rendering_word(
            page_table    = PageTable.RANK,
            lines   = [RenderingWord.RANKING.value + f'{number + 1}'],
            color   = colors[8],
            size    = BaseParameter.word_big,
            font    = PathConfig.font_base
        )
    fonts_mg.rendering_word(
        page_table    = PageTable.RANK,
        lines   = [RenderingWord.MIN.value],
        color   = colors[3],
        size    = BaseParameter.word,
        font    = PathConfig.font_base
    )
    fonts_mg.rendering_word(
        page_table    = PageTable.RANK,
        lines   = [RenderingWord.SEC.value],
        color   = colors[3],
        size    = BaseParameter.word,
        font    = PathConfig.font_base
    )
    fonts_mg.rendering_word(
        page_table    = PageTable.RANK,
        lines   = [RenderingWord.FRACTION.value],
        color   = colors[3],
        size    = BaseParameter.word,
        font    = PathConfig.font_base
    )
