#!/usr/bin/python
#
# This script provides a set of functions for generating simple plots with matplotlib

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def plot_line(data, title, xlabel, ylabel, xticks, group_names, legend=True):
    """
    data        an Nx or Nx * Nn array or ndarray
    xticks      labels for each x value
    group_names labels for each n value
    """
    legend=bool(int(legend)) 
    print "Show Legend =", legend
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

    font = {'family' : 'normal',
            'weight' : 'normal',
            'size'   : 20}

    mpl.rc('font', **font)

    n = data.shape[1]
    show_legend = legend and (n > 1);

    legend_outside=0
    # left bottom width height
    box = [0.12,0.12,0.85,0.85]
    if legend_outside and show_legend:
        box[2] = 0.6 
    if rot:
        box[1] = 0.2

    fig = plt.figure()
    #fig, ax = plt.subplots()
    ax = fig.add_axes(box)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    #plt.autoscale(enable=True, axis=u'both', tight=True)
    ax.yaxis.grid(True)


    # don't show labels for over 20 points
    if (len(xticks) > 20):
        xticks = ['']
    ax.set_xticklabels(xticks, rotation=rot)

    ymin = 0
    ymax = 1.1
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
    markers=iter(['x', ',', 'o', '.', '*'])

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
                #title='Layer',
                loc='center right', 
                borderaxespad=0.5
                )
        #plt.legend().draggable()

def plot_scatter(dx, dy, title, xlabel, ylabel):
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

def plot_bar(data, title, xlabel, ylabel, xticks, group_names):
    """
    data        an Nx or Nx * Nn array or ndarray
    xticks      labels for each x value
    group_names labels for each n value
    """

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
    assert(data.shape[0] == len(xticks)), "data.shape[0] = %d, len(xticks) = %d" % (data.shape[0],len(xticks))

    rot = 0
    max_x_label = max([len(str(s)) for s in xticks])
    max_text_width = 80/len(xticks)
    print "label:",max_x_label,"max:",max_text_width
    if (max_x_label > max_text_width):
        rot = 30

    fig = plt.figure()
    #fig, ax = plt.subplots()
    # left bottom width height
    ax = fig.add_axes([0.1,0.2,0.8,0.7])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale(enable=True, axis=u'both', tight=False)
    ax.yaxis.grid(True)

    width=0.30
    ind = np.arange(data.shape[0])
    n = data.shape[1]
    if (len(xticks) > 20):
        xticks = ['']
    ax.set_xticklabels(xticks, rotation=rot)
    xtp = ind+width*n/2
    ax.set_xticks(xtp)

    ymin = 0.8
    ymax = 1
    axes = plt.gca()
    # axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax*1.05])
    #axes.set_yticks(np.arange(ymin,ymax,0.1))
    
    groups = list()

    color=iter(plt.cm.rainbow(np.linspace(0,1,n)))
    for d in range(0,n):
        c=next(color)
        # grp = ax.bar(ind + width*d, data[:,d], width, color=c)
        grp = ax.bar(ind + width*d, data[:,d], width, color=c)
        groups.append(grp)

    if (n > 1):
        ax.legend(groups, group_names, bbox_to_anchor=(1.05, 1), loc='upper right', borderaxespad=0.)


