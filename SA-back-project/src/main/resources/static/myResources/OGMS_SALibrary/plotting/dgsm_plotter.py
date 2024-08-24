import matplotlib.pyplot as plt
import numpy as np


def bar(Si, plot=True, path="", target=""):
    labels = Si['names']
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    for key in Si:
        if key == 'dgsm':
            ax.bar(x, Si[key], width, label="dgsm", yerr=Si['dgsm_conf'])
        elif key == 'vi':
            ax.scatter(x, Si[key], label="vi")
            ax.plot(x, Si[key])

    ax.set_title('Sensitivity Index of DGSM')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()

    plt.savefig(path + 'SA_score_figure_' + target + '.jpg')
    if plot:
        plt.show()
