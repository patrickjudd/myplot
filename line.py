#!/usr/bin/python
#
# This script provides a set of functions for generating simple plots with matplotlib

import numpy as np
import itertools 
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def line(data, title, xlabel, ylabel, xticks, group_names, legend=True):
    """
    Plot a line graph with N lines
    data        an Nx or Nx * Nn array or ndarray
    xticks      labels for each x value
    group_names labels for each n value
    """
    legend=bool(int(legend)) 
    print "LINE"
    data = np.array(data)
    group_names = list(group_names)

    # if data is 1d, make it a 2d array
    if ( len(data.shape) == 1 ):
        # print "1D array: Reshaping"
        data = data.reshape(len(data),-1)
    else:
        assert data.shape[1] == len(group_names), "data.shape[1] = %d, len(group_names) = %d" % (data.shape[1],len(group_names))

    # print data.shape
    assert(len(data.shape) == 2)

    # try to make data fit the labels
    if (data.shape[0] != len(xticks)):
        print "xticks (", len(xticks), ") don't match data (", data.shape, ". trying to fix"
        data = data.T;
    assert(data.shape[0] == len(xticks)), "data.shape[0] = %d, len(xticks) = %d" % (data.shape[0],len(xticks))
    assert(data.shape[1] == len(group_names)), "data.shape[1] = %d, len(group_names) = %d" % (data.shape[1],len(group_names))

    # should I rotate x axis labels?
    rot = 0
    max_x_label = max([len(str(s)) for s in xticks])
    max_text_width = 80/len(xticks)
    print "max label width:",max_x_label,"max:",max_text_width
    if (max_x_label > max_text_width):
        rot = 30

    fontsize = 18
    font = {'family' : 'normal',
            'weight' : 'normal',
            'size'   : fontsize}

    mpl.rc('font', **font)

    n = data.shape[1]
    show_legend = legend and (n > 1);

    legend_outside=1
    # left bottom width height
    box = [0.15,0.12,0.82,0.85]
    bbanchor=( 1, 1 )
    figsize=[ 8, 6 ]
    if legend_outside and show_legend:
        #box = [0.11,0.12,0.65,0.85]
        box[2] /= 1.25
        bbanchor=( 1.3, 0.447 )
        figsize[0] *= 1.25
    if rot:
        box[1] = 0.2

    if ylabel == '':
        box[0] -= 0.05

    # Create Figure
    fig = plt.figure(figsize=figsize)
    #fig, ax = plt.subplots()
    ax = fig.add_axes(box)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    #plt.autoscale(enable=True, axis=u'both', tight=True)
    ax.yaxis.grid(True)

    # dont use offset at the top of the figure
    y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(y_formatter)

    # don't show labels for over 20 points
    if (len(xticks) > 20):
        xticks = ['']
    ax.set_xticklabels(xticks, rotation=rot)

    dmin = np.min(data)
    dmax = np.max(data)
    diff = dmax-dmin

    ymin = 0
    ymax = 1.1
    ymin = dmin-0.1*diff
    ymax = dmax+0.1*diff

    xmin = int(xticks[0])
    xmax = int(xticks[-1])
    xmin = 0
    xmax = len(xticks)
    
    plt.xticks(np.arange(0, len(xticks), 1))


    axes = plt.gca()
    #axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    #axes.set_yticks(np.arange(ymin,ymax,0.1))
    
    groups = list()

    # data = X * N
    n = data.shape[1]
    color=iter(plt.cm.rainbow(np.linspace(0,1,n)))
    markers=itertools.cycle(['x', ',', 'o', '.', '*'])

    # plot each line
    for d in range(0,n):
        c=next(color)
        m=next(markers)
        #grp = ax.bar(ind + width*d, data[:,d], width, color=c)
        grp = ax.plot( range(len(xticks)) , data[:,d] , label='%s' % group_names[d], marker=m)
        groups.append(grp)

    if (show_legend):
        #ax.legend(groups, group_names, bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)
        #plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
        plt.legend(
                title='Layer',
                fontsize=fontsize,
                loc='center right',
                bbox_to_anchor=(bbanchor),
                borderaxespad=0.5
                )
