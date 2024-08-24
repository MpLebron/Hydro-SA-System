import sys
import re
import numpy as np
from numpy.matlib import repmat
# 工具
from OGMS_SALibrary.sample import read_param_file
from OGMS_SALibrary.sample import read_setting_file
from OGMS_SALibrary.util import nni, nni_kernel
# 采样
from OGMS_SALibrary.sample import uniform_sampler, monte_carlo_sampler, latin_hypercube_sampler, \
    fractional_factorial_sampler, finite_difference_sampler, \
    morris_sampler, vbsa_sampler, sobol_sequence_sampler, fast_sampler, extended_fast_sampler
# 测试函数
from OGMS_SALibrary.test_functions import Ishigami
from OGMS_SALibrary.test_functions import Sobol_G
# SA方法
from OGMS_SALibrary.analyze import dgsm, fractional_factorial, rsa, \
    morris, vbsa, sobol, fast, rbd_fast, extended_fast,\
    delta, pawn
# 可视化方法
from OGMS_SALibrary.plotting import dgsm_plotter, fractional_factorial_plotter, rsa_plotter, \
    morris_plotter, vbsa_plotter, sobol_plotter, fast_plotter, rbd_fast_plotter, extended_fast_plotter,\
    delta_plotter, pawn_plotter

import matplotlib.pyplot as plt


if __name__ == '__main__':
    path = sys.argv[1]
    # path = 'I:/saProjectData/0573fa4c-2bb9-4285-aaa5-809b04da5451'
    params = read_param_file(path)
    sampleMethod, saMethod, number, targets, observations, objectiveFuns = read_setting_file(path)

    # 根据函数名动态调用采样方法  大写转小写、空格转下划线
    func = re.sub(r' +', '_', sampleMethod.lower())
    X = eval(func+".sample")(params, number)

    np.save(path+"params_sampling.npy",X)
    np.savetxt(path+"params_sampling.csv", X, fmt='%.04f', delimiter=',', header=",".join(params['names']), comments="")



