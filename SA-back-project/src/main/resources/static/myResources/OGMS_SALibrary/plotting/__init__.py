# 散点图(X-Y)、彩色散点图(X1-X2-Y)、平行坐标图(X1-Xn-Y)
# 这三类图形与任何SA方法无关，只是展示样本与结果的对应情况，因为这三种图会对应很多子图，所以还是在前端用echart绘制
# 另外的敏感性指数多以（带有误差线的）柱状图来表示结果，几个例外：morris的sigma；Sobol的S2；fractional_factorial的IE

# 参考Pianosi, Sensitivity analysis of environmental models: A systematic review with practical workflow

# dgsm: 一阶vi 一阶标准差vi_std 总效应dgsm 总效应置信范围dgsm_conf

# fractional_factorial: 主效应ME 交互效应 IE

# rsa: mvd, spread, irr, idxb
"""
       mvd：两个CDF（行为和非行为）之间的最大垂直差异。 0-1 绝对度量，值越大，敏感度越高
    spread：两个CDF（行为和非行为）之间的面积。相对度量，值越大，敏感度越高
       irr：输入范围缩减，即仅考虑行为集时，输入范围对于原始范围的相对缩减。0-1 绝对度量，值越低，敏感度越高
      idxb：满足条件的样本指数（行为）
"""

# morris: mu mu_star sigma mu_star_conf
#       μ mu 或 μ* mu_star 越大，参数越敏感; σ sigma 越大，与其他参数的交互作用越强

# vbsa:  S1、ST，分别一阶（主效应）、总效应

# sobol: S1、S1_conf、ST、ST_conf、S2、S2_conf，分别一阶（主效应）、总效应、二阶

# fast: S1, V, A, B, Vi，分别是一阶指数、总方差、傅里叶系数A、傅里叶系数B、每个参数的方差 有用的可能就是S1 和 Vi

# rbd_fast: S1 S1_conf 只有一阶指数

# extended_fast: S1 S1_conf ST ST_conf 分别一阶（主效应）、总效应

# delta: delta delta_conf S1 S1_conf

# pawn: KS_median, KS_mean, KS_max, KS_dummy
"""
    KS检验的指标是D，条件和无条件的两条累计分布曲线的最大垂直差作
    KS值越小代表两组结果差异小，敏感度也就小；值越大，敏感度也就越大
"""

