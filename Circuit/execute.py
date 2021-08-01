from Circuit.circuit import Circuit
import pickle


def inter(root):
    if root:
        if isinstance(root, str):
            return
        else:
            # print(root.gate.gate_type, ":", root.gate.left_wire.get_keys(), root.gate.right_wire.get_keys(),
            #       root.gate.output_wire.get_keys())
            # root.gate.show()
            inter(root.left_gate)
            inter(root.right_gate)


def execute():
    with open('..\\myCircuit.txt', 'rb') as cFile:
        c = pickle.load(cFile)
    c.show_circuit()
    # inter(c.root)
    # print(c.input_labels)
    input_labels = c.input_labels
    kA = input_labels['A'][1]
    kB = input_labels['B'][1]
    kC = input_labels['C'][1]
    inputs = {'A': kA, 'B': kB, 'C': kC}
    result = c.execute(inputs)
    print("________________")
    print("output:", result)
    print("________________")


execute()
