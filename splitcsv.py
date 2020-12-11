# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 19:20:23 2020
@modified: 14 JULY 2020
@author: Shen Ge

"""
import pandas as pd

# ensure that all numbers are already positive
start = 0
delta = 3
end = 360


df = pd.read_csv('reducedcraters1.4to1.7km.csv')
df = pd.read_csv('reducedcraters1.7to99km.csv')
df = pd.read_csv('reducedcraters0.5to1.4km.csv')

df = df.sort_values(by=['LON'])


# if longitude < 0 degrees, then add 360 degrees to the longitude value
#df[df['LON']<0]['LON'] = df[df['LON']<0]['LON']+360
df.loc[df['LON']<0,'LON'] = df['LON'] + 360
print(df)

df = df.sort_values(by=['LON'])

dflon = df['LON']

valrowpos = start
while valrowpos < end:
    dfsegment = df[dflon.between(valrowpos,valrowpos+delta)]   
    
    if dfsegment.empty is False:
        print(dfsegment)
        valname = str(valrowpos) + '.csv'
        if valrowpos < 10:
            valname = '00' + str(valrowpos) + '.csv'
        elif valrowpos < 100:
            valname = '0' + str(valrowpos) + '.csv'
        
        dfsegment.to_csv(valname,index=False)
    else:                
        print('No value for range from ' + str(valrowpos) + ' to ' + str(valrowpos+delta) + '!')
#        print('Not generating csv.')
    valrowpos+=delta