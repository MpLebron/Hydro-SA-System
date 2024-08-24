import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np


def bar(Si, plot=True, path="", target=""):
    fig = plt.figure()
    gs0 = gridspec.GridSpec(1, 3, figure=fig)

    labels = Si['names']
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars mu_star sigma mu_star_conf
    for key in Si:
        if key == 'mu_star':
            ax1 = fig.add_subplot(gs0[:, 0])
            ax1.barh(x, Si[key], width, label="mu_star", xerr=Si['mu_star_conf'])
        elif key == 'sigma':
            ax2 = fig.add_subplot(gs0[:, 1:])
            for i in range(len(labels)):
                ax2.scatter(Si['mu_star'][i], Si[key][i], label=labels[i])

    ax1.set_yticks(x)
    ax1.set_yticklabels(labels)
    ax1.invert_yaxis()  # labels read top-to-bottom
    ax1.legend()

    ax2.set_xlabel('mu_star')
    ax2.set_ylabel('sigma')
    ax2.legend()

    fig.suptitle('Sensitivity Index of Morris')
    fig.tight_layout()

    plt.savefig(path + 'SA_score_figure_' + target + '.jpg')
    if plot:
        plt.show()
