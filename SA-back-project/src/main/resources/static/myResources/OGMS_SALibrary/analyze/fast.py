import numpy as np
import math


def analyze(params, X, Y, Nharm=4):
    """
        得到 S1, V, A, B, Vi，分别是一阶指数、总方差、傅里叶系数A、傅里叶系数B、每个参数的方差
        有用的可能就是S1 和 Vi

        参考自 SAFE的fast 和 SALib的efast
        前面 omega 的计算是SALib
        后面 Si 的计算是SAFE
    """

    D = params['num_vars']

    Ny = Y.shape
    N = Ny[0]

    omega = np.zeros([D])
    omega[0] = math.floor((N - 1) / (2 * Nharm))
    m = math.floor(omega[0] / (2 * Nharm))

    if m >= (D - 1):
        omega[1:] = np.floor(np.linspace(1, m, D - 1))
    else:
        omega[1:] = np.arange(D - 1) % m + 1

    # Compute Fourier coefficients (vectors A and B) from Y
    A = np.zeros((N,))
    B = np.zeros((N,))
    start = 2 if N%2==0 else 1
    baseplus = np.sum(np.reshape(Y[start:], (int((N - 1) / 2), 2)), axis=1)  # shape ((N-1)/2,1)
    baseminus = -np.diff(np.reshape(Y[start:], (int((N - 1) / 2), 2)), axis=1).flatten()  # shape ((N-1)/2,1)
    for j in range(N):
        if (j + 1) % 2 == 0:  # j+1 is even
            sp = Y[0]
            for k in range(int((N - 1) / 2)):
                sp = sp + baseplus[k] * np.cos((j + 1) * (k + 1) * np.pi / N)
            A[j] = sp / N
        else:  # j is odd
            sp = 0
            for k in range(int((N - 1) / 2)):
                sp = sp + baseminus[k] * np.sin((j + 1) * (k + 1) * np.pi / N)
            B[j] = sp / N

    # Compute main effect from A and B
    V = 2 * np.sum(A ** 2 + B ** 2)  # total output variance
    Vi = np.nan * np.zeros((D,))  # output variances from the i-th input
    for i in range(D):
        idx = np.arange(1, Nharm + 1) * int(omega[i])
        Vi[i] = 2 * np.sum(A[idx - 1] ** 2 + B[idx - 1] ** 2)
    S1 = Vi / V
    # return S1, V, A, B, Vi

    Si = {'names': params['names'], 'S1': S1, 'Vi': Vi, 'coreVariables': ['S1', 'Vi']}

    return Si
