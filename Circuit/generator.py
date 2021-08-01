from Circuit.circuit import Circuit
import pickle

class Generator:
    def __init__(self, circuit, garbler_inputs=None, evaluator_inputs=None):
        self.circuit = circuit
        self.garbler_inputs = garbler_inputs
        self.evaluator_inputs = evaluator_inputs
        self.gc = None
    def generate(self):
        """
        生成混淆电路，保存至myCircuit.txt文件
        :return: 1
        """
        c = Circuit(self.circuit)
        c.generate()
        self.gc = c
        with open('..\\myCircuit.txt', 'wb') as cFile:
            pickle.dump(c, cFile)

        return 1

    def get_input_labels(self):

        return self.gc.input_labels