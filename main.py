import json

from System import System
from observation_parse import read_observation
from PBFS import get_diagnose, get_observation_diagnoses
from multiprocessing import Pool
import random
import operator
import time


def _obs_run(observation):
    config_dict = {}
    config_dict['gate_prior'] = random.random() * 0.5
    config_dict['observation_priors'] = {o: 1.0 - random.random() * 0.25 for o in observation[1].keys()}
    start_time = time.time()
    predicted_diagnoses1 = get_diagnose(system_gal, observation, config_dict['observation_priors'],
                                        config_dict['gate_prior'], experiment=False)
    baseline_time = (time.time() - start_time)
    print("--- Baseline %s seconds ---" % baseline_time)
    config_dict['baseline_time'] = baseline_time
    start_time = time.time()
    predicted_diagnoses2 = get_diagnose(system_gal, observation, config_dict['observation_priors'],
                                        config_dict['gate_prior'], experiment=True)
    experiment_time = (time.time() - start_time)
    print("--- GAL %s seconds ---" % experiment_time)

    config_dict['experiment_time'] = experiment_time
    config_dict['predicted_diagnose_baseline'] = predicted_diagnoses1
    config_dict['predicted_diagnose_experiment'] = predicted_diagnoses2

    with open('{}_{}.json'.format(sys_name, observation[-1]), 'w') as f:
        json.dump(config_dict, f)

    print("--- Baseline ---")

    print(sorted(predicted_diagnoses1, key=operator.itemgetter(1))[::-1])

    print("--- GAL ---")

    print(sorted(predicted_diagnoses2, key=operator.itemgetter(1))[::-1])


for sys_name in ['c17', '74182', '74181', '74183']:
    system_gal = System.create_system('data_systems/' + sys_name + '.sys')
    #system_gal.draw()
    observations = read_observation('observations/' + sys_name + '_iscas85.obs')
    print("Started!!")
    with Pool(5) as p:
        p.map(_obs_run, observations[:5])
    p.join()





# print('\n\n\n')
# print(sorted(true_diagnoses, key=operator.itemgetter(1))[::-1])

#outputs = system_gal.run(input_values=observations[0][0])
#for observation in observations:
#    outputs = system_gal.run(input_values=observation[0])

#system_gal.draw()

# for observation in observations:
    #     for o, v in observation[1].items():
    #         if random.random() > (observation_priors[o]):
    #             observation[1][o] = 1 - v
    #
    # observation = observations[0]
    #
    # true_diagnoses = get_observation_diagnoses(system_gal, observation, config_dict['gate_prior'])