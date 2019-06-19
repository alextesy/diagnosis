import os
from collections import defaultdict
import json
import pandas as pd
import numpy as np


system_results = defaultdict(lambda: defaultdict(list))
for f_name in os.listdir('results/randoming_gates'):
    if not f_name.endswith('.json'):
        continue

    sys_id = f_name.split('_')[0]
    with open(os.path.join('results/randoming_gates', f_name), 'r') as f:
        f_dict = json.load(f)

    obs_avg_diagnose_size = np.average([len(t[0]) for t in f_dict['predicted_diagnose_baseline']])
    system_results[sys_id]['diagnose_sizes'].append(obs_avg_diagnose_size)

    diff = f_dict['baseline_time'] - f_dict['experiment_time']
    if diff < 0:
        system_results[sys_id]['worse'].append(-diff)
        system_results[sys_id]['worse_normalized'].append(-diff / f_dict['baseline_time'])
    else:
        system_results[sys_id]['better'].append(diff)
        system_results[sys_id]['better_normalized'].append(diff / f_dict['baseline_time'])

results_df = pd.DataFrame(columns=['system', 'number of observations', 'improvements', 'improvement avg',
                                   'normalized improvement avg', 'decreases', 'decrease avg', 'normalized decrease avg',
                                   'avg diagnose size'])

for sys in system_results.keys():
    n_observations = len(system_results[sys]['better']) + len(system_results[sys]['worse'])

    results_df = results_df.append({'system': sys, 'number of observations': n_observations,
                                    'improvements': len(system_results[sys]['better']),
                                    'improvement avg': np.average(system_results[sys]['better']),
                                    'normalized improvement avg': np.average(system_results[sys]['better_normalized']),
                                    'decreases': len(system_results[sys]['worse']),
                                    'decrease avg': np.average(system_results[sys]['worse']),
                                    'normalized decrease avg': np.average(system_results[sys]['worse_normalized']),
                                    'avg diagnose size': np.average((system_results[sys]['diagnose_sizes']))},
                                   ignore_index=True)

results_df.to_csv('summed_results.csv', index=False)
