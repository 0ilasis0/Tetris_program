# info.filename → 呼叫程式所在檔案名稱
# info.lineno → 呼叫程式的行號
# info.function → 呼叫函式名稱
# info.code_context → 呼叫程式的原始程式碼

import datetime
import inspect
import os


class Debug:
    def __init__(self, enable=True):
        self.enable = enable   # 可以隨時關閉/開啟 debug 輸出

    def _get_frameinfo(self, frame=None):
        """取得呼叫來源資訊"""
        if frame is None:
            frame = inspect.currentframe().f_back
        info = inspect.getframeinfo(frame)
        filename = os.path.basename(info.filename)  # 只取檔名
        return info, filename

    def log(self, *args, caller_frame=None):
        """一般 debug 訊息 (綠色)"""
        if not self.enable:
            return
        info, filename = self._get_frameinfo(caller_frame or inspect.currentframe().f_back)
        time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\033[92m[DEBUG {time} {filename}:{info.lineno} {info.function}()]\033[0m", *args)

    def var(self, **kwargs):
        """印出變數名稱與值 (藍色)"""
        if self.enable:
            frame = inspect.currentframe().f_back
            info, filename = self._get_frameinfo(frame)
            time = datetime.datetime.now().strftime("%H:%M:%S")
            for k, v in kwargs.items():
                print(f"\033[94m[VAR {time} {filename}:{info.lineno} {info.function}()]\033[0m {k} = {v}")

    def error(self, *args):
        """紅色錯誤訊息"""
        if self.enable:
            info, filename = self._get_frameinfo(inspect.currentframe().f_back)
            time = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"\033[91m[ERROR {time} {filename}:{info.lineno} {info.function}()]\033[0m", *args)

    def toggle(self):
        """切換 debug 狀態"""
        self.enable = not self.enable

dbg = Debug()
