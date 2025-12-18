from core.variable import PageTable


class PageTree:
    def __init__(self, name):
        self.name = name          # 節點名稱（TableStore 名稱）
        self.children = []        # 子節點
        self.parent = None        # 父節點
        self.family_table = {}    # 小家庭分支{index: 子頁名稱}

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)

    def get_catalog_to_click(self, family_table):
        return {i: child.name for i, child in enumerate(family_table)}

    def update_catalog_recursive(self):
        # 建立所有父子索引對照表 (hook_y)
        if self.children:
            self.family_table = {i: child.name for i, child in enumerate(self.children)}
            for child in self.children:
                child.update_catalog_recursive()


#
# 建立樹狀頁面節點
#
tree_path_table = {
    # 主選單
    PageTable.MENU:    PageTree(PageTable.MENU),
    # 子頁
    PageTable.SINGLE_MENU: PageTree(PageTable.SINGLE_MENU),
    PageTable.SINGLE:  PageTree(PageTable.SINGLE),

    PageTable.DOUBLE:  PageTree(PageTable.DOUBLE),
    PageTable.ENDLESS: PageTree(PageTable.ENDLESS),
    PageTable.SONG:    PageTree(PageTable.SONG),
    PageTable.HELP:    PageTree(PageTable.HELP),
    PageTable.RANK:    PageTree(PageTable.RANK),
    PageTable.EXIT:    PageTree(PageTable.EXIT),
}



#
# 建立父子關係
#

# 主選單加入子頁
tree_path_table[PageTable.MENU].add_child(tree_path_table[PageTable.SINGLE_MENU])
tree_path_table[PageTable.MENU].add_child(tree_path_table[PageTable.DOUBLE])
tree_path_table[PageTable.MENU].add_child(tree_path_table[PageTable.ENDLESS])
tree_path_table[PageTable.MENU].add_child(tree_path_table[PageTable.SONG])
tree_path_table[PageTable.MENU].add_child(tree_path_table[PageTable.HELP])
tree_path_table[PageTable.MENU].add_child(tree_path_table[PageTable.RANK])
tree_path_table[PageTable.MENU].add_child(tree_path_table[PageTable.EXIT])

tree_path_table[PageTable.SINGLE_MENU].add_child(tree_path_table[PageTable.SINGLE])

#
# 執行生成所有父子索引對照表 (hook_y)
#
tree_path_table[PageTable.MENU].update_catalog_recursive()



#
# 建立 genealogy_table 整棵樹分之dict
# Stack 使用
#
def build_genealogy_table(node, genealogy = None):
    if genealogy is None:
        genealogy = {}
    if node.children:
        genealogy[node.name] = node.family_table
        for child in node.children:
            build_genealogy_table(child, genealogy)
    return genealogy

genealogy_table = build_genealogy_table(tree_path_table[PageTable.MENU])


import pprint

# 確認祖譜樣貌 高級print
pprint.pprint(genealogy_table)
