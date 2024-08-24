import numpy as np
from SALib.util import scale_samples


def sample(params, number):
    """
        随机模拟 (或者统计模拟) 方法有一个很酷的别名是蒙特卡罗方法(Monte Carlo Simulation)
        样本量，给多少，是多少
        通用的
    """
    D = params['num_vars']
    tmp = np.random.random([number, D])

    p = scale_samples(tmp, params)

    return p