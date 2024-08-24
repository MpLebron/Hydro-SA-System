import numpy as np


def sample(params, number):
    """
        均匀采样
        样本量，给多少，是多少
    """
    D = params['num_vars']
    bounds = np.array(params['bounds'])
    low = bounds[:, 0]
    high = bounds[:, 1]
    p = np.random.uniform(low, high, [number, D])
    return p
