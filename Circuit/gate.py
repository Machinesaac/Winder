from Circuit.wire import Wire
from cryptography.fernet import Fernet, InvalidToken
import base64
from random import shuffle

gates_type = {
    'AND': lambda x, y: x & y,
    'XOR': lambda x, y: x ^ y,
    'OR': lambda x, y: x | y
}


# 规定左为garbler输入，右为executor输入
class Gate:
    def __init__(self, gate_type, create_left=True, create_right=True, gid=None):
        self.gid = gid  # 门在电路中的唯一id
        self.table = []  # 门的混淆表
        self.gate_type = gate_type  # 门的类型
        self.left_wire = Wire() if create_left else None  # 门的左输入线实例
        self.right_wire = Wire() if create_right else None  # 门的右输入线实例
        self.output_wire = Wire()  # 门的输出线实例
        self.output_table = {self.output_wire.true_key: 1, self.output_wire.false_key: 0}

    def execute(self, left_value, right_value):
        output_value = gates_type[self.gate_type](left_value, right_value)
        output_label = self.output_wire.true_key if output_value == 1 else 0
        return output_label

    def garble(self):
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

    def degarble(self, key1, key2):
        output_label = "something wrong!"
        key1 = Fernet(base64.urlsafe_b64encode(key1))
        key2 = Fernet(base64.urlsafe_b64encode(key2))

        for table_entry in self.table:
            try:
                output_label = key2.decrypt(key1.decrypt(table_entry))
            except InvalidToken:
                # 不是当前entry，继续尝试
                pass

        return output_label

    # 用来在生成混淆表后，清除门实例除混淆表以外的所有内容，以构造混淆电路
    def clear(self):
        self.left_wire = None
        self.right_wire = None  # 门的右输入线实例
        self.output_wire = None  # 门的输出线实例
        self.output_table = None

    def show(self):
        print("Left_wire: true_key:{}, false_key:{}".format(self.left_wire.true_key if self.left_wire else None, self.left_wire.false_key if self.left_wire else None))
        print("Right_wire: true_key:{}, false_key:{}".format(self.right_wire.true_key if self.right_wire else None, self.right_wire.false_key if self.right_wire else None))
        print("garble table: {}".format(self.table))


"""
gate = Gate('AND')
k1 = gate.left_wire.true_key
k2 = gate.right_wire.true_key
gate.garble()
gate.test()
key3 = gate.degarble(k1, k2)
print(gate.output_table[key3])
"""
