import numpy as np
import matplotlib.pyplot as plt
import itertools 

def cmap(n):
    my_cmap = plt.cm.Set1
    colorIdx = np.linspace(0,1,9) #+ np.array([1.,0,1.,0,1.,0])/12
    
    my_cmap = plt.cm.Paired
    #colorIdx = np.linspace(0,1,6) #+ np.array([1.,0,1.,0,1.,0])/12
    colorIdx = np.array([1,2,5,7,9.25,11.125], dtype=float)/12 # alternating dark light
    #colorIdx = np.array([0,6,2,8,4,10], dtype=float)/12 # alternating dark light

    #print "colorIdx =", colorIdx
    color=itertools.cycle(my_cmap(colorIdx))
    return color
