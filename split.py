#!/usr/bin/python3
import sys
import os

import pandas as pd

inputfile = input('Enter input file: ')
try:
    df = pd.read_csv(inputfile)
except FileNotFoundError:
    print('File not found! Let us use one as an example: ')
    df = pd.read_csv('https://www1.ncdc.noaa.gov/pub/data/cdo/samples/PRECIP_HLY_sample_csv.csv')
except:
    print('Not a valid csv file for ingestion.')
    print('Using sample noaa data.')
    df = pd.read_csv('https://www1.ncdc.noaa.gov/pub/data/cdo/samples/PRECIP_HLY_sample_csv.csv')


directory = input('Enter directory to which to place the files: ')
# Check whether the specified path exists or not
isExist = os.path.exists(directory)
if not isExist:
  os.makedirs(directory)
  print("Directory not found. Made directory.")

print('Options for column headers. Please choose one of the following:')
for key in df.keys():
    print(key)
groupname = input('Enter the column header to which you wish to sort: ')


# if you did not enter a column name in the list or you didn't enter anything
if groupname not in df.keys() or groupname == '':
    groupname = df.keys()[0]
    print('Your inputted header was not found. Assuming the first column name: ')
    print(groupname)

for group, dataframe in df.groupby(groupname):
    dataframe.to_csv(f'{directory}/coords_{group}.csv',index=False)

print('COMPLETE!')
print('=========================================')
