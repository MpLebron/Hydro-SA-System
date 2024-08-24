

def read_param_file(path):
    # 读取参数文件
    with open(path + 'paramsSum.txt', 'r') as f:
        param_list = f.readlines()

    num_vars = len(param_list)
    names = []
    bounds = []
    for i in range(0, len(param_list)):
        line = param_list[i].rstrip('\n')
        param = line.split(":")
        names.append(param[0])
        nums = param[1].split(",")
        bounds.append([float(nums[0]), float(nums[1])])

    params = {
        'num_vars': num_vars,
        'names': names,
        'groups': None,
        'bounds': bounds
    }
    return params


def read_setting_file(path):
    # 读取采样方法、样本数量
    with open(path + 'simSetting.txt', 'r') as f:
        sim_list = f.readlines()

    sampleMethod = ""
    saMethod = ""
    times = 0
    targets = []
    observations = []
    objectiveFuns = []
    for i in range(0, len(sim_list)):
        line = sim_list[i].rstrip('\n')
        sim = line.split(":")
        if sim[0] == "sampleMethod":
            sampleMethod = sim[1]
        elif sim[0] == "SAmethod":
            saMethod = sim[1]
        elif sim[0] == "simTimes":
            times = int(sim[1])
        elif sim[0] == "simTargets":
            targets = sim[1].split(',')
        elif sim[0] == "observations":
            observations = sim[1].split(',')
        elif sim[0] == "objectiveFuns":
            objectiveFuns = sim[1].split(',')

    return sampleMethod, saMethod, times, targets, observations, objectiveFuns

