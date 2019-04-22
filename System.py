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

    def run(self, input_values):
        gates = self.gates
        values_dict = {}
        for i in range(len(gates)):
            current_gate = gates[i]
            try:
                inputs = [input_values[i] for i in current_gate.inputs]
                output, prior = current_gate.activate(inputs)
                values_dict[current_gate.output] = (int(output), 1 - prior)
            except KeyError:
                break
        for j in range(i, len(gates)):
            current_gate = gates[j]
            input_list = []
            for input in current_gate.inputs:
                if 'i' in input:
                    input_list.append((input_values[input], 1.0))
                else:
                    input_list.append(values_dict[input])
            all_input_options = [[[], 1.0]]
            for inp in input_list:
                options_size = len(all_input_options)
                for option_index in range(options_size):
                    option = all_input_options[option_index]
                    if inp[1] != 1:
                        all_input_options.append(copy.deepcopy(option))
                    option[0].append(inp[0])
                    option[1] *= inp[1]
                    if inp[1] != 1:
                        all_input_options[-1][0].append(1.0 - inp[0])
                        all_input_options[-1][1] *= (1.0 - inp[1])
            prob = 0
            for option in all_input_options:
                output, prior = current_gate.activate(option[0])
                if output:
                    prob += (1 - prior) * option[1]
                else:
                    prob += prior * option[1]
            values_dict[current_gate.output] = (1.0, prob)
        for k, v in values_dict.items():
            if 'o' in k:
                print(f'Output {k} with probability: {v}')

