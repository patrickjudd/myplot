import numpy as np
import itertools 
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def plot_sbar(data, title, xlabel, ylabel, xticks, group_names, legend=True):
    """
    plot a stacked bar graph (N bars stacked on top of eachother)
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
    max_text_width = 80/len(xticks)
    print "label:",max_x_label,"max:",max_text_width
    if (max_x_label > max_text_width):
        rot = 30

    fontsize = 20
    font = {'size' : fontsize}
    mpl.rc('font', **font)

    legend_outside=0
    n = data.shape[1]
    show_legend = legend and (n > 1);
    print "Show Legend =", show_legend
    
    # left bottom width height
    box = [0.15,0.12,0.82,0.85]
    figsize=[ 8, 6 ]
    bbanchor=[ 1, 1 ]
    legend_loc='upper right'
    if legend_outside and show_legend:
        print "Putting legend outside plot"
        box[2] /= 1.25
        bbanchor=( 1, 1 )
        legend_loc='upper right',
        figsize[0] *= 1.25
    if rot:
        box[1] = 0.2

    if ylabel == '':
        box[0] -= 0.05

    # Create Figure
    fig = plt.figure(figsize=figsize)
    #fig, ax = plt.subplots()
    # left bottom width height
    ax = fig.add_axes(box)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale(enable=True, axis=u'both', tight=False)
    ax.yaxis.grid(True)

    # dont use offset at the top of the figure
    y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(y_formatter)

    width=0.30
    ind = np.arange(data.shape[0])
    n = data.shape[1]
    if (len(xticks) > 20):
        xticks = ['']
    ax.set_xticklabels(xticks, rotation=rot)
    xtp = ind+width*n/2
    ax.set_xticks(xtp)

    dmin = np.min(data)
    dmax = np.max(data)
    diff = dmax-dmin

    ymin = 0
    ymax = 1.1
    #ymin = dmin-0.1*diff
    ymax = dmax+0.1*diff

    xmin = int(xticks[0])
    xmax = int(xticks[-1])
    xmin = 0
    xmax = len(xticks)
    
    plt.xticks(np.arange(0, len(xticks), 1))
    plt.autoscale(enable=True, axis=u'both', tight=True)

    axes = plt.gca()
    #axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    #axes.set_yticks(np.arange(ymin,ymax,0.1))

    color=iter(plt.cm.rainbow(np.linspace(0,1,n)))
    fill=iter(['','//'])
    p = [] # list of bars
    b = [0] * len(xticks) # bottom position
    for i,n in enumerate(n_labels):
        d = list(data[:,i])
        p.append(
                plt.bar(
                    ind, 
                    d, 
                    width, 
                    color=next(color), 
                    bottom=b,
                    align='center', 
                    hatch=next(fill)
                    )
                )
        b = np.add(b,d)

    if (show_legend):
        plt.legend(
                p, 
                n_labels,
                fontsize=fontsize,
                loc=legend_loc,
                bbox_to_anchor=(bbanchor),
                #bbox_to_anchor=(1,1),
                borderaxespad=0.5
                )

