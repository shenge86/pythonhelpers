# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 19:23:22 2021

@author: Shen Ge
@name: 
@description:
    Reads in csv file and filters out data based on limits in criteria of certain column(s)
"""
import sys

import pandas as pd
import numpy as np


if __name__ == '__main__':
    source = 'input.csv'
    try:
        df = pd.read_csv(source)
    except (IOError, OSError) as e:
        print(e.errno)
        print("Sorry, Mr. User. Try to be a little more careful. \nTypos are understandable. Please check your .csv file name or path.")
        sys.exit(1)

    