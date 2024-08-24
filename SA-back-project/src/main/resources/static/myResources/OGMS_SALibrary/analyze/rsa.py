import numpy as np
from numpy.matlib import repmat
from ..util import empiricalcdf


def analyze(params, X, Y):
    """
        采样方法不是固定的，比如 lhs 和 mc 都可以，但是样本量要正确。
        得出的结果有四个 mvd, spread, irr, idxb
           mvd：两个CDF（行为和非行为）之间的最大垂直差异。 0-1 绝对度量，值越大，敏感度越高
        spread：两个CDF（行为和非行为）之间的面积。相对度量，值越大，敏感度越高
           irr：输入范围缩减，即仅考虑行为集时，输入范围对于原始范围的相对缩减。0-1 绝对度量，值越低，敏感度越高
          idxb：满足条件的样本指数（行为）
    """
    threshold = Y.mean()

    Nx = X.shape
    N = Nx[0]
    M = Nx[1]
    Ny = Y.shape

    # Identify sets above and below the threshold:
    idxb = Y < repmat(threshold, N, 1).flatten()

    # Initialise arrays of indices:
    mvd = np.nan*np.ones([M, ])
    spread = np.nan*np.ones([M, ])
    irr = np.nan*np.ones([M, ])
    # Define above and below subsamples:
    Xb = X[idxb, :]
    Xnb = X[~idxb, :]

    for i in range(M):
        # Empirical CDF of behavioural and non-behavioural inputs:
        xx = np.unique(np.sort(X[:, i]))
        CDFb = empiricalcdf(Xb[:, i], xx)
        CDFnb = empiricalcdf(Xnb[:, i], xx)
        # Compute distances between CDFs:
        mvd[i] = np.max(abs(CDFb - CDFnb))
        spread[i] = np.trapz(np.max(np.stack((CDFb, CDFnb), axis=0), axis=0), x=xx) -\
             np.trapz(np.min(np.stack((CDFb, CDFnb), axis=0), axis=0), x=xx)

    # Ranges of input factors that produce ''behavioural'' output:
    xmin = np.min(Xb, axis=0)
    xmax = np.max(Xb, axis=0)
    # Compute the relative reduction wrt the original ranges of input factors
    irr = 1 - (xmax-xmin) / (np.max(X, axis=0)- np.min(X, axis=0))

    # Si = {'names': params['names'], 'mvd': mvd, 'spread': spread, 'irr': irr, 'idxb': idxb, }
    Si = {'names': params['names'], 'mvd': mvd, 'spread': spread, 'irr': irr, 'coreVariables': ['mvd', 'spread', 'irr']}
    return Si

