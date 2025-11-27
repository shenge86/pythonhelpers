# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 17:11:17 2025

@author: sheng
@name: General Excel Parser
@description:
    
    Takes in an excel file and parses out particular entries
"""
import sys, os
from decimal import Decimal
import readline # probably unnecessray since we are going to use tkinter

import pandas as pd
import numpy as np

import tkinter as tk
from tkinter import filedialog

def select_file():
    root = tk.Tk()
    # 1. Temporarily force the root window to be topmost
    root.attributes('-topmost', True) 
    # 2. Hide the main window *after* setting topmost
    root.withdraw()  # Hide the main window
    
    # Define the allowed file types
    allowed_file_types = (
         ("Data Files (CSV, XLSX, XLSM)", "*.csv *.xlsx *.xlsm"),
         ("CSV Files", "*.csv"),
         ("Excel Files (XLSX)", "*.xlsx"),
         ("Excel Files (XLSM)", "*.xlsm"),
         ("All files", "*.*")
     )
    
    # 3. Open the dialog and link it to the parent
    file_path = filedialog.askopenfilename(
        parent=root, # explicitly set the parent
        title="Select a file",
        initialdir="./",
        filetypes=allowed_file_types        
    )
    
    # 4. Destroy the hidden root window after selection
    root.destroy()
    
    return file_path

#%%
if __name__ == '__main__':
    print('Parse out excel sheet...')
    # if len(sys.argv) > 2:
    #     file = sys.argv[1]
    # else:
    #     file = input('Enter the xlsx file path: ')

    # while not os.path.exists(file):
    #     print('File does not exist! Try again please.')
    #     file = input('Enter the xlsx file path: ')
    file_path = select_file()

    root, extension = os.path.splitext(file_path)

    #%%
    if extension.lower() in ['.xlsx', '.xlsm']:
        excel = pd.ExcelFile(file_path)
        num_sheets = len(excel.sheet_names)
    
        if num_sheets > 1:
            print(excel.sheet_names)
            name_sheet = input('Enter which sheet you should use: ')
    
        df  = pd.read_excel(excel, sheet_name = name_sheet)
    else:
        df = pd.read_csv(file_path)

    #%%
    # these configuration parameters can eventually be read from a config file (not hardcoded!!)
    # define the bounds of knowledge
    mincol = 0
    maxcol = 17
    
    headerrow = 0
    skiprows  = [0, 2]
    

    dff = df.iloc[:,mincol:maxcol]
    dff_filtered = dff.drop(skiprows)

    