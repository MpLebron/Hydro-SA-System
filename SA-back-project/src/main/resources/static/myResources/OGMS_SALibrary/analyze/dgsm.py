from SALib.analyze import dgsm


def analyze(params, X, Y):
    """
        有 vi vi_std 和 dgsm dgsm_conf ，分别是一阶和总效应
          First order (+conf.) and Total order (+conf.)

        采样策略是随意的，但是样本量要正确。 示例中采用 finite_difference_sampler
        是先进行Sobol序列，然后对其进行有限差分，而形成的
    """
    Si = dgsm.analyze(params, X, Y)
    Si['coreVariables'] = ['vi', 'dgsm']
    return Si
