

def preprocess_obs(obs):
    obs = obs.replace('.', '').replace('[','').replace(']','').replace('\n', '').replace(')', '')
    obs = obs.split(',')[2:]
    inputs_dict = {}
    outputs_dict = {}
    for i in obs:
        if 'i' in i:
            obs_dict = inputs_dict
        else:
            obs_dict = outputs_dict

        if i[0] == '-':
            obs_dict[i[1:]] = 0
        else:
            obs_dict[i] = 1
    return inputs_dict, outputs_dict


def read_observation(path):
    with open(path, 'r') as f:
        observation_list = f.read().split('.\n')
    observations = [preprocess_obs(obs) for obs in observation_list]
    return observations

# read_observation(r'C:\Users\t-alkre\Documents\diagnosis\observations\c17_iscas85.obs')
