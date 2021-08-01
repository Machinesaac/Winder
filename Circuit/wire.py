import os
import Circuit.settings as settings


class Wire:
    def __init__(self, wid=None):
        self.id = wid  # 电路中每条线的唯一id
        self.true_key = os.urandom(settings.MAX_BIT)  # 代表逻辑值真的标签
        self.false_key = os.urandom(settings.MAX_BIT)  # 代表逻辑值假的标签
        self.keys = (self.true_key, self.false_key)

    def get_label_by_value(self, value):
        return self.true_key if value == 1 else self.false_key

    def get_keys(self):
        return self.false_key, self.true_key
