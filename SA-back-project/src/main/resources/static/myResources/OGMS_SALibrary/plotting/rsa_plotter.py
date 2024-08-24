import matplotlib.pyplot as plt
import numpy as np


def bar(Si, plot=True, path="", target=""):
    labels = Si['names']
    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars
    fig, ax = plt.subplots()
    for key in Si:
        if key == 'mvd':
            ax.bar(x-width, Si[key], width, label="mvd")
        elif key == 'spread':
            ax.bar(x, Si[key], width, label="spread")
        elif key == 'irr':
            ax.bar(x+width, Si[key], width, label="irr")

    ax.set_title('Sensitivity Index of RSA')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()

    plt.savefig(path + 'SA_score_figure_' + target + '.jpg')
    if plot:
        plt.show()
