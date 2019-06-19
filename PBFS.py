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


def get_diagnose(system, observation, observation_priors, gate_prior, experiment=False):
    diagnoses = []
    obs_diagnoses = {}

    output_ids = list(system.outputs)
    for i in range(2 ** len(output_ids)):
        values_string = ('{0:0' + str(len(output_ids)) + 'b}').format(i)

        print(system.id, observation[-1], 'starts observation', values_string)

        obs = (observation[0], {})

        for v_i, v in enumerate(values_string):
            obs[1][output_ids[v_i]] = int(v)

        obs_p = 1.0
        for o in output_ids:
            if obs[1][o] == observation[1][o]:
                obs_p *= observation_priors[o]
            else:
                obs_p *= 1 - observation_priors[o]

        if experiment:
            gs = []
            for v_i, v in enumerate(values_string):
                old_value_string = values_string[:v_i] + str(1 - int(v)) + values_string[v_i + 1:]
                if old_value_string in obs_diagnoses:
                    gs += [g for g in obs_diagnoses[old_value_string] if g not in gs]
                    gs += [g for g in system.dependencies.get(output_ids[v_i], []) if g not in gs]
                    breakg
                if len(gs) == len(system.gates):
                    break

            observation_diagnoses = get_observation_diagnoses(system, obs, gate_prior, gs, True)
            obs_diagnoses[values_string] = set([g for t in observation_diagnoses for g in t[0]])
        else:
            observation_diagnoses = get_observation_diagnoses(system, obs, gate_prior)

        observation_diagnoses = [(list(t[0]), t[1] * obs_p) for t in observation_diagnoses]
        diagnoses.extend(observation_diagnoses)
        print(system.id, observation[-1], 'done observation', values_string)

    return diagnoses


def get_observation_diagnoses(system, observation, gate_prior, gs=[], experiment=False):
    observation_inputs = observation[0]
    observation_outputs = observation[1]

    if experiment:
        gates = gs
        gates += [g.id for g in system.gates if g.id not in gates]
    else:
        gates = [g.id for g in system.gates]

    diagnoses = []

    outputs = system.run(input_values=observation_inputs)

    sys_ok = True
    for o, v in outputs.items():
        if v != observation_outputs[o]:
            sys_ok = False
            break
    if sys_ok:
        return diagnoses

    queue = add_neighbors([], set(), gates)
    while len(queue) > 0:
        gate_set = queue.pop()
        if len(diagnoses) > 0 and len(gate_set) > len(diagnoses[0][0]):
            break

        if is_superset(gate_set, diagnoses):
            continue

        outputs = system.run(input_values=observation_inputs, invalid_gates=gate_set)

        dp = gate_prior ** len(gate_set)
        for o, v in outputs.items():
            if v != observation_outputs[o]:
                dp = 0
                break

        if dp > 0:
            # print('Diagnose found', gate_set)
            diagnoses.append((gate_set, dp))
            break

        queue = add_neighbors(queue, gate_set, gates)

    return diagnoses
