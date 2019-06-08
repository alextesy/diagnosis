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


def get_diagnose(system, observation, observation_priors, gate_prior):
    diagnoses = []

    output_ids = list(observation[1].keys())
    for i in range(2 ** len(output_ids)):
        values_string = ('{0:0' + str(len(output_ids)) + 'b}').format(i)

        obs = (observation[0], {})

        for v_i, v in enumerate(values_string):
            obs[1][output_ids[v_i]] = int(v)

        obs_p = 1.0
        for o in output_ids:
            if obs[1][o] == observation[1][o]:
                obs_p *= observation_priors[o]
            else:
                obs_p *= 1 - observation_priors[o]

        observation_diagnoses = get_observation_diagnoses(system, obs, gate_prior)
        observation_diagnoses = [(t[0], t[1] * obs_p) for t in observation_diagnoses]

        diagnoses.extend(observation_diagnoses)

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
