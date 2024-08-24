from SALib.sample import fast_sampler
 

def sample(params, number):
    """
        样本量 = N*D  D是参数量  N > 64
    """
    p = fast_sampler.sample(params, number)
    return p