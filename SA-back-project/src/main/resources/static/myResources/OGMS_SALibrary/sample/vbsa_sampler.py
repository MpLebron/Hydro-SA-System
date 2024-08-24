from . import latin_hypercube_sampler as latin
from . import monte_carlo_sampler as mc
from . import uniform_sampler as uniform
import numpy as np


def sample(params, number):
    """
        先用 latin/mc/uniform 采2*number个样本，在重采样2*number + D*number个样本，和sobol不计算二阶指数一样
        样本量 = N*(D+2)  D是参数量
    """
    X = latin.sample(params, 2*number)
    p = vbsa_resampling(X)
    return p


def vbsa_resampling(X):

    Nx = X.shape
    NX = Nx[0]
    M = Nx[1]

    N = int(NX/2)
    XA = X[0:N, :]
    XB = X[N:2*N, :]
    XC = np.nan*np.ones((N*M, M))

    Ci = np.zeros((N, M))

    for i in range(M):
        idxnot_i = np.concatenate((np.arange(0, i), np.arange(i+1, M)))
        Ci[:, idxnot_i] = XB[:, idxnot_i]
        Ci[:, i] = XA[:, i]
        XC[i*N:(i+1)*N, :] = Ci

    return np.vstack((XA, XB, XC))
