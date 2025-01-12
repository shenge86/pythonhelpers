# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 22:50:13 2023

@author: Shen
"""

from decimal import Decimal
import numpy as np
import matplotlib.pyplot as plt

sample_size = 625

counter = 0

ax = plt.gca()
ax.axes.xaxis.set_visible(True)
ax.axes.yaxis.set_visible(False)

for i in range(50):
    sample = np.random.binomial(n=1, p=0.53, size =sample_size)   # Creates a sample drawn from a binomial distribution
    sample_mean = np.mean(sample)                           # Computes the sample mean
    x = [sample_mean-1.96*0.5/np.sqrt(sample_size), sample_mean+1.96*0.5/np.sqrt(sample_size)]    # 95% confidence interval
    y = [i/30, i/30]
    if sample_mean-1.96*0.5/np.sqrt(sample_size) <= 0.53 and 0.53 <= sample_mean+1.96*0.5/np.sqrt(sample_size):  # Updates the counter and colors the interval plot depending on whether or not it includes the true mean
        plt.plot(x,y,color="red")
        counter += 1
    else: 
        plt.plot(x,y,color="blue")

        plt.plot([0.53,0.53],[0,1.75],color="gray")

print(f' {round(Decimal((counter/50)*100),3)} percent of the intervals contain the true mean 0.53 (gray line)')

plt.savefig("myplot.png")