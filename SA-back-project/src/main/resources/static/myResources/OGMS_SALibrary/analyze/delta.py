from SALib.analyze import delta


def analyze(params, X, Y):
    """
        得到 delta delta_conf S1 S1_conf
        有用的还是 delta 和 delta_conf

        带有置信区间的柱状图 https://echarts.apache.org/examples/zh/editor.html?c=custom-error-bar
        置信区间是通过随机打乱Y和X，然后计算对应的Delta得分，计算他们之间的标准差

        没有特定的采样方法，lhs或rsu都行
    """
    Si = delta.analyze(params, X, Y)
    Si['coreVariables'] = ['delta', 'S1']
    return Si
