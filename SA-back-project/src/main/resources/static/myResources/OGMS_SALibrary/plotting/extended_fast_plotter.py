import matplotlib.pyplot as plt
import numpy as np


def bar(Si, plot=True, path="", target=""):
    labels = Si['names']
    x = np.arange(len(labels))  # the label locations
    width = 0.2  # the width of the bars
    fig, ax = plt.subplots()
    for key in Si:
        if key == 'S1':
            ax.bar(x-width/2, Si[key], width, label="S1", yerr=Si['S1_conf'])
        elif key == 'ST':
            ax.bar(x+width/2, Si[key], width, label="ST", yerr=Si['ST_conf'])

    ax.set_title('Sensitivity Index of eFAST')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()

    plt.savefig(path + 'SA_score_figure_' + target + '.jpg')
    if plot:
        plt.show()
