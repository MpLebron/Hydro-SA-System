from SALib.analyze import sobol


def analyze(params, X, Y):
    """
        指数包括三种，S1、S1_conf、ST、ST_conf、S2、S2_conf，分别一阶（主效应）、总效应、二阶（可选）
        采样方法为 Sobol 序列，
        样例中的每8小组样本为一大组，第1组+第8组+第234组，计算主效应和总效应；第1组+第8组+第567组，计算二阶

        和eFAST有点类似，计算指标的时候，没有用到参数样本！
        不仅仅是没传过去，真正计算的时候，也只是使用结果数组Y！

        不同抽样算法对Sobol敏感性分析影响的研究  刘欢
        看来这个可以改变，不是绑定的
    """
    Si = sobol.analyze(params, Y, calc_second_order=True)
    Si['names'] = params['names']
    Si['coreVariables'] = ['S1', 'ST']  # S2二阶指数不便于比较
    return Si
