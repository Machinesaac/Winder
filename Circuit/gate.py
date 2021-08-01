from Circuit.wire import Wire
from cryptography.fernet import Fernet, InvalidToken
import base64
from random import shuffle

# 定义门的逻辑值计算
gates_type = {
    'AND': lambda x, y: x & y,
    'XOR': lambda x, y: x ^ y,
    'OR': lambda x, y: x | y
}


# 规定左输入线为garbler输入，右输入线为executor输入

class Gate:
    """
    混淆电路中的门类
    """
    def __init__(self, gate_type, create_left=True, create_right=True, gid=None):
        """

        :param gate_type: 门的类型：'AND' or 'XOR or 'OR'
        :param create_left: 是否创建左输入线
        :param create_right: 是否创建右输入线
        :param gid: 门在电路中的唯一id
        """
        self.gid = gid  # 门在电路中的唯一id
        self.table = []  # 门的混淆表
        self.gate_type = gate_type  # 门的类型
        self.left_wire = Wire() if create_left else None  # 门的左输入线实例
        self.right_wire = Wire() if create_right else None  # 门的右输入线实例
        self.output_wire = Wire()  # 门的输出线实例
        self.output_table = {self.output_wire.true_key: 1, self.output_wire.false_key: 0}  # 门的输出表

    def execute(self, left_value, right_value):
        """
        根据逻辑值输入计算门的加密输出
        :param left_value: 左输入线的逻辑值
        :param right_value: 右输入线的逻辑值
        :return: 门输出的加密值
        """
        output_value = gates_type[self.gate_type](left_value, right_value)
        output_label = self.output_wire.true_key if output_value == 1 else 0

        return output_label

    def garble(self):
        """
        当前门实例进行加密混淆，将混淆表存在self.table
        :return: 1
        """
        g = gates_type[self.gate_type]

        # 0 0
        activate_value = g(0, 0)  # 门输出导线值
        activate_label = self.output_wire.get_label_by_value(activate_value)  # 门输出激活值
        key1 = Fernet(base64.urlsafe_b64encode(self.left_wire.false_key))  # 左输入导线的加密实例
        key2 = Fernet(base64.urlsafe_b64encode(self.right_wire.false_key))  # 右输入导线的加密实例
        self.table.append(key1.encrypt(key2.encrypt(activate_label)))  # 将混淆值添入混淆表

        # 0 1
        activate_value = g(0, 1)  # 门输出导线值
        activate_label = self.output_wire.get_label_by_value(activate_value)  # 门输出激活值
        key1 = Fernet(base64.urlsafe_b64encode(self.left_wire.false_key))  # 左输入导线的加密实例
        key2 = Fernet(base64.urlsafe_b64encode(self.right_wire.true_key))  # 右输入导线的加密实例
        self.table.append(key1.encrypt(key2.encrypt(activate_label)))  # 将混淆值添入混淆表

        # 1 0
        activate_value = g(1, 0)  # 门输出导线值
        activate_label = self.output_wire.get_label_by_value(activate_value)  # 门输出激活值
        key1 = Fernet(base64.urlsafe_b64encode(self.left_wire.true_key))  # 左输入导线的加密实例
        key2 = Fernet(base64.urlsafe_b64encode(self.right_wire.false_key))  # 右输入导线的加密实例
        self.table.append(key1.encrypt(key2.encrypt(activate_label)))  # 将混淆值添入混淆表

        # 1 1
        activate_value = g(1, 1)  # 门输出导线值
        activate_label = self.output_wire.get_label_by_value(activate_value)  # 门输出激活值
        key1 = Fernet(base64.urlsafe_b64encode(self.left_wire.true_key))  # 左输入导线的加密实例
        key2 = Fernet(base64.urlsafe_b64encode(self.right_wire.true_key))  # 右输入导线的加密实例
        self.table.append(key1.encrypt(key2.encrypt(activate_label)))  # 将混淆值添入混淆表

        shuffle(self.table)  # 打乱混淆表 注意，这里是不符合密码学安全的！！！

        return 1

    def degarble(self, left_key, right_key):
        """
        根据输入标签解密门的输出标签
        :param left_key: 左输入线的标签
        :param right_key: 右输入线的标签
        :return: 门的输出标签
        """
        output_label = None
        key1 = Fernet(base64.urlsafe_b64encode(left_key))
        key2 = Fernet(base64.urlsafe_b64encode(right_key))

        # 遍历当前门实例的混淆表，尝试解密出输出标签
        for table_entry in self.table:
            try:
                output_label = key2.decrypt(key1.decrypt(table_entry))

            except InvalidToken:
                # 不是当前entry，继续尝试
                pass

        return output_label

    def clear_gate(self):
        """
        在生成混淆表后，清除门实例除混淆表以外的所有内容，以构造混淆电路
        :return: 1
        """
        self.left_wire = None
        self.right_wire = None
        self.output_wire = None
        self.output_table = None

        return 1

    def show_gate(self):
        """
        输出当前门实例的信息
        :return: 1
        """
        print("Left_wire: true_key:{}, false_key:{}".format(self.left_wire.true_key if self.left_wire else None, self.left_wire.false_key if self.left_wire else None))
        print("Right_wire: true_key:{}, false_key:{}".format(self.right_wire.true_key if self.right_wire else None, self.right_wire.false_key if self.right_wire else None))
        print("garble table: {}".format(self.table))

        return 1