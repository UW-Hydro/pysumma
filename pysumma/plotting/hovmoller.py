import numpy as np
import matplotlib.pyplot as plt


def hovmoller(data_array, xdim, ydim, how='mean', colormap='viridis',
        variable_range=None, add_colorbar=True, cbar_kwargs={}, ax=None):
    '''Make a Hovmoller plot'''
    # Check if dimensions are valid
    time_groups = ['year', 'month', 'day', 'hour',
                   'minute', 'second', 'dayofyear',
                   'week', 'dayofweek', 'weekday', 'quarter']

    x_da_dim = xdim in list(data_array.dims)
    x_tg_dim = xdim in time_groups
    if x_tg_dim:
        xdim = 'time.{}'.format(xdim)
        if not how:
            raise Exception("Must specify aggregation "
                            "method for x dimension")
    elif not x_da_dim:
        raise Exception("x dimension not valid")

    y_da_dim = ydim in list(data_array.dims)
    y_tg_dim = ydim in time_groups

    if y_tg_dim:
        ydim = 'time.{}'.format(ydim)
        if not how:
            raise Exception("Must specify aggregation "
                            "method for y dimension")
    elif not y_da_dim:
        raise Exception("y dimension not valid")

    # Make sure the aggregation method is valid
    aggregation_methods = {'mean': lambda x: x.mean(),
                           'max': lambda x: x.max(),
                           'min': lambda x: x.min(),
                           'median': lambda x: x.median(),
                           'std': lambda x: x.std()}
    if how not in aggregation_methods.keys():
        raise Exception("Invalid time aggregation method given")

    # Do the group statements
    aggregate = aggregation_methods[how]
    grouped1 = data_array.groupby(ydim)
    grouped2 = grouped1.apply(lambda x: aggregate(x.groupby(xdim)))
    x = grouped2[(list(grouped2.dims)[1])]
    y = grouped2[(list(grouped2.dims)[0])]
    z = np.ma.masked_invalid(grouped2.values)

    if variable_range is not None:
        assert len(variable_range) == 2, 'variable_range must have 2 values!'
        norm = plt.Normalize(variable_range[0], variable_range[1])
    else:
        norm = plt.Normalize(np.nanmin(z), np.nanmax(z))

    if not ax:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))

    if variable_range:
        vmin, vmax = variable_range
    else:
        vmin, vmax = None, None

    if 'ax' not in cbar_kwargs.keys():
        cbar_kwargs['ax'] = ax

    im = ax.pcolormesh(x, y, z, cmap=colormap, vmin=vmin, vmax=vmax)
    ax.axes.axis([x.min(), x.max(), y.min(), y.max()])
    if add_colorbar:
        ax.get_figure().colorbar(im, **cbar_kwargs)

    # TODO: Format axes and labels
    daysofweek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                  'Thursday', 'Friday', 'Saturday']
    seasons = ['DJF', 'MAM', 'JJA', 'SON']
    months = ['January', 'February', 'March', 'April',
              'May', 'June', 'July', 'August',
              'September', 'October', 'November', 'December']
    months_wb = months[0:-4] + months[-3:]
    return ax
