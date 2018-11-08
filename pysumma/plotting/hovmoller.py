import numpy as np
import matplotlib.pyplot as plt


def hovmoller(data_array, xdim, ydim, how='mean', cmap='viridis'):
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
    print(y_da_dim, y_tg_dim, x_da_dim, x_tg_dim)
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
    fig, ax = plt.subplots(nrows=1, ncols=1)
    im = ax.axes.pcolormesh(x, y, z, cmap=cmap)
    ax.axes.axis([x.min(), x.max(), y.min(), y.max()])
    fig.colorbar(im)

    # TODO: Format axes and labels
    daysofweek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                  'Thursday', 'Friday', 'Saturday']
    seasons = ['DJF', 'MAM', 'JJA', 'SON']
    months = ['January', 'February', 'March', 'April',
              'May', 'June', 'July', 'August',
              'September', 'October', 'November', 'December']
    months_wb = months[0:-4] + months[-3:]
    return fig, ax
