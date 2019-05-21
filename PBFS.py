import random


def is_superset(gate_set, diagnoses):
    for diagnose in diagnoses:
        if diagnose[0].issubset(gate_set):
            return True
    return False


def add_neighbors(queue, gate_set, gates):
    """
    returns the new queue the the new candidates.
    Args:
        queue(list): the old queue
        gate_set(set): the current gate set to get its neighbors
        gates(list): the system gates
    """
    # the gate set neighbors
    candidates = [gate_set.union({g}) for g in gates if g not in gate_set]
    # remove the ones that are already in the queue
    candidates = [c for c in candidates if c not in queue]
    return candidates + queue


def get_diagnose(system, observation, gate_prior, observation_prior, full):
    observation_inputs = observation[0]
    observation_outputs = observation[1]

    gates = [g.id for g in system.gates]
    diagnoses = []
    queue = add_neighbors([], set(), gates)

    while len(queue) > 0:
        gate_set = queue.pop()

        if (not full) and is_superset(gate_set, diagnoses):
            continue

        outputs = system.run(input_values=observation_inputs, invalid_gates=gate_set)

        dp = gate_prior ** len(gate_set)
        for o, v in outputs.items():
            if v == observation_outputs[o]:
                dp *= observation_prior
            else:
                dp *= (1 - observation_prior)

        if dp > 0:
            diagnoses.append((gate_set, dp))

        queue = add_neighbors(queue, gate_set, gates)

    print(len(diagnoses))
    return diagnoses
