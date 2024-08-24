import numpy as np
from warnings import warn


def analyze(params, X, Y, Nboot=0, dummy=False):
    """
        S1、ST，分别一阶（主效应）、总效应，不能输出二阶敏感性指数

        和Sobol还是不一样，Sobol采用的Sobol序列采样
        这个的采样策略则不是指定的，lhs或rsu都行，其他的采样方法应该也可以，后面继续研究原理
        参考自 SAFE
    """
    D = params['num_vars']
    N = int((Y.shape[0] / (2 + D)))

    YA = Y[0:N]
    YB = Y[N:2 * N]
    YC = Y[2 * N:]

    # Compute indices
    YC = np.reshape(YC, (D, N))

    if Nboot > 1:   # Use bootstrapping
        bootsize = N  # size of bootstrap resamples
        B = np.random.randint(N, size=(bootsize, Nboot))

        Si = np.nan * np.ones((Nboot, D))
        STi = np.nan * np.ones((Nboot, D))
        Sdummy = np.nan * np.ones((Nboot,))
        STdummy = np.nan * np.ones((Nboot,))
        idxSi = np.nan * np.ones((Nboot, D))
        idxSTi = np.nan * np.ones((Nboot, D))
        idxdummy = np.nan * np.ones((Nboot,))

        for n in range(Nboot):
            Si[n, :], STi[n, :], Sdummy[n], STdummy[n], \
            idxSi[n, :], idxSTi[n, :], idxdummy[n] = \
                compute_indices(YA[B[:, n]], YB[B[:, n]], YC[:, B[:, n]])

        # Print to screen a warning message if any NAN was found in YA,YB. YC:
        if np.sum(np.isnan(YA)) + np.sum(np.isnan(YB)) + np.sum(np.isnan(YC.flatten())):

            str_Si = "\nX%d: %1.0f" % (1, np.mean(idxSi[:, 0]))
            str_STi = "\nX%d: %1.0f" % (1, np.mean(idxSTi[:, 0]))

            for i in range(1, D):
                str_Si = str_Si + "\nX%d: %1.0f" % (i + 1, np.mean(idxSi[:, i]))
                str_STi = str_STi + "\nX%d: %1.0f" % (i + 1, np.mean(idxSTi[:, i]))
            if dummy:
                str_Si = str_Si + "\ndummy: %1.0f" % (np.mean(idxdummy))
                str_STi = str_STi + "\ndummy: %1.0f" % (np.mean(idxdummy))

            warn('\n The average number of samples that could be used to ' +
                 'approximate main effects (Si) is:' + str_Si)
            warn('\n The average number of samples that could be used to ' +
                 'approximate total effects (STi) is:' + str_STi + '\n')

    else:
        Si, STi, Sdummy, STdummy, idxSi, idxSTi, idxdummy = \
            compute_indices(YA, YB, YC)

        # Print to screen a warning message if any NAN was found in YA,YB. YC:
        if np.sum(np.isnan(YA)) + np.sum(np.isnan(YB)) + np.sum(np.isnan(YC.flatten())):

            str_Si = "\nX%d: %1.0f" % (1, idxSi[0])
            str_STi = "\nX%d: %1.0f" % (1, idxSTi[0])
            for i in range(1, D, 1):
                str_Si = str_Si + "\nX%d: %1.0f" % (i + 1, idxSi[i])
                str_STi = str_STi + "\nX%d: %1.0f" % (i + 1, idxSTi[i])
            if dummy:
                str_Si = str_Si + "\ndummy: %1.0f" % (idxdummy)
                str_STi = str_STi + "\ndummy: %1.0f" % (idxdummy)

            warn('\n The number of samples that could be used to ' +
                 'approximate main effects (Si) is:' + str_Si)
            warn('\n The number of samples that could be used to ' +
                 'approximate total effects (STi) is:' + str_STi + '\n')
    if dummy:
        # return Si, STi, Sdummy, STdummy
        Si = {'names': params['names'], 'S1': Si, 'ST': STi, 'Sdummy': Sdummy, 'STdummy': STdummy, 'coreVariables': ['S1', 'ST']}
    else:
        # return Si, STi
        Si = {'names': params['names'], 'S1': Si, 'ST': STi, 'coreVariables': ['S1', 'ST']}
    return Si


def compute_indices(YA, YB, YC):
    Nc = YC.shape
    M = Nc[0]

    nanB = np.isnan(YB)
    nanA = np.isnan(YA)

    f0 = np.mean(YA[~nanA])
    VARy = np.mean(YA[~nanA] ** 2) - f0 ** 2

    Si = np.nan * np.ones((M,))
    STi = np.nan * np.ones((M,))
    idxSi = np.nan * np.ones((M,))
    idxSTi = np.nan * np.ones((M,))

    for i in range(M):
        yCi = YC[i, :]
        nanC = np.isnan(yCi)

        idx = nanA | nanC  # find indices where either YA or YCi is a NaN
        # and that will need to be excluded from computation

        Si[i] = (np.mean(YA[~idx] * yCi[~idx]) - f0 ** 2) / VARy
        # This is Eq (4.21) in Saltelli et al. (2008)
        # and also Eq. (12) in Saltelli et al. (2010), where the method is
        # attributed to Sobol (1993).

        idxSi[i] = np.sum(~idx)  # save number of samples that could be actually
        # used for estimating main effects
        # use 'numpy.sum' instead of 'sum' to spead up the code

        idx = nanB | nanC  # find indices where either YB or YCi is a NaN
        # and that will need to be excluded from computation

        STi[i] = 1 - (np.mean(YB[~idx] * yCi[~idx]) - f0 ** 2) / VARy
        # This is Eq (4.22) in Saltelli et al. (2008)

        idxSTi[i] = np.sum(~idx)  # save number of samples that could be actually
        # used for estimating total effects
        # use 'numpy.sum' instead of 'sum' to spead up the code

    # Compute indices for the dummy parameter:
    idx = nanA | nanB

    Sdummy = (np.mean(YA[~idx] * YB[~idx]) - f0 ** 2) / VARy
    # This is Eq (3) and (12) in Khorashadi Zadeh et al. (2017)

    STdummy = 1 - (np.mean(YB[~idx] ** 2) - f0 ** 2) / VARy
    # This is Eq (4) and (13) in Khorashadi Zadeh et al. (2017)

    idxdummy = np.sum(~idx)

    return Si, STi, Sdummy, STdummy, idxSi, idxSTi, idxdummy
