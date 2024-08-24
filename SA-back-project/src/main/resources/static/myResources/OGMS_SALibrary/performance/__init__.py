# 目标函数和精度评价是两回事吗？
# 目标函数：实测和模拟流量的LOG函数、DRMS函数、径流系数误差ROCE
# 精度评价：Nash效率系数（确定性系数）、百分比偏差Bias、相关系数R、模拟流量残差平方和RSS、模拟平均流量Qvg
#           洪峰相对误差REPF、洪量相对误差RE、洪量精度评定指标IVF

# 基于统计度量的目标函数
"""
    Nash效率系数：用于评价实测值与模拟值两个序列的吻合程度
    确定性系数R^2：用于评价实测值与模拟值两个序列的吻合程度
    相关系数R：用于判断实测值与模拟值两个序列的相关性 跟R2太像
    百分比偏差Bias：用于评价模拟序列相对于实测序列的偏离程度 跟RE太像
"""
# 基于径流特征的目标函数 综合考虑流量和洪水三要素（洪峰流量、洪水总量以及洪水过程线）
"""
    实测和模拟流量的LOG函数：侧重于小流量值的拟合误差
    实测和模拟流量的DRMS函数：侧重于大流量值的拟合误差
    
    径流系数误差ROCE：强调模拟过程整体的拟合精度
    
    洪峰相对误差Qre：用于评价洪峰洪量模拟误差
    洪量相对误差RE
"""
import numpy as np


# Nash效率系数：用于评价实测值与模拟值两个序列的吻合程度
def Nash(sim, obs):
    sim = np.array(sim)
    obs = np.array(obs)
    n = sim.shape[0]
    score = np.empty(n)
    for i in range(n):
        s = sim[i]
        err = ((s - obs)**2).sum()
        den = ((obs - obs.mean())**2).sum()
        score[i] = 1-err/den
    return score
# 确定性系数R^2：用于评价实测值与模拟值两个序列的吻合程度
def RSquared(sim, obs):
    sim = np.array(sim)
    obs = np.array(obs)
    n = sim.shape[0]
    score = np.empty(n)
    for i in range(n):
        s = sim[i]
        nume = pow(((s-s.mean())*(obs-obs.mean())).sum(), 2)
        den = ((s-s.mean())**2).sum() * ((obs-obs.mean())**2).sum()
        score[i] = nume/den
    return score
# 实测和模拟流量的LOG函数：侧重于小流量值的拟合误差
def Log(sim, obs):
    sim = np.array(sim)
    obs = np.array(obs)
    n = sim.shape[0]
    score = np.empty(n)
    for i in range(n):
        s = sim[i]
        nume = ((np.log(s)-np.log(obs))**2).sum()
        score[i] = nume/len(s)
    return score
# 实测和模拟流量的DRMS函数：侧重于大流量值的拟合误差
def DRMS(sim, obs):
    sim = np.array(sim)
    obs = np.array(obs)
    n = sim.shape[0]
    score = np.empty(n)
    for i in range(n):
        s = sim[i]
        nume = ((s - obs)**2).sum()
        score[i] = pow(nume/len(s), 0.5)
    return score
# 径流系数误差ROCE：强调模拟过程整体的拟合精度
def ROCE(sim, obs):
    sim = np.array(sim)
    obs = np.array(obs)
    n = sim.shape[0]
    score = np.empty(n)
    for i in range(n):
        s = sim[i]
        nume = s.mean()-obs.mean()
        score[i] = abs(nume/obs.mean())
    return score
# 洪峰相对误差Qre：用于评价洪峰模拟误差
def QRE(sim, obs):
    sim = np.array(sim)
    obs = np.array(obs)
    n = sim.shape[0]
    score = np.empty(n)
    for i in range(n):
        s = sim[i]
        nume = s.max()-obs.max()
        score[i] = abs(nume/obs.max())
    return score
# 水量相对误差RE
def RE(sim, obs):
    sim = np.array(sim)
    obs = np.array(obs)
    n = sim.shape[0]
    score = np.empty(n)
    for i in range(n):
        s = sim[i]
        nume = (s-obs).sum()
        den = obs.sum()
        score[i] = abs(nume/den)
    return score


if __name__ == '__main__':
    sim = [[1, 2, 3, 4, 5], [1, 1, 3, 3, 5]]
    obs = [1, 2, 3, 4, 4]
    score = Nash(sim, obs)
    print("nash: ", score)
    score = RSquared(sim, obs)
    print("r2: ", score)
    score = Log(sim, obs)
    print("log: ", score)
    score = DRMS(sim, obs)
    print("drms: ", score)
    score = ROCE(sim, obs)
    print("roce: ", score)
    score = QRE(sim, obs)
    print("qre: ", score)
    score = RE(sim, obs)
    print("re: ", score)
