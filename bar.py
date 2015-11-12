import numpy as np
import itertools 
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def plot_bar(data, title, xlabel, ylabel, xticks, group_names, legend=True):
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
