from Circuit.gate import Gate
from anytree import Node, RenderTree
import pickle
from copy import copy

class CNode:
    """
    电路执行树的节点类
    """
    def __init__(self, gate=None, left_gate=None, right_gate=None, parent=None):
        """
        :param gate: 此节点所代表的门（class Gate）实例
        :param left_gate:  左子节点
        :param right_gate:  右子节点
        :param parent: 父节点，若为None则为根节点，代表输出门
        """
        self.gate = gate
        self.left_gate = left_gate
        self.right_gate = right_gate
        self.parent = parent


class Circuit:
    """
    混淆电路类
    """
    def __init__(self, c, garbler_inputs=None, evaluator_inputs=None):
        """
        :param c: dict，电路构造的Json表示
        :param garbler_inputs: list，电路生成者的输入线符号
        :param evaluator_inputs: list，电路执行者的输入线符号
        """
        self.garbler_inputs = garbler_inputs
        self.evaluator_inputs = evaluator_inputs
        self.c = c
        self.root = None  # 电路执行树的根节点
        self.input_labels = {}  # 电路的输入标签
        self.output_table = {}   # 电路的输出表：{label：value}

    def generate(self):
        """
        1.建立电路执行树，将根节点保存至self.root
        2.生成电路输出表，保存至self.output_table
        3.清理混淆电路实例，实例中仅保留每个门的混淆表与电路的输出表
        
        :return: 1
        """
        self.root = self.build_tree(self.c, None)
        self.output_table = self.root.gate.output_table
        self.clear()
        return 1

    def build_tree(self, c, parent):
        """
        递归建立电路执行树
        :param c: 子电路节点
        :param parent: 父电路节点
        :return: 当前节点
        """
        left_c = c['left']
        right_c = c['right']
        gate_type = c['type']
        create_left = True
        create_right = True
        cnode = CNode(parent=parent)

        if isinstance(left_c, dict):
            left_gate = self.build_tree(left_c, cnode)
            create_left = False
        else:
            left_gate = left_c

        if isinstance(right_c, dict) or (right_c in self.input_labels):
            right_gate = self.build_tree(right_c, cnode)
            create_right = False
        else:
            right_gate = right_c

        gate = Gate(gate_type, create_left, create_right)

        if not create_left:
            gate.left_wire = copy(left_gate.gate.output_wire)
        else:
            if left_c in self.input_labels:
                gate.left_wire.false_key = self.input_labels[left_c][0]
                gate.left_wire.true_key = self.input_labels[left_c][1]
            else:
                self.input_labels[left_gate] = (gate.left_wire.false_key, gate.left_wire.true_key)

        if not create_right:
            gate.right_wire = copy(right_gate.gate.output_wire)
        else:
            if right_c in self.input_labels:
                gate.right_wire.false_key = self.input_labels[right_c][0]
                gate.right_wire.true_key = self.input_labels[right_c][1]
            else:
                self.input_labels[right_gate] = (gate.right_wire.false_key, gate.right_wire.true_key)

        gate.garble()  # 混淆门
        is_output_gate = 1 if parent == None else 0
        # gate.clear(is_output_gate)
        cnode.gate = gate
        cnode.left_gate = left_gate
        cnode.right_gate = right_gate

        return cnode

    def execute(self, inputs):
        """
        电路执行方法
        :param inputs: dict，电路输入：{wire sign：label}
        :return: 电路输出：0 or 1
        """
        def iterate(inputs, cnode):
            if cnode:
                if isinstance(cnode, str):
                    return inputs[cnode]
                else:
                    key1 = iterate(inputs, cnode.left_gate)
                    key2 = iterate(inputs, cnode.right_gate)
                    # print("k1:", key1, "k2", key2)

                    return cnode.gate.degarble(key1, key2)

        output_label = iterate(inputs, self.root)
        output_gate = self.root.gate

        return self.output_table[output_label]

    def clear(self):
        """
        清理混淆电路实例，使实例中仅保留每个门的混淆表与电路的输出表
        :return: 1
        """
        def iterate(cnode):
            if cnode:
                if isinstance(cnode, str):
                    return
                else:
                    cnode.gate.clear_gate()
                    iterate(cnode.left_gate)
                    iterate(cnode.right_gate)
                    return

        iterate(self.root)

        return 1

    def show_circuit(self):
        """
        展示电路
        :return: 1
        """
        def iterate(root, parent):
            if root:
                if isinstance(root, str):
                    # print(root)
                    node = Node(root, parent)
                else:
                    # print(root.gate.gate_type)
                    node = Node(root.gate.gate_type, parent)
                    iterate(root.left_gate, node)
                    iterate(root.right_gate, node)

            return node

        root = iterate(self.root, None)
        for pre, fill, node in RenderTree(root):
            print("{}{}".format(pre, node.name))

        return 1

