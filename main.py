from System import System
from observation_parse import read_observation
from PBFS import get_diagnose, get_observation_diagnoses
import random
import operator
import time


gate_prior = random.random() * 0.5

system_gal = System.create_system(r'data_systems\c432.sys')
#system_gal.draw()
observations = read_observation(r'observations\c432_iscas85.obs')

observation = observations[0]
observation_priors = {o: 1.0 - random.random() * 0.25 for o in observation[1].keys()}
start_time = time.time()
predicted_diagnoses1 = get_diagnose(system_gal, observation, observation_priors, gate_prior, experiment=False)
print("--- Baseline %s seconds ---" % (time.time() - start_time))
start_time = time.time()
predicted_diagnoses2 = get_diagnose(system_gal, observation, observation_priors, gate_prior, experiment=True)
print("--- GAL %s seconds ---" % (time.time() - start_time))

# for observation in observations:
#     for o, v in observation[1].items():
#         if random.random() > (observation_priors[o]):
#             observation[1][o] = 1 - v
#
# observation = observations[0]
#
# true_diagnoses = get_observation_diagnoses(system_gal, observation, gate_prior)
print("--- Baseline ---")

print(sorted(predicted_diagnoses1, key=operator.itemgetter(1))[::-1])

print("--- GAL ---")

print(sorted(predicted_diagnoses2, key=operator.itemgetter(1))[::-1])

# print('\n\n\n')
# print(sorted(true_diagnoses, key=operator.itemgetter(1))[::-1])

#outputs = system_gal.run(input_values=observations[0][0])
#for observation in observations:
#    outputs = system_gal.run(input_values=observation[0])

#system_gal.draw()
