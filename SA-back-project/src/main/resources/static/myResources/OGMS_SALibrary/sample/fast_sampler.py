import numpy as np
import math
from SALib.util import scale_samples


def sample(params, N, Nharm=4):
    """
        样本量 = N  N > 64  也就是，给多少，是多少
        其实和 SALib 里的采样方法的差别就在 omega 的生成上
        SAFE里太啰嗦，做的是同一件事
        参考自 SAFE的fast 和 SALib的efast
    """
    D = params['num_vars']

    if N <= 4 * Nharm ** 2:
        raise ValueError("""Sample size N > 4M^2 is required. M=4 by default.""")

    omega = np.zeros([D])
    omega[0] = math.floor((N - 1) / (2 * Nharm))
    m = math.floor(omega[0] / (2 * Nharm))

    if m >= (D - 1):
        omega[1:] = np.floor(np.linspace(1, m, D - 1))
    else:
        omega[1:] = np.arange(D - 1) % m + 1

    s = np.pi / 2 * (2 * np.arange(1, N + 1) - N - 1) / N
    X = np.nan * np.zeros((N, D))
    for n in range(N):
        X[n, :] = 1 / 2 + 1 / np.pi * np.arcsin(np.sin(omega * s[n]))

    X = scale_samples(X, params)

    return X
