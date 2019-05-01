from System import System
from observation_parse import read_observation
from PBFS import get_full_diagnose

system_gal = System.create_system(r'data_systems\c17.sys')
# observations = read_observation(r'C:\Users\t-alkre\Documents\diagnosis\observations\c17_iscas85.obs')
# get_full_diagnose(system_gal, observations[0])
#outputs = system_gal.run(input_values=observations[0][0])
#for observation in observations:
#    outputs = system_gal.run(input_values=observation[0])

system_gal.draw()
