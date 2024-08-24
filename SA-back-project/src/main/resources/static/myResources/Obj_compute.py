import sys
import numpy as np
from OGMS_SALibrary.performance import *


def compute(obs_data, sim_data):
    scoreArr = []
    score = Nash(sim_data, obs_data)
    scoreArr.append(score)

    score = RSquared(sim_data, obs_data)
    scoreArr.append(score)

    score = Log(sim_data, obs_data)
    scoreArr.append(score)

    score = DRMS(sim_data, obs_data)
    scoreArr.append(score)

    score = ROCE(sim_data, obs_data)
    scoreArr.append(score)

    score = QRE(sim_data, obs_data)
    scoreArr.append(score)

    score = RE(sim_data, obs_data)
    scoreArr.append(score)

    return scoreArr


path = sys.argv[1]
# path = "I:/saProjectData/da8effb5-b79d-4c6d-8a82-d7b628e3bdf8"
eventName = sys.argv[2]
# eventName = "Flow"
if __name__ == '__main__':
    # 读取观测数据与模拟数据
    # 第一行用#开头 作为注释行
    obs_data = np.loadtxt(path + "obs_" + eventName + ".txt", dtype=float, comments='#', usecols=(0), unpack=True)
    sim_data = np.loadtxt(path + "sim_result_" + eventName + ".dat", delimiter=" ")

    # 按照第一列：计算任务序号，升序排序，并删除第一列
    sim_data = sim_data[np.lexsort(sim_data[:, ::-1].T)]
    sim_data = sim_data[:, 1:]

    # 计算每次模拟结果的评价指标得分
    objs = compute(obs_data, sim_data)
    objs2 = list(map(list, zip(*objs))) # 行转列

    # 将结果写入文件
    obj_file_path = path + "obj_" + eventName + ".dat"
    title = ["Nash", "RSquared", "Log", "DRMS", "ROCE", "QRE", "RE"]
    with open(obj_file_path, 'w') as ft:
        ft.write('\t'.join(title) + "\n")
        for obj in objs2:
            ft.write('\t'.join(('%.2f' % i) for i in obj) + "\n")

    print("计算并保存完毕 -- " + obj_file_path)
