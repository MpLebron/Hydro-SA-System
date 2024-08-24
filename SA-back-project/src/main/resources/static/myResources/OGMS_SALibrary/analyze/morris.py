from SALib.analyze import morris


def analyze(params, X, Y):
    """
        mu mu_star sigma mu_star_conf
        众所周知，Morris的采样方法是特定的，过程比较复杂
        μ mu 或 μ* mu_star 越大，参数越敏感; σ sigma 越大，与其他参数的交互作用越强
    """
    Si = morris.analyze(params, X, Y)
    Si['coreVariables'] = ['mu_star', 'sigma']
    return Si
