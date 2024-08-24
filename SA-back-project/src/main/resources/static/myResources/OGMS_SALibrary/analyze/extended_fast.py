from SALib.analyze import fast


def analyze(params, X, Y):
    """
        得到 S1 S1_conf ST ST_conf 四个结果；
        将Y分成三部分，每部分计算一个参数的指标

        算是采样方法特定，真的是绑定的，采样时和计算时都会生成一个欧米噶！
        发现没，计算指标的时候，没有用到参数样本！
        不仅是没传过去，真正计算也是通过欧米噶计算的
    """
    Si = fast.analyze(params, Y)
    Si['coreVariables'] = ['S1', 'ST']
    return Si
