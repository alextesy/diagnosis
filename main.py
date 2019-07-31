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

    start_time = time.time()
    predicted_diagnoses2 = get_diagnose(system_gal, observation, config_dict['observation_priors'],
                                        config_dict['gate_prior'], experiment=True, use_dependencies=True)
    experiment_dependencies_time = (time.time() - start_time)

    start_time = time.time()
    predicted_diagnoses3 = get_diagnose(system_gal, observation, config_dict['observation_priors'],
                                        config_dict['gate_prior'], experiment=True, use_previous=True)
    experiment_previous_time = (time.time() - start_time)

    start_time = time.time()
    predicted_diagnoses4 = get_diagnose(system_gal, observation, config_dict['observation_priors'],
                                        config_dict['gate_prior'], experiment=True, use_previous=True,
                                        use_dependencies=True)
    experiment_all_time = (time.time() - start_time)

    print("--- Baseline %s seconds ---" % baseline_time)
    print("--- experiment_previous %s seconds ---" % experiment_previous_time)
    print("--- experiment_dependencies %s seconds ---" % experiment_dependencies_time)
    print("--- experiment_all %s seconds ---" % experiment_all_time)

    config_dict['baseline_time'] = baseline_time
    config_dict['experiment_dependencies_time'] = experiment_dependencies_time
    config_dict['experiment_previous_time'] = experiment_previous_time
    config_dict['experiment_all_time'] = experiment_all_time

    config_dict['predicted_diagnose_baseline'] = predicted_diagnoses1
    config_dict['predicted_diagnose_experiment_dependencies'] = predicted_diagnoses2
    config_dict['predicted_diagnose_experiment_previous'] = predicted_diagnoses3
    config_dict['predicted_diagnose_experiment_all'] = predicted_diagnoses4

    with open('results/randoming_gates/{}_{}.json'.format(sys_name, observation[-1]), 'w') as f:
        json.dump(config_dict, f)


for sys_name in ['c17', '74182', '74283', '74181']:
    system_gal = System.create_system('data_systems/' + sys_name + '.sys')
    #system_gal.draw()
    observations = read_observation('observations/' + sys_name + '_iscas85.obs')

    # _obs_run(observations[5])

    for i in range(0, len(observations), 10):
        print("Started!!")
        observations_to_run = observations[i:i+10]

        with Pool(len(observations_to_run)) as p:
            p.map(_obs_run, observations_to_run)
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
