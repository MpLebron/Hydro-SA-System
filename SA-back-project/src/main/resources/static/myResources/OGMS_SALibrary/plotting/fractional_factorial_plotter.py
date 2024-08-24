import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np


def bar(Si, plot=True, path="", target=""):
    fig = plt.figure()
    gs0 = gridspec.GridSpec(1, 3, figure=fig)

    labels = Si['names']
    data = Si['IE']
    index = 0
    s2 = [[0 for col in range(len(labels))] for row in range(len(labels))]
    for i in range(1, len(labels)):
        for j in range(i):
            s2[i][j] = data[index]
            index += 1
    s2 = np.array(s2)

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars
    for key in Si:
        if key == 'ME':
            ax1 = fig.add_subplot(gs0[:, 0])
            ax1.barh(x, Si[key], width, label="ME")
        elif key == 'IE':
            ax2 = fig.add_subplot(gs0[:, 1:])
            heatmap(s2, labels, labels, ax=ax2, cbarlabel="Interactive Effect")

    ax1.set_yticks(x)
    ax1.set_yticklabels(labels)
    ax1.invert_yaxis()  # labels read top-to-bottom
    ax1.legend()

    fig.suptitle('Sensitivity Index of FF')
    fig.tight_layout()

    plt.savefig(path + 'SA_score_figure_' + target + '.jpg')
    if plot:
        plt.show()


def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    # ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, rotation_mode="anchor")

    # Turn spines off and create white grid.
    # ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar

