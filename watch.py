# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 23:34:12 2020
@last modified: 29 APR 2020

@author: sheng
@description:
    A bunch of process checking functions
    Can be used with any other Python script by import
"""

import os
import psutil
import gc
import time
from time import process_time
import sys

import pandas as pd
import numpy as np


#logging.debug("debug") 
#logging.info("info") 
#logging.warning("warning") 
#logging.error("error")
#logging.critical("critical")

##### SYSTEM PERFORMANCE TESTING FUNCTIONS ######
def follow(thefile):
    thefile.seek(0,2) # Go to the end of the file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1) # Sleep briefly
            continue
        yield line


##### SYSTEM PERFORMANCE TESTING FUNCTIONS ######
def memory_usage_psutil():
    """return the memory usage of the process in MB"""
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)
    print("Memory usage of process in MB: ", mem)
    return mem

def memory_usage_pandas(df):
    """returns pandas dataframe memory usage in MB"""
    mem = df.memory_usage(index=True,deep=True).sum()
    print("---------------------------------------------------------------------------------------------")
    print("Memory usage of loading csv, parquet, msgpack or hdf file into pandas dataframe in MB: ", mem/8e6)
    print("---------------------------------------------------------------------------------------------")
    return mem

        
if __name__=="__main__":
    thefile = 'stuff.log'
    # line = follow(thefile)
    # print(line)
    
    file = open(thefile,'r')
    while 1:
        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(1)
            file.seek(where)
        else:
            print(line) # already has newline