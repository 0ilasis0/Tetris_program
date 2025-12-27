from core.variable import PageTable

class RenewJSON:
    """
    負責定義各個 JSON 檔案的初始內容結構
    """
    @staticmethod
    def single_object(data: dict):
        """ 初始化 Single Object 相關資料 """
        pass
        # page_key = PageTable.SINGLE.value
        # data[page_key] = {}

        # # ... (您原本的生成邏輯) ...
        # for level in range(0, single_object_config.level_amount):
        #     level_key = single_object_config.name_level + f"{level}"
        #     data[page_key][level_key] = {}
        #     for obj_idx in range(0, single_object_config.store_amount[single_object_config.name_level + f"{level}"]):
        #         obj_key = single_object_config.name_object + f"{obj_idx}"
        #         data[page_key][level_key][obj_key] = {
        #             "name": f"{level_key}_{obj_key}",
        #             "size": [single_object_config.jell_size, single_object_config.jell_size],
        #             "pos": [0, 0],
        #             "other": [0]
        #         }

        # for number in range(0, single_object_config.dot_amount):
        #     data[page_key][single_object_config.name_dot + f"{number}"] = {
        #         "name": single_object_config.name_dot + f"{number}",
        #         "size": [single_object_config.dot_size, single_object_config.dot_size],
        #         "pos": [0, 0],
        #         "other": [0]
        #     }
