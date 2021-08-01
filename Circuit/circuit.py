from Circuit.gate import Gate
from anytree import Node, RenderTree
import pickle
from copy import copy

C = {
    'left': {
        'left': 'A',
        'type': 'AND',
        'right': 'B',
    },
    'type': 'OR',
    'right': {
        'left': 'B',
        'type': 'XOR',
        'right': 'C'
    }
}


class CNode:
    def __init__(self, gate=None, left_gate=None, right_gate=None, parent=None):
        self.gate = gate
        self.left_gate = left_gate
        self.right_gate = right_gate
        self.parent = parent


class Circuit:
    def __init__(self, c, garbler_inputs, evaluator_inputs):
        self.garbler_inputs = garbler_inputs  # p1的输入
        self.evaluator_inputs = evaluator_inputs  # p2的输入
        self.c = c  # 电路构造Json表示
        self.root = None
        self.gid = 0
        self.input_labels = {}
        self.output_table = {}

    def generate(self):
        self.root = self.build_tree(self.c, None)
        self.output_table = self.root.gate.output_table
        self.clear()
        return self.root

    def build_tree(self, c, parent):
        # 此处的c为子电路
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

        gate = Gate(gate_type, create_left, create_right, self.gid)
        self.gid += 1

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
        output_label = self._iteration(inputs, self.root)
        output_gate = self.root.gate
        return self.output_table[output_label]

    def clear(self):
        def iterate(cnode):
            if cnode:
                if isinstance(cnode, str):
                    return
                else:
                    cnode.gate.clear()
                    iterate(cnode.left_gate)
                    iterate(cnode.right_gate)
                    return
        iterate(self.root)

        return

    def _iteration(self, inputs, cnode):
        if cnode:
            if isinstance(cnode, str):
                # rint(cnode)
                return inputs[cnode]
            else:
                key1 = self._iteration(inputs, cnode.left_gate)
                key2 = self._iteration(inputs, cnode.right_gate)
                # print("k1:", key1, "k2", key2)

                return cnode.gate.degarble(key1, key2)

    # 以下为辅助函数
    def _inter(self, root, parent):
        if root:
            if isinstance(root, str):
                # print(root)
                node = Node(root, parent)
            else:
                # print(root.gate.gate_type)
                node = Node(root.gate.gate_type, parent)
                self._inter(root.left_gate, node)
                self._inter(root.right_gate, node)

        return node

    def show_circuit(self):
        root = self._inter(self.root, None)
        for pre, fill, node in RenderTree(root):
            print("{}{}".format(pre, node.name))


"""
def inter(root):
    if root:
        if isinstance(root, str):
            print(root)
        else:
            print(root.gate.gate_type)
            inter(root.left_gate)
            inter(root.right_gate)
"""


def test():
    c = Circuit(C, ['A', 'B'], ['C'])
    c.generate()
    with open('..\\myCircuit.txt', 'wb') as cFile:
        pickle.dump(c, cFile)
    # c.show_circuit()
    # c.execute()

test()
