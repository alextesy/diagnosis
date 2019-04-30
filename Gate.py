import random


class Gate(object):
    def __init__(self, gate_type, gate_id, output, inputs, prior=None): #output, inputs):
        """

        Args:
            gate_type(str): Type of the gate (and, nand, xor ...)
            gate_id(str): ID of the gate
            output(str): output id
            inputs(List[str]): list of inputs ids
            prior(float): a probability fot the gate to fail
        """
        self.type = gate_type
        self.id = gate_id
        self.prior = prior if prior is not None else random.random() * 0.5,
        self.output = output
        self.inputs = inputs

    def activate(self, inputs):
        # Not Implemented here
        pass

    @classmethod
    def create_gate(cls, gate_type):
        gate_map = {
            'and': AND_GATE,
            'or': OR_GATE,
            'xor': XOR_GATE,
            'nand': NAND_GATE,
            'nor': NOR_GATE,
            'inverter': INVERT_GATE,
            'buffer': BUFFER_GATE
        }

        return gate_map[gate_type]


class XOR_GATE(Gate):
    def activate(self, inputs):
        return bool(inputs[0]) != bool(inputs[1])


class AND_GATE(Gate):
    def activate(self, inputs):
        return bool(inputs[0]) and bool(inputs[1])


class OR_GATE(Gate):
    def activate(self, inputs):
        return bool(inputs[0]) or bool(inputs[1])


class NOR_GATE(Gate):
    def activate(self, inputs):
        return not(bool(inputs[0]) or bool(inputs[1]))


class NAND_GATE(Gate):
    def activate(self, inputs):
        return not(bool(inputs[0]) and bool(inputs[1]))


class INVERT_GATE(Gate):
    def activate(self, inputs):
        return not bool(inputs[0])


class BUFFER_GATE(Gate):
    def activate(self, inputs):
        return bool(inputs[0])

