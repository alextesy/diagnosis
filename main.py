from System import System
from observation_parse import read_observation

system_gal = System.create_system(r'C:\Users\t-alkre\Documents\diagnosis\data_systems\c432.sys')
observations = read_observation(r'C:\Users\t-alkre\Documents\diagnosis\observations\c432_iscas85.obs')
for observation in observations:
    system_gal.run(input_values=observation[0])