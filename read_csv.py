#!/usr/bin/python
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

import myplot

args = sys.argv
script = args.pop(0)
csv = args.pop(0)
assert len(args) == 0

save_file = os.path.splitext(csv)[0] # strip file extension

c = np.loadtxt(csv, delimiter=',', dtype=str)
nets = c[0,1:] # get top row
x = c[1:,0] # get left column
d = c[1:,1:].astype(float) # get the data
myplot.plot_line(d, "", "Integer Bits", "Relative Accuracy", x, nets)
plt.savefig(save_file + '.pdf', format='pdf', dpi=1000)
plt.show()
