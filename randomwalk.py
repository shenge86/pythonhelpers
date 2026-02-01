# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 23:44:24 2026

@author: sheng
@name: Random Walk

@description:
    
    A one-dimensional random walk can also be looked at as a Markov chain whose state space is given by the integers 
    i = 0, +/-1, +/-2, ...
    for some number p satisfying 0 < p < 1
    
    Transition probabilities are given by
    P_i,i+1 = p = 1 - P_i,i-1
    
    I don't wear an ascot and I'm not few colors short of a rainbow
"""
import sys
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    print('Run 1D random walk')
    
    if len(sys.argv) > 1:
        tmax = sys.argv[2]
    else:
        tmax = input('Max time: ')
    
    if tmax in ['']:
        tmax = 10
    else:
        tmax = int(tmax)
    
    # initial point
    xstate = 0
    t = 0
    
    xarr  = [xstate]
    tarr  = np.arange(t, tmax+1)
    while t < tmax:
        r = np.random.rand()
        if r >= 0.5:
            xstate +=1
        else:
            xstate -=1
        
        xarr.append(xstate)
        
        t+=1
    
    print(xarr)
    
    #%% Plot
    plt.figure()
    plt.plot(tarr, xarr)
    plt.xlabel("Time")
    plt.ylabel("Values")
    plt.title("Random Walk vs time")
    plt.show()
    
    plt.figure()
    plt.hist(xarr)
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Histogram')
    plt.show()