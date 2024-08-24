from SALib.sample import finite_diff


def sample(params, number):
    """
        样本量 = N*(D+1) D是参数量

        dgsm 使用这个采样方式
        采样策略是随意的，但是样本量要正确。
        示例中采用的是Sobol序列，然后对其进行有限差分，而形成的
    """
    p = finite_diff.sample(params, number)
    return p