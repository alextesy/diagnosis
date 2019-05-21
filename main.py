from System import System
from observation_parse import read_observation
from PBFS import get_diagnose
import random
import operator


gate_prior = random.random() * 0.5

observation_prior = 1.0 - random.random() * 0.25

system_gal = System.create_system(r'data_systems\c17.sys')
observations = read_observation(r'C:\Users\t-alkre\Documents\diagnosis\observations\c17_iscas85.obs')
predicted_diagnoses = get_diagnose(system_gal, observations[0], gate_prior, observation_prior, True)

observation = observations[0]

observation_inputs = observation[0]
observation_outputs = observation[1]

observation_output_values = {}
for o, v in observation_outputs.items():
    if random.random() <= observation_prior:
        observation_output_values[o] = v
    else:
        observation_output_values[o] = 1 - v

true_diagnoses = get_diagnose(system_gal, observations[0], gate_prior, 1, False)

print(sorted(predicted_diagnoses, key=operator.itemgetter(1))[::-1])
print('\n\n\n')
print(sorted(true_diagnoses, key=operator.itemgetter(1))[::-1])

#outputs = system_gal.run(input_values=observations[0][0])
#for observation in observations:
#    outputs = system_gal.run(input_values=observation[0])

#system_gal.draw()
