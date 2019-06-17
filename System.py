import copy
from collections import defaultdict
from string import digits
import networkx
import pylab

from Gate import Gate


class System(object):
    def __init__(self, system_id, inputs, outputs, gates):
        self.id = system_id
        self.inputs = inputs
        self.outputs = outputs
        self.gates = gates
        self.dependencies = self._find_dependencies()

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

    def run(self, input_values, invalid_gates=set()):
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

    def draw(self):
        # Build a graph
        G = networkx.DiGraph()

        component = set()

        for g in self.gates:
            G.add_node(g.id, s="s")

            for c in g.inputs:
                if c not in component:
                    component.add(c)
                    G.add_node(c, s="o")
                G.add_edge(c, g.id)

            if g.output not in component:
                component.add(g.output)
                G.add_node(g.output, s="o")
            G.add_edge(g.id, g.output)

        # Drawing the graph
        # First obtain the node positions using one of the layouts
        nodes_pos = networkx.layout.kamada_kawai_layout(G)

        # Get all distinct node classes according to the node shape attribute
        nodes_shapes = set((n_shape[1]["s"] for n_shape in G.nodes(data=True)))

        # For each node class filter and draw the subset of nodes with the same symbol
        for n_shape in nodes_shapes:
            networkx.draw_networkx_nodes(G, nodes_pos, node_color='b', node_size=100, node_shape=n_shape,
                                         nodelist=[s_node[0] for s_node in filter(
                                             lambda x: x[1]["s"] == n_shape, G.nodes(data=True))], with_labels=True)

        # Finally, draw the edges between the nodes
        networkx.draw_networkx_edges(G, nodes_pos, arrowsize=10)
        networkx.draw_networkx_labels(G, nodes_pos, font_color='w', font_size=3)

        # And show the final result
        pylab.axis('off')
        pylab.show()

    def _find_dependencies(self):
        gate_dependencies = defaultdict(list)  # gates
        dependencies = defaultdict(list)  # i,z
        for g in self.gates[::-1]:
            if 'o' in g.output:
                gate_dependencies[g.output].append(g.id)
                dependencies[g.output].extend(g.inputs)
            else:
                for output in self.outputs:
                    if g.output in dependencies[output]:
                        gate_dependencies[output].append(g.id)
                        dependencies[output].extend(g.inputs)
        return gate_dependencies


