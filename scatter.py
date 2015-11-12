#!/usr/bin/python
#
# This script provides a set of functions for generating simple plots with matplotlib

import numpy as np
import itertools 
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def scatter(dx, dy, title, xlabel, ylabel):
    fig = plt.figure()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale(enable=True, axis=u'both', tight=False)
    ax = fig.add_subplot(1,1,1)
    fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
    yticks = mtick.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(yticks)

    for las in range(1,dx.shape[1]):
        x = dx[:,las] 
        y = dy[:,las] * 100
        ax.plot(x,y, label='%d' % las)
        plt.legend(title='')
