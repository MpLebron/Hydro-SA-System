from SALib.sample import ff


def sample(params, number):
    """
        样本量 = 2^([log2 D]+1)  D是参数量
        注：对数换底公式：loga b = logc b / logc a    []:math.ceil()向上取整

        部分析因分析 采用这种采样方式
        这个采样策略也是特定的，采样时会生成虚拟变量
    """
    p = ff.sample(params, number)
    return p
