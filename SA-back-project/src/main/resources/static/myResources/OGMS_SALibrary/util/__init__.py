import numpy as np
from sklearn.metrics.pairwise import pairwise_kernels


def empiricalcdf(x, xi):

    ###########################################################################
    # Check inputs
    ###########################################################################
    if not isinstance(x, np.ndarray):
        raise ValueError('"x" must be a numpy.array.')
    if x.dtype.kind != 'f' and x.dtype.kind != 'i' and x.dtype.kind != 'u':
        raise RuntimeError('"x" must contain floats or integers.')

    if not isinstance(xi, np.ndarray):
        raise ValueError('"xi" must be a numpy.array.')
    if xi.dtype.kind != 'f' and xi.dtype.kind != 'i' and xi.dtype.kind != 'u':
        raise ValueError('"xi" must contain floats or integers.')

    x = x.flatten() # shape (N, )
    xi = xi.flatten() # shape (Ni, )

    ###########################################################################
    # Estimate empirical CDF values at 'x':
    ###########################################################################

    N = len(x)
    F = np.linspace(1, N, N)/N

    x = np.flip(np.sort(x), axis=0)
    x, iu = np.unique(x, return_index=True)
    iu = N-1 - iu # Correct the indices so that they refer to the vector x sorted

    F = F[iu]
    N = len(F)

    # Interpolate the empirical CDF at 'xi':
    Fi = np.ones((len(xi),))

    for j in range(N-1, -1, -1):
        Fi[xi[:] <= x[j]] = F[j]

    Fi[xi < x[0]] = 0

    return Fi


def split_sample(Z, n=10):

    ###########################################################################
    # Check inputs
    ###########################################################################

    if not isinstance(Z, np.ndarray):
        raise ValueError('"Z" must be a numpy.array.')
    if Z.dtype.kind != 'f' and Z.dtype.kind != 'i' and Z.dtype.kind != 'u':
        raise ValueError('"Z" must contain floats or integers.')

    Nz = Z.shape
    N = Nz[0]
    if len(Nz) == 2:
        if Nz[1] != 1:
            raise ValueError('"Z" must be of size (N, ) or (N,1).')
        Z = Z.flatten()
    elif len(Nz) != 1:
        raise ValueError('"Z" must be of size (N, ) or (N,1).')

    if not isinstance(n, (int, np.int8, np.int16, np.int32, np.int64)):
        raise ValueError('"n" must be scalar and integer.')
    if n <= 0:
        raise ValueError('"n" must be positive.')

    ###########################################################################
    # Create sub-samples
    ###########################################################################
    n_eff = n

    Zu = np.unique(Z) # district values of Z

    if len(Zu) < n: # if number of distinct values less than the specified
                    # number of groups

        n_eff = len(Zu)
        Zc = np.sort(Zu) # groups' centers are the different values of Xi
        Zk = np.concatenate((Zc, np.array([Zc[-1]]))) # groups' edges

    else:
        # Sort values of Z in ascending order:
        Z_sort = np.sort(Z)
        # Define indices for splitting Z into ngroup equiprobable groups
        # (i.e. with the same number of values):
        split = [int(round(j)) for j in np.linspace(0, N, n_eff+1)]
        split[-1] = N-1
        # Determine the edges of Z in each group:
        Zk = Z_sort[split]

        # Check that values that appear several times in Z belong to the same group:
        idx_keep = np.full((n_eff+1, ), True, dtype=bool)
        for k in range(len(Zk)):
            if np.sum(Zk[k+1:n_eff+1] == Zk[k]) > 1:
                if k < len(Zk)-1:
                    idx_keep[k] = False
        Zk = Zk[idx_keep]
        n_eff = len(Zk) - 1

        Zc = np.mean(np.column_stack((Zk[np.arange(0, n_eff)],
                                      Zk[np.arange(1, n_eff+1)])),
                     axis=1) # centers (average value of each group)

    # Determine the respective groups of the sample:
    idx = -1 * np.ones((N, ), dtype='int8')
    for k in range(n_eff):
        if k < n_eff - 1:
            idx[[j >= Zk[k] and j < Zk[k+1] for j in Z]] = k
        else:
            idx[[j >= Zk[k] and j <= Zk[k+1] for j in Z]] = k

    return idx, Zk, Zc, n_eff


def allrange(y, par):

    """ This function can be used as input argument ("output_condition") when
    applying PAWN.pawn_indices, PAWN.pawn_convergence, PAWN.pawn_plot_ks """

    idx = np.full(y.shape, True, dtype=bool)

    return idx


def de_mean(x):
    xmean = np.mean(x)
    return [xi - xmean for xi in x]


def covariance(x, y):
    n = len(x)
    return np.dot(de_mean(x), de_mean(y)) / (n-1)


def nni(y, A):
    """
    计算最邻近指数，用于判断采样点空间分布的分散性，随机分布时=1，聚集分布时<1，分散分布时>1
    一种多目标约束下的山地遥感试验空间采样方法 尹高飞
    """
    equal_num = 0
    min_dis_ave = 0
    for i in range(0, len(y)):
        poi = y[i]
        distances = []
        for j in range(0, len(y)):
            p = y[j]
            if j != i:
                # pearson
                # pearson = covariance(poi, p)/np.sqrt(np.var(poi)*np.var(p))
                # 余弦相似度
                # poi_norm = np.linalg.norm(poi)
                # p_norm = np.linalg.norm(p)
                # cos = np.dot(poi, p) / (poi_norm * p_norm)
                # 欧氏距离 高维失效
                dis = np.linalg.norm(poi - p)
                distances.append(dis)
                if (poi==p).all():
                    equal_num += 1
        min_dis = min(distances)
        min_dis_ave += min_dis / len(y)
    nni = min_dis_ave
    return nni,equal_num


def nni_kernel(y, A):
    k = pairwise_kernels(y, metric='cosine')
    min_dis_ave = 0
    for a in k:
        min_dis = min(a)
        min_dis_ave += min_dis / len(y)
    nni = min_dis_ave / (0.5 * np.sqrt(A / len(y)))
    return nni