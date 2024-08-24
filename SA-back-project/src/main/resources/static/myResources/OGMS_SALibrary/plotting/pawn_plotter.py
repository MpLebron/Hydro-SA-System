import matplotlib.pyplot as plt
import numpy as np


def bar(Si, plot=True, path="", target=""):
    labels = Si['names']
    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars
    fig, ax = plt.subplots()
    for key in Si:
        if key == 'KS_median':
            ax.bar(x-width, Si[key], width, label="KS_median")
        elif key == 'KS_mean':
            ax.bar(x, Si[key], width, label="KS_mean")
        elif key == 'KS_max':
            ax.bar(x+width, Si[key], width, label="KS_max")

    ax.set_title('Sensitivity Index of PAWN')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()

    plt.savefig(path + 'SA_score_figure_' + target + '.jpg')
    if plot:
        plt.show()
