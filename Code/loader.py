import numpy as np
import os
import pandas as pd

# data loading

def load(dataset="csv_files_data1", clip=True, permute=True, sort_node=0):

    weights, delays, fitnesses = [], [], []

    for file in os.listdir(dataset):
        if file[-4:] == '.csv':
            data_path = os.path.join(dataset, file)
            df = pd.read_csv(data_path, delimiter=',', header=None)
            weights.append(df.loc[0].to_numpy())
            delays.append(df.loc[1].to_numpy())
            fitnesses.append(df.loc[2][0])

    weights = np.stack(weights)
    delays = np.stack(delays)
    fitnesses = np.array(fitnesses)

    if clip:
        weights = np.clip(weights, -20., 20.)
        delays = np.clip(delays, 1., 10.)
        fitnesses = np.clip(fitnesses, -10000., 10000.)

    if permute:
        assert clip==True
        for individual in range(len(fitnesses)):
            weights[individual], delays[individual] = permutation(weights[individual], delays[individual], sort_node=sort_node)

    return weights, delays, fitnesses



def permutation(weights, delays, sort_node=0):

    # create adjacency matrix
    ad_mat_weights = np.zeros((14,14))
    ad_mat_delays = np.zeros((14,14))

    # populate adjacency matrix
    index = 0
    for a in range(0,6):
        for b in range(6,12):
            ad_mat_weights[a, b] = weights[index]
            ad_mat_delays[a, b] = delays[index]
            index +=1
    
    for a in range(6,12):
        for b in range(6,12):
            if a != b:
                ad_mat_weights[a, b] = weights[index]
                ad_mat_delays[a, b] = delays[index]
                index += 1

    for a in range(6,12):
        for b in range(12,14):
            ad_mat_weights[a, b] = weights[index]
            ad_mat_delays[a, b] = delays[index]
            index += 1

    # sort w/d of first node
    sorting = np.argsort(weights[sort_node*6:sort_node*6+6] / delays[sort_node*6:sort_node*6+6])

    # create small permutation matrix
    unit_mat = np.eye(6)
    small_perm_mat = unit_mat[sorting].T

    # embed small in large permutation matrix
    perm_mat = np.eye(14)
    perm_mat[6:12, 6:12] = small_perm_mat

    # permute adjacency matrix
    perm_ad_mat_weights = perm_mat.T @ ad_mat_weights @ perm_mat
    perm_ad_mat_delays = perm_mat.T @ ad_mat_delays @ perm_mat

    # reconstruct weight vector
    perm_weights, perm_delays = [], []

    for a in range(0,6):
        for b in range(6,12):
            perm_weights.append(perm_ad_mat_weights[a, b])
            perm_delays.append(perm_ad_mat_delays[a, b])
        
    for a in range(6,12):
        for b in range(6,12):
            if a != b:
                perm_weights.append(perm_ad_mat_weights[a, b])
                perm_delays.append(perm_ad_mat_delays[a, b])

    for a in range(6,12):
        for b in range(12,14):
            perm_weights.append(perm_ad_mat_weights[a, b])
            perm_delays.append(perm_ad_mat_delays[a, b])

    perm_weights = np.array(perm_weights)
    perm_delays = np.array(perm_delays)

    return perm_weights, perm_delays