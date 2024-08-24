from SALib.sample import latin


def sample(params, number):
    """
        样本量也没有要求，给多少，是多少
        这个方法是通用的
        rbd_fast,vbsa 使用这个采样方式
    """
    p = latin.sample(params, number)
    return p
