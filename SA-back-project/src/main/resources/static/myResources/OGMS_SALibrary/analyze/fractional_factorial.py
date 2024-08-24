from SALib.analyze import ff


def analyze(params, X, Y):
    """
        部分析因分析
        有 ME 和 IE 两个指标，分别是主效应和交互效应（二阶，可选）
        这个采样策略也是特定的，采样时会生成虚拟变量
    """
    Si = ff.analyze(params, X, Y, second_order=True)
    Si['coreVariables'] = ['ME', 'IE']  # IE二阶指数是以一维数组存储的，可以用于比较
    return Si
