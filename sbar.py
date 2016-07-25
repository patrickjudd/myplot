import numpy as np
import itertools 
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import myplot
import prettyplotlib as ppl

def sbar(data, title, xlabel, ylabel, xticks, group_names, legend=True, fontsize=16, ylim=()):
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
    percent = 0 

    #mpl.rcParams['axes.linewidth'] = 1
    #rcParams['axes.linewidth'] = 7 # set the value globally

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
    max_text_width = 100/len(xticks)
    print "label:",max_x_label,"max:",max_text_width
    if (max_x_label > max_text_width):
        rot = 30

    #mpl.rc('font',**{'family':'sans-serif', 'sans-serif':['Helvetica'], 'size':fontsize})
    mpl.rc('font',**{'size':fontsize})

    legend_outside=0
    n = data.shape[1]
    show_legend = legend and (n > 1);
    print "Show Legend =", show_legend
    
    # left bottom width height
    box = [0.1,0.08,0.85,0.82]
    figsize=[ 8, 6 ] # WxH
    bbanchor=[ 0.5 , 1 ] # x,y
    legend_loc='lower center'
    if legend_outside and show_legend:
        print "Putting legend outside plot"
        box[2] /= 1.25
        bbanchor=( 1, 1 )
        legend_loc='upper left'
        figsize[0] *= 1.25
    if rot:
        box[1] += 0.08
        box[3] -= 0.08

    if ylabel == '':
        box[0] -= 0.05

    if title != '':
        box[3] -= 0.05

    # Create Figure
    fig = plt.figure(figsize=figsize)
    #fig, ax = plt.subplots()
    # left bottom width height
    ax = fig.add_axes(box)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.autoscale(enable=True, axis=u'both', tight=False)

    # gridelines
    ax.yaxis.grid(True, zorder=0,linestyle='solid', color='0.9', linewidth=1)

    # dont use offset at the top of the figure
    y_formatter = mpl.ticker.ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(y_formatter)

    if (len(group_names) == 1):
        width=0.4
    else:
        width=0.8/len(group_names)

    ind = np.arange(data.shape[0])
    n = data.shape[1]
    if (len(xticks) > 20):
        xticks = ['']
    ax.set_xticklabels(xticks, rotation=rot)
    xtp = ind#+width*n/2
    ax.set_xticks(xtp)
    # ax.spines['left'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)

    # convert to percent
    if percent:
        data *= 100
        fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
        yticks = mtick.FormatStrFormatter(fmt)
        ax.yaxis.set_major_formatter(yticks)

    dmin = np.min(data.sum(1))
    dmax = np.max(data.sum(1))
    diff = dmax-dmin

    if len(ylim) == 0:
        ymin = dmin-0.1*diff
        ymax = dmax+0.1*diff
    elif len(ylim) == 1:
        ymin = 0
        ymax = ylim[0]
    elif (ylim[0] == ''):
        ymin = dmin-0.1*diff
        ymax = ylim[1]
    elif (ylim[1] == ''):
        ymin = ylim[0]
        ymax = dmax+0.1*diff
    else:
        ymin = ylim[0]
        ymax = ylim[1]

    if (type(xticks[0]) is np.string_ or type(xticks[0]) is str):
        xmin = 0
        xmax = len(xticks)
    else:
        xmin = int(xticks[0])
        xmax = int(xticks[-1])

    xmin -= 0.5
    xmax += -0.5
    #plt.style.use('ggplot')
    #plt.xticks(np.arange(0, len(xticks), 1))
    #plt.autoscale(enable=True, axis=u'both', tight=True)

    axes = plt.gca()
    axes.set_xlim([xmin,xmax])
    axes.set_ylim([ymin,ymax])
    #axes.set_yticks(np.arange(ymin,ymax,0.1))

#    axes.spines['left'].linewidth = 2
#    axes.spines['bottom'].linewidth = 5

    # Colors / Patterns
    color=myplot.cmap(n)
    #color=itertools.cycle(plt.cm.Paired(np.linspace(0,1,6)))
    fill=iter(['','/'])

    p = [] # list of bars
    b = [0] * len(xticks) # bottom position

    # draw a veritcal line at 1
    plt.axhline(y=1.0, zorder=3, linewidth=2, color='black')

    for i,n in enumerate(n_labels):
        d = list(data[:,i])
        print n
        print d
        inds = ind - (len(n_labels) - 1)*width/2 + width*i
        print 'inds:', inds

        # annotate values to bars that go outside the plot
        if (d[0] > ymax):
            fs = int(width*30)
            ax.text(inds[0],ymax,"%.1f"%d[0], ha='center', va='bottom', fontsize=fs, zorder=5, rotation=45)
              # rect.get_x() + rect.get_width()/2., 1.05*height,
                            # '%d' % int(height),
                                            # ha='center', va='bottom')
        p.append(
                # ppl.bar(
                plt.bar(
                    #ind + width*i - width/2, 
                    inds,
                    d, 
                    width, 
                    zorder = 4,
                    color=next(color), 
                    #color=plt.rcParams['axes.color_cycle'][i],
                    alpha=1,
                    #bottom=b,
                    align='center', 
                    #hatch=next(fill)
                    hatch=''
                    )
                )
        b = np.add(b,d)

    if (show_legend):
        #p = p[::-1]
        plt.legend(
                p, 
                n_labels,
                ncol=n_labels,
                fontsize=fontsize,
                loc=legend_loc,
                bbox_to_anchor=(bbanchor),
                borderaxespad=1,
                frameon=False
                )

