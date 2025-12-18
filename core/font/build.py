from core.font.json_manager import json_mg
from core.variable import PageTable, PathConfig


def build_json():
    file_path = PathConfig.json_save

    data = {
        PageTable.SONG.value: {
            "select_song": [
                10
            ],
            "volume": [
                10
            ]
        },
        PageTable.RANK.value: [
            [0,0,0],
            [0,0,0],
            [0,0,0]
        ]
    }

    json_mg.write_json(file_path, data, mode='w', encoding = None, indent = 4)
    print(f"JSON 已生成: {file_path}")
