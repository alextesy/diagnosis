from System import System
from observation_parse import read_observation
from PBFS import get_diagnose, get_observation_diagnoses
import random
import operator


gate_prior = random.random() * 0.5

system_gal = System.create_system(r'data_systems\c17.sys')

observations = read_observation(r'observations\c17_iscas85.obs')

observation = observations[0]
observation_priors = {o: 1.0 - random.random() * 0.25 for o in observation[1].keys()}

predicted_diagnoses = get_diagnose(system_gal, observation, observation_priors, gate_prior)

# for observation in observations:
#     for o, v in observation[1].items():
#         if random.random() > (observation_priors[o]):
#             observation[1][o] = 1 - v
#
# observation = observations[0]
#
# true_diagnoses = get_observation_diagnoses(system_gal, observation, gate_prior)

print(sorted(predicted_diagnoses, key=operator.itemgetter(1))[::-1])
# print('\n\n\n')
# print(sorted(true_diagnoses, key=operator.itemgetter(1))[::-1])

#outputs = system_gal.run(input_values=observations[0][0])
#for observation in observations:
#    outputs = system_gal.run(input_values=observation[0])

#system_gal.draw()
