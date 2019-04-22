import copy

from System import System
from Gate import Gate
from observation_parse import read_observation


def system_activate(system, input_values, output_values):
    gates = system.gates
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

