import copy
from string import digits

from Gate import Gate


class System(object):
    def __init__(self, system_id, inputs, outputs, gates):
        self.id = system_id
        self.inputs = inputs
        self.outputs = outputs
        self.gates = gates
        #self.map = system_map

    @classmethod
    def create_system(cls, path):
        with open(path, 'r') as f:
            system_str = f.read().split('.\n')
        system_id, system_inputs, system_outputs, gates = System.parse_system(system_str)
        #system_map = {tuple(gate.inputs): gate for id_gate, gate in gates.items()}
        return System(system_id, system_inputs, system_outputs, gates)

    @staticmethod
    def parse_system(system_list):
        inputs = system_list[1].replace('[', '').replace('\n', '').replace(']', '').split(',')
        outputs = system_list[2].replace('[', '').replace('\n', '').replace(']', '').split(',')
        gates = System.create_gates(system_list[3])
        return system_list[0], inputs, outputs, gates

    @staticmethod
    def create_gates(gates_str):
        gate_list = gates_str.split('],\n')
        parsed_gates = []
        for gate in gate_list:
            # Parsing gate
            gate_list = gate.replace('[', '').replace(']', '').split(',')
            # Parsing gate type
            remove_digits = str.maketrans('', '', digits)
            gate_type = gate_list[0].translate(remove_digits)
            # Create gate object
            Gate_Constructor = Gate.create_gate(gate_type)
            gate = Gate_Constructor(gate_type, gate_list[1], gate_list[2], gate_list[3:])
            parsed_gates.append(gate)
        return parsed_gates

    def run(self, input_values, invalid_gates=set):
        gates = self.gates
        values_dict = input_values
        for i in range(len(gates)):
            current_gate = gates[i]
            inputs = [values_dict[i] for i in current_gate.inputs]
            output = current_gate.activate(inputs)
            if current_gate.id in invalid_gates:
                output = 1 - int(output)
            values_dict[current_gate.output] = int(output)
        return {o: values_dict[o] for o in self.outputs}

