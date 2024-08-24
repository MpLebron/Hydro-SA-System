from SALib.sample import morris


def sample(params, number):
    """
        样本量 = T*(G+1)  T:轨迹数N  G:分组数，没有就是D（参数量）

        众所周知，Morris的采样方法是特定的，过程比较复杂
    """
    p = morris.sample(params, number)
    return p