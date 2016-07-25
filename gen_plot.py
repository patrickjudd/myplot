#!/usr/bin/python
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import sbar
import scipy.stats
import myplot
import math

args = sys.argv
script = args.pop(0)
csv = args.pop(0)
assert len(args) == 0

save_file = os.path.splitext(csv)[0]

normalize_to_0 = 0
normalize_total = 0
append_avg = 0
append_geo = 1
ignore_0 = 0
invert = 1

c = np.loadtxt(csv, delimiter=',', dtype=str)
n = c[0,1:] # different groups = first column
x = c[1:,0] # x axis labels = first row
d = c[1:,1:].astype(float) 

if [type(n[0]) is str]:
    n = [i.strip() for i in n]
if [type(x[0]) is str]:
    x = [i.strip() for i in x]

#d = np.fliplr(d)
#n = n[::-1]
#print n

# normalize to baseline (col 0)
if normalize_to_0:
    print "Normalizing to column 0: ", n[0]
    d = np.divide(d,d[:,0:1])

# normalize to total
if normalize_total:
    print "Normalizing to total of: ", n
    denom = d.sum(1)
    denom = denom.reshape(len(denom),-1)
    d = np.divide(d,denom)


if ignore_0:
    print "Ignoring column 0: ", n[0]
    d = d[:,1:]
    n = n[1:]

# d = delay

# caclulate inverse EDP an ED2
if 0:
    energy=0.93
    edp = d * energy
    eds = (d**2) * energy
    d = np.concatenate( (edp, eds) , axis=1)
    n = ["$1/EDP$","$1/ED^2$"]
    save_file='edp'

if append_avg:
    print "Appending Average"
    avg = d.mean(0)
    avg = avg.reshape( (1, avg.size) )
    print 'avg =', avg
    s = d.shape
    # shell = np.zeros( (s[0], s[1]+1, s[2]) )
    # shell[:,:-1,:] = d
    # shell[:,-1,:] = avg
    # d = shell
    d = np.concatenate( (d,avg), axis=0 )
    x = np.concatenate( (x,['avg']) )

if append_geo:
    avg = d.mean(0, keepdims=True)
    gmean = scipy.stats.gmean(d[:], axis=0)
    print d.shape
    print gmean.shape
    d = np.concatenate( (d,gmean.reshape(1,-1)), axis=0 )
    x = np.concatenate( (x,['geo']) )

if 0:
    d = 1.0/d
    d[-1] = scipy.stats.gmean(d[:-1])
    x[-1] = 'geo'
    ytitle="Speedup"
    save_file = "speedup-per-window"

if invert:
    
    d[:] = 1.0/d[:]
    # n = ['Speedup','Efficiency','1/EDP']
    n = ['Speedup','Efficiency']
    # ytitle="Speedup"
    ytitle=" "

else:
    ytitle=""


print "x,n,data"
print x
print n
print d

max_rest = d[1:,:].max()
ymax = (max_rest)*1.1

title=""
xtitle=""
x = myplot.rename_nets(x.tolist())
sbar.sbar(d, title, xtitle, ytitle, x, n, fontsize=12, ylim=(0,ymax))
plt.savefig(save_file + '.pdf', format='pdf', dpi=1000)
# plt.show()
