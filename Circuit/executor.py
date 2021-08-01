from Circuit.circuit import Circuit
import pickle

class Executor:
    def __init__(self, inputs, file_path):
        """
        :param inputs: 电路输入
        :param file_path: 电路的文件路径
        """
        self.inputs = inputs
        self.file_path = file_path

    def execute(self):
        """
        执行电路，返回结果逻辑值
        :return: 结果逻辑值
        """
        with open(self.file_path, 'rb') as cFile:
            c = pickle.load(cFile)
            c.show_circuit()
            result = c.execute(self.inputs)

        return result