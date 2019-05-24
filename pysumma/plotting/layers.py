'''Layer plotting for SUMMA output'''

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def plot_layers(var, depth, ax=None, colormap='viridis'):
    # Preprocess the data
    mask = var != -9999
    lo_depth = depth.where(depth > 0).where(mask).T
    hi_depth = depth.where(depth < 0).where(mask).T
    var = var.where(mask).T
    time = depth.time.values

    # Map colors to full range of data
    norm = plt.Normalize(var.min(), var.max())
    cmap = mpl.cm.get_cmap(colormap)
    rgba = cmap(norm(var))

    # Create axes if needed
    if not ax:
        fig, ax = plt.subplots(figsize=(18,8))

    # Plot soil layers - need to reverse because we plot bottom down
    for l in lo_depth.midToto.values[::-1]:
        y = lo_depth[l]
        y[np.isnan(y)] = 0
        ax.vlines(time, ymin=-y, ymax=0, color=rgba[l])

    # Plot snow layers - plot top down
    for l in hi_depth.midToto.values:
        y = hi_depth[l]
        y[np.isnan(y)] = 0
        ax.vlines(time, ymin=0, ymax=-y, color=rgba[l])

    # Add the colorbar
    mappable = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    mappable.set_array(var.values.flatten())
    plt.gcf().colorbar(mappable, label=var.long_name, ax=ax)
    return ax
