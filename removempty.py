# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 22:20:58 2020

@author: Shen Ge
@name: remove csv empty rows
@description: 
    Simple command line script to remove empty rows from a csv file and save as a csv file with all empty rows removed.

"""
import sys
import pandas as pd

def main(src,output):    
    df = pd.read_csv(src)  # Create a Dataframe from CSV
    
    # Drop rows with any empty cells
    df.dropna(
        axis=0,
        how='any',
        thresh=None,
        subset=None,
        inplace=True
    )
        
    df.to_csv(output)    
    return output

def mainarg(argv):
    print("Removing empty rows...")
    msg = "python removempty.py <input.csv> <output.csv>"
    if len(argv) != 2:
        print("You must input 2 arguments: 1 for the input csv file and 1 for the output csv file.")
        print(msg)
        sys.exit(2)
    
    src = argv[0]
    output = argv[1]
    
    out = main(src,output)
    print("Data saved as", out)
    
    return


if __name__ == "__main__":    
    mainarg(sys.argv[1:])
    sys.exit(0)