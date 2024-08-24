import math
from SALib.sample import saltelli


def sample(params, number):
    """
        样本量 = N*(D+2) | N*(2D+2)  D是参数量，前者为不计算二阶，后者为计算二阶
        N 应该是2的幂次方，且小于 skip_values，否则会出现警告，影响 Sobol 序列的收敛性
    """
    skip_values = 2 ** int(math.log(number, 2)+1)
    p = saltelli.sample(params, number, calc_second_order=True, skip_values=skip_values)
    return p
