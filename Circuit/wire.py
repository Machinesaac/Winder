import os
import Circuit.settings as settings


class Wire:
    """
    电路中的线路实例
    """
    def __init__(self, wid=None):
        """
        :param wid: 电路中每条线的唯一id
        """
        self.id = wid
        self.true_key = os.urandom(settings.MAX_BIT)  # 代表逻辑值真的标签
        self.false_key = os.urandom(settings.MAX_BIT)  # 代表逻辑值假的标签
        self.keys = (self.true_key, self.false_key)

    def get_label_by_value(self, value):
        """
        通过逻辑值获得对应的标签
        :param value: 逻辑值
        :return: 对应标签
        """
        return self.true_key if value == 1 else self.false_key

    def get_keys(self):
        """
        返回电路标签组: (false_key, true_key)
        :return: 电路标签组: (false_key, true_key)
        """
        return self.false_key, self.true_key
