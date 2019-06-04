import random
from collections import defaultdict


def is_superset(gate_set, diagnoses):
    for diagnose in diagnoses:
        if set(diagnose[0]).issubset(set(gate_set)):
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


def get_diagnose(system, observations, gate_prior, observation_p=0.25):
    diagnoses = []
    for observation in observations:
        observation_priors = {o: 1.0 - random.random() * observation_p for o in observation[1].keys()}
        observation_diagnoses = get_observation_diagnoses(system, observation, gate_prior)

        if len(diagnoses) == 0:
            new_diagnoses = observation_diagnoses
        else:
            new_diagnoses = defaultdict(int)
            for o_d, o_p in observation_diagnoses:
                for d, p in diagnoses:
                    union = tuple(sorted(o_d.union(d)))
                    new_diagnoses[union] += o_p * p
            new_diagnoses = new_diagnoses.items()

        new_diagnoses_list = sorted(new_diagnoses, key=lambda item: len(item[0]))
        diagnoses = [(t[0], t[1]) for i, t in enumerate(new_diagnoses_list) if not is_superset(t[0], new_diagnoses_list[:i])]

    return diagnoses


def get_observation_diagnoses(system, observation, gate_prior):
    observation_inputs = observation[0]
    observation_outputs = observation[1]

    gates = [g.id for g in system.gates]
    diagnoses = []
    queue = add_neighbors([], set(), gates)

    while len(queue) > 0:
        gate_set = queue.pop()

        if is_superset(gate_set, diagnoses):
            continue

        outputs = system.run(input_values=observation_inputs, invalid_gates=gate_set)

        dp = gate_prior ** len(gate_set)
        for o, v in outputs.items():
            if v != observation_outputs[o]:
                dp = 0
                break

        if dp > 0:
            diagnoses.append((gate_set, dp))

        queue = add_neighbors(queue, gate_set, gates)

    return diagnoses
