"""
Created on 1 OCT 2021
@author: Shen Ge
@name: CSV File Comparer
@description:
    Compares two different csv files and calculates statistical differences
    Enhanced version can also do extra computations if you know what the
    type of data is, e.g. compare lat/lons and calculate delta distances between them
"""
import sys, os
import numpy as np
import pandas as pd

# user defined library
from gis import *
if __name__ == "__main__":
    print('Ready to compare!')
    try:
        file1 = sys.argv[1]
    except:
        file1 = input('Input path of first csv file: ')

    try:
        file2 = sys.argv[2]
    except:
        file2 = input('Input path of second csv file: ')

    try:
        outfile = sys.argv[3]
    except:
        outfile = input('Enter path of output file: ')

    try:
        df1 = pd.read_csv(file1)
    except:
        print('Could not find first file.')
        sys.exit(2)

    try:
        df2 = pd.read_csv(file2)
    except:
        print('Could not find second file.')
        sys.exit(2)

    print('Example of column input 1, 2, 3, 4, 5, 6')
    print('Note column 0 is actually the first column.')
    cols = ''
    while len(cols) < 1:
        cols = input('Enter columns to compare with a comma between each one: ')

    columns = [int(x) for x in cols.split(',')]
    dfd = df1.iloc[:,columns] - df2.iloc[:,columns]
    print(dfd)
    dfd = dfd.dropna()

    #%% now comes the fun part of actually doing some calculations if desired
    # comment out following as needed
    delta_dist = [calcDist(lat1,lon1,lat2,lon2) for lat1,lon1,lat2,lon2 in zip(df1['lat'],df1['lon'],df2['lat'],df2['lon'])]
    dfd['delta_dist (m)'] = delta_dist

    dfd['Image'] = df1['Image']

    # save the difference file
    dfd.to_csv(outfile,index='None')
    descriptions = dfd.describe()
    descriptions.to_csv(outfile[:-3]+'_stats.csv',index='None')
