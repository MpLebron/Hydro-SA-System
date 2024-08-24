import numpy as np
from warnings import warn
from ..util import empiricalcdf, split_sample, allrange


def analyze(params, X, Y, n=10, Nboot=1, dummy=False, output_condition=allrange, par=[]):
    """
        KS_median, KS_mean, KS_max, KS_dummy
        KS检验的指标是D，条件和无条件的两条累积分布曲线的最大垂直差作
        KS值越小代表两组结果差异小，敏感度也就小；值越大，敏感度也就越大

        没有特定的采样方法，lhs或rsu都行

        参考自SAFE
    """
    YY, xc, NC, n_eff, Xk, XX = pawn_split_sample(X, Y, n)

    Nx = X.shape
    N = Nx[0]
    M = Nx[1]

    # Compute indices
    YF = np.unique(Y)   # Set points at which the CDFs will be evaluated:

    # Initialize sensitivity indices
    KS_median = np.nan * np.ones((Nboot, M))
    KS_mean = np.nan * np.ones((Nboot, M))
    KS_max = np.nan * np.ones((Nboot, M))
    if dummy: # Calculate index for the dummy input
        KS_dummy = np.nan * np.ones((Nboot, ))

    # Compute conditional CDFs
    # (bootstrapping is not used to assess conditional CDFs):
    FC = [np.nan] * M
    for i in range(M): # loop over inputs
        FC[i] = [np.nan] * n_eff[i]
        for k in range(n_eff[i]): # loop over conditioning intervals
            FC[i][k] = empiricalcdf(YY[i][k], YF)

    # Initialize unconditional CDFs: 降雨
    FU = [np.nan] * M

    # Determine the sample size for the unconditional output bootsize:
    bootsize = [int(np.min(i)) for i in NC] # numpy.ndarray(M,)

    bootsize_unique = np.unique(bootsize)
    N_compute = len(bootsize_unique)  # number of unconditional CDFs that will

    if dummy:
        bootsize_min = min(bootsize)
        idx_bootsize_min = np.where([i == bootsize_min for i in bootsize])[0]
        idx_bootsize_min = idx_bootsize_min[0] # index of an input for which
        # the sample size of the unconditional sample is equal to bootsize_min

        if N_compute > 1:
            warn('The number of data points to estimate the conditional and '+
                 'unconditional output varies across the inputs. The CDFs ' +
                 'for the dummy input were computed using the minimum sample ' +
                 ' size to provide an estimate of the "worst" approximation' +
                 ' of the sensitivity indices across input.')

    # Compute sensitivity indices with bootstrapping
    for b in range(Nboot): # number of bootstrap resample

        # Compute empirical unconditional CDFs
        for kk in range(N_compute): # loop over the sizes of the unconditional output

            idx_bootstrap = np.random.choice(np.arange(0, N, 1), size=(bootsize_unique[kk], ), replace='False')
            # Compute unconditional CDF:
            FUkk = empiricalcdf(Y[idx_bootstrap], YF)

            idx_input = np.where([i == bootsize_unique[kk] for i in bootsize])[0]
            for i in range(len(idx_input)):
                FU[idx_input[i]] = FUkk

        # Compute KS statistic between conditional and unconditional CDFs:
        KS_all = pawn_ks(YF, FU, FC, output_condition, par)

        #  Take a statistic of KS across the conditioning intervals:
        KS_median[b, :] = np.array([np.median(j) for j in KS_all])  # shape (M,)
        KS_mean[b, :] = np.array([np.mean(j) for j in KS_all])  # shape (M,)
        KS_max[b, :] = np.array([np.max(j) for j in KS_all])  # shape (M,)

        if dummy:
            idx_dummy = np.random.choice(np.arange(0, N, 1), size=(bootsize_min, ), replace='False')
            # Compute empirical CDFs for the dummy input:
            FC_dummy = empiricalcdf(Y[idx_dummy], YF)
            # Compute KS stastic for the dummy input:
            KS_dummy[b] = pawn_ks(YF, [FU[idx_bootsize_min]], [[FC_dummy]],
                                  output_condition, par)[0][0]

    if Nboot == 1:
        KS_median = KS_median.flatten()
        KS_mean = KS_mean.flatten()
        KS_max = KS_max.flatten()

    if dummy:
        Si = {'names': params['names'], 'KS_median': KS_median, 'KS_mean': KS_mean, 'KS_max': KS_max,
              'KS_dummy': KS_dummy, 'coreVariables': ['KS_median', 'KS_mean', 'KS_max']}
        # return KS_median, KS_mean, KS_max, KS_dummy
    else:
        Si = {'names': params['names'], 'KS_median': KS_median, 'KS_mean': KS_mean, 'KS_max': KS_max,
              'coreVariables': ['KS_median', 'KS_mean']}
        # return KS_median, KS_mean, KS_max
    return Si


def pawn_split_sample(X, Y, n=10):

    Nx = X.shape
    Ny = Y.shape
    if len(Nx) != 2:
        raise ValueError('input "X" must have shape (N,M)')
    N = Nx[0]
    M = Nx[1]
    ###########################################################################
    # Check inputs
    ###########################################################################
    if isinstance(n, (int, np.int8, np.int16, np.int32, np.int64)):
        n = [n] * M
    ###########################################################################
    # Create sub-samples
    ###########################################################################
    # Intialise variables
    YY = [np.nan] * M
    XX = [np.nan] * M
    xc = [np.nan] * M
    NC = [np.nan] * M
    n_eff = [np.nan] * M
    Xk = [np.nan] * M

    for i in range(M): # loop over the inputs

        idx, Xk[i], xc[i], n_eff[i] = split_sample(X[:, i], n[i])
        # "idx" contains the indices for each group for the i-th input

        XX[i] = [np.nan] * n_eff[i] # conditioning samples for i-th input
        YY[i] = [np.nan] * n_eff[i]
        NC[i] = np.nan * np.ones((n_eff[i], )) # shapes of the conditioning
        # samples for i-th input

        for k in range(n_eff[i]): # loop over the conditioning intervals
            idxk = idx == k # indices of the k-th conditioning interval
            XX[i][k] = X[idxk, :]
            YY[i][k] = Y[idxk]
            NC[i][k] = np.sum(idxk)

        # Print a warning if the number of groups that were used is lower than
        # the prescribed number of groups:
        if n_eff[i] < n[i]:
            warn("For X%d, %d groups were used instead of " % (i+1, n_eff[i]) +
                 "%d so that values that are repeated several time " % (n[i]) +
                 "belong to the same group")

    return YY, xc, NC, n_eff, Xk, XX


def pawn_ks(YF, FU, FC, output_condition=allrange, par=[]):

    ###########################################################################
    # Check inputs
    ###########################################################################

    if not callable(output_condition):
        raise ValueError('"output_condition" must be a function.')
    if not isinstance(par, list):
        raise ValueError('"par" must be a list.')

    M = len(FC) # number of inputs

    # Initialise variable
    KS = [np.nan] * M

    # Find subset of output values satisfying a given condition
    idx = output_condition(YF, par)

    # Calculate KS statistics:
    for i in range(M): # loop over inputs
        n_effi = len(FC[i])
        KS[i] = np.nan * np.ones((n_effi,))

        for k in range(n_effi): # loop over conditioning intervals
            # Compute KS:
            KS[i][k] = np.max(abs(FU[i][idx] - FC[i][k][idx]))

    return KS

