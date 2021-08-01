from Circuit.generator import Generator
from Circuit.executor import Executor

def test_1():
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
    g = Generator(C, ['A', 'B'], ['C'])
    g.generate()
    input_labels = g.get_input_labels()
    kA = input_labels['A'][1]
    kB = input_labels['B'][1]
    kC = input_labels['C'][1]
    inputs = {'A': kA, 'B': kB, 'C': kC}

    e = Executor(inputs, '..\\myCircuit.txt')
    result = e.execute()

    print("________________")
    print("output:", result)
    print("________________")


test_1()
