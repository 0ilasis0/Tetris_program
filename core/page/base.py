class PageManager:
    def __init__(self):
        self.history_stack = None

        self.page_map = {}
        self.keymaps = {}
        self.current_page = None
        self.current_boot = None
        self.callbacks = {}

    def set (self, stack, keymaps, page_map, current_page):
        self.history_stack = stack

        self.page_map       = page_map
        self.keymaps        = keymaps
        self.current_page   = current_page

    def boot_page(self, page_name):
        '''偵測是否需要載入初始畫面'''
        if page_name in self.callbacks:
            self.callbacks[page_name]()

    def register_init_fcn(self, page_name, fcn):
        """註冊頁面初始化函式"""
        self.callbacks[page_name] = fcn

page_mg = PageManager()
