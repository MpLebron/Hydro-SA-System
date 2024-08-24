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
from OGMS_SALibrary.performance import *


def compute(target):

    # 如果有实测数据，并且选择了目标函数，需要根据模拟结果和实测数据计算目标函数，用于敏感性分析
    if target in observations:
        # 读取该target的目标函数结果文件
        scoreObj = np.loadtxt(path + "obj_" + target + ".dat", delimiter="\t", skiprows=1)
        # "Nash", "RSquared", "Log", "DRMS", "ROCE", "QRE", "RE"
        indexs = []
        for obj in objectiveFuns:
            if obj == "Nash":
                indexs.append(0)
            elif obj == "RSquared":
                indexs.append(1)
            elif obj == "Log":
                indexs.append(2)
            elif obj == "DRMS":
                indexs.append(3)
            elif obj == "ROCE":
                indexs.append(4)
            elif obj == "QRE":
                indexs.append(5)
            elif obj == "RE":
                indexs.append(6)

        if len(indexs)>0:
            score = scoreObj[:, indexs[0]]
            for i in range(1, len(indexs)):
                tmpScore = scoreObj[:, indexs[i]]
                score = (score+tmpScore)/2

            Si = eval(saMethod + ".analyze")(params, X, score)
        else:
            Si = eval(saMethod + ".analyze")(params, X, Y)
    else:
        Si = eval(saMethod+".analyze")(params, X, Y)

    # 先组装参数名
    str_Si = "names: "+'\t'.join(Si["names"])+'\n'
    for e in Si:
        if e != "names":
            # 一维浮点数数组
            if type(Si[e][0]) == np.float64:
                str_Si += e + ": " + '\t'.join(str('{:.2f}'.format(i)) for i in Si[e])+'\n'
            # 一维字符串数组 names coreVariables
            elif type(Si[e][0]) == type("a"):
                str_Si += e + ": " + '\t'.join(Si[e])+'\n'
            # 二维浮点数数组 sobol
            elif type(Si[e][0]) == np.ndarray:
                str_Si += e + ": "
                for i in range(len(Si[e])):
                    str_Si += '\t'.join(str('{:.2f}'.format(i)) for i in Si[e][i]) + '\n'
            # 二维字符串数值 fractional_factorial
            elif type(Si[e][0]) == type(()):
                str_Si += e + ": "
                for i in range(len(Si[e])):
                    str_Si += '-'.join(list(Si[e][i])) + '\t'

    with open(path + 'SA_score_' + target + '.txt', 'w', encoding='UTF-8') as f:
        f.write(str_Si)

    eval(saMethod + "_plotter.bar")(Si, False, path, target)

if __name__ == '__main__':
    path = sys.argv[1]
    # path = 'I:/saProjectData/ae2a1cac-b6e0-45fe-82a7-f30d36c41213'
    params = read_param_file(path)
    sampleMethod, saMethod, number, targets, observations, objectiveFuns = read_setting_file(path)

    # 读取采样文件
    X = np.load(path + "params_sampling.npy")

    # 读取结果索引文件
    with open(path + 'resultIndex.txt', 'r') as f:
        result = f.readlines()
    for i in range(0, len(result)):
        line = result[i].rstrip("\n")
        res = line.split(":")
        if res[0] == "resultForSA":
            resultForSA = res[1]
        elif res[0] == "resultIndexs":
            resultIndexs = list(map(int, res[1].split(",")))
        elif res[0] == "resultForDisplay":
            resultForDisplay = res[1].split(",")

    # 读取结果文件
    total = np.loadtxt(path + resultForSA, delimiter=" ")

    # 按照第一列：计算任务序号，升序排序，并删除第一列
    total = total[np.lexsort(total[:, ::-1].T)]
    total = total[:, 1:]

    # 计算各个模拟目标的参数敏感性指标
    for i in range(0, len(targets)):
        Y = total[:, resultIndexs[i]]
        compute(targets[i])





