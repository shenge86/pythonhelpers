# -*- coding: utf-8 -*-
"""
######################################################
Created on Fri Jul 17 22:37:28 2020

@author: ShenGe
@name: interpolater
@description: 
    Standalone script which intakes a csv file with 2 columns of data. It interpolates the data according to a pre-defined range.    
######################################################
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# now interpolate data in 0.12 degree azimuth increments (3000 values)
def main(xmin,xmax,delta,xp,yp,zp):
    """Interpolates data for a certain delta
    :param xmin: minimum x coordinate for interpolated range (forms minimum value of x array)
    :param xmax: maximum x coordinate for interpolated range (forms maximum value of x array)
    :param delta: delta between each interpolated x coordinate
    :param xp: 1D x-coordinates (original data of x-coords)
    :param yp: 1D y-coordinates (original data of y-coords)
    :param zp: 1D z-coordinates (original data of z-coords)
    :return x, y, z: interpolated values in x and y coords interpolated based on x
    :rtype: float with same shape as x
    """
    numpts = int((xmax-xmin)/delta) + 1
    # make new x array
    x = np.linspace(xmin,xmax,numpts)            
    # interpolate
    y = np.interp(x,xp,yp)
    z = np.interp(x,xp,zp)
    return x,y,z

if __name__ == "__main__":
    print("Running")
    
    # parameters
    xmin = 0
    xmax = 359.88
    delta = 0.12
    
    # data
    # source = 'azelev_test.csv'
    source = 'azelev_test_720561600_723081600.csv'
    source = 'azelev_test_723085200_725608800.csv'
    source = 'azelev_test_725612400.csv'
    
    df = pd.read_csv(source)            
    df = df.sort_values(df.columns[0]) # sort data based on ascending first column
    
    xp = df.iloc[:,0]
    yp = df.iloc[:,1]
    zp = df.iloc[:,2]
    
    # run main
    x,y,z = main(xmin,xmax,delta,xp,yp,zp)
    print(x)
    print(y)
    print(z)
    
    Z = np.array([x,y,z])
    dfo = pd.DataFrame(data=np.transpose(Z),columns=['Azimuth','Elevation','ET'])
    
    output = source + '_interpolated.csv'
    dfo.to_csv(output,index=None,header=True)
    
    # plot for just testing
    plt.plot(x,y,'ro')
    plt.show()