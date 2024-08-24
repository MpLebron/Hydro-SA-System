from SALib.analyze import rbd_fast


def analyze(params, X, Y):
    """
        S1 S1_conf 只有一阶指数
        采样策略不是绑定的，lhs或rsu都行
    """
    Si = rbd_fast.analyze(params, X, Y)
    Si['coreVariables'] = ['S1']
    return Si
