import numpy as np
import itertools 
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import myplot


def bar(data, title, xlabel, ylabel, xticks, group_names, legend=True, fontsize=16):
    """
    data        an Nx or Nx * Nn array or ndarray
    xticks      labels for each x value
    group_names labels for each n value
    """

    legend=bool(int(legend)) 
    data = np.array(data)
    group_names = list(group_names)
    n_labels = group_names

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
    max_text_width = 60/len(xticks)
    print "label:",max_x_label,"max:",max_text_width
    if (max_x_label > max_text_width):
        rot = 30
    if (max_x_label > 2*max_text_width):
        rot = 60


    mpl.rc('font', family='Helvetica', size=fontsize)

    legend_outside=1
    n = data.shape[1]
    show_legend = legend and (n > 1);
    print "Show Legend =", show_legend
    
    # left bottom width height
    box = [0.10,0.12,0.82,0.85]
    figsize=[ 8, 6 ]
    bbanchor=[ 1, 1 ]
    legend_loc='upper right'
    if legend_outside and show_legend:
        print "Putting legend outside plot"
        box[2] /= 1.25
        bbanchor=( 1, 1 )
        legend_loc='upper left'
        figsize[0] *= 1.25
        box[0] -= 0.05
    if rot:
        box[0] += 0.02
        box[1] += 0.08
        box[3] -= 0.08

    if ylabel == '':
        box[0] -= 0.05

    if title != '':
        box[3] -= 0.05

    fig = plt.figure()
    #fig, ax = plt.subplots()
    # left bottom width height
    ax = fig.add_axes(box)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale(enable=True, axis=u'both', tight=False)
    ax.yaxis.grid(True)

    if (len(group_names) == 1):
        width=0.5
    else:
        width=0.9/len(group_names)

    ind = np.arange(data.shape[0])
    n = data.shape[1]
    if (len(xticks) > 20):
        xticks = ['']
    ax.set_xticklabels(xticks, rotation=rot, ha='right')
    xtp = ind+width*n/2
    ax.set_xticks(xtp)

    ymin = 1.0
    ymax = 1.0
    ymax = max(data)*1.1
    axes = plt.gca()
    # axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    #axes.set_yticks(np.arange(ymin,ymax,0.1))
    

    # add bars
    color=myplot.cmap(n)
    groups = list()
    for d in range(0,n):
        c=next(color)
        grp = ax.bar(ind + width*d, data[:,d], width, color=c)
        groups.append(grp)

    if (show_legend):
        plt.legend(
                groups, 
                n_labels,
                fontsize=fontsize,
                loc=legend_loc,
                bbox_to_anchor=(bbanchor),
                borderaxespad=0.5
                )

