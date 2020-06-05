# -*- coding: utf-8 -*-
"""
Created on Wed May  6 17:22:13 2020
@modified: 3 JUNE 2020
@author: Shen Ge
@name: csv / excel reducer
@description: 
    Reduce data based on some criteria. This can be used on its own from command line.
    Note certain functions cannot be called form command line. Please import from different script and use these functions instead.
"""
import sys, getopt

import pandas as pd
#import pyarrow
import numpy as np

# import watch

######## DATA I/O FUNCTIONS ##########
def readdata(source,numrows=None):
    """Reads in a csv, parquet, msgpack, hdf5 or feather file containing rows of data    
    :param source: the pathname of the data file (string)
    :param numrows: number of rows to read in. Note: optional and only used with csv files (int)
    :return: rows of data
    :rtype: dataframes
    """    
    
    if (source[-8:]==".parquet"):
        print("Reading in parquet file...")
        df = pd.read_parquet(source)
    elif (source[-4:] == ".csv"):
        print("Reading in csv file...")
        if numrows is None:
            try:
                df = pd.read_csv(source)
            except (IOError, OSError) as e:
                print(e.errno)
                print("Sorry, Mr. User. Try to be a little more careful. \nTypos are understandable. Please check your .csv file name or path.")
                sys.exit(1)
        else:
            try:
                df = pd.read_csv(source,nrows=numrows)
            except (IOError, OSError) as e:
                print(e.errno)
                print("Sorry, Mr. User. Try to be a little more careful. \nTypos are understandable. Please check your .csv file name or path.")
                sys.exit(1)
    elif (source[-8:]==".msgpack"):
        print("Reading in msgpack file...")
        try:
            df = pd.read_msgpack(source)
        except (IOError,OSError):
            print("Sorry, Mr. User. Try to be a little more careful. \nTypos are understandable. Please check your .msgpack file name or path.")
            sys.exit(1)
    elif (source[-3:]==".h5"):
        print("Reading in hdf5 file...")
        try:
            df = pd.read_hdf(source,'table')
        except (IOError,OSError):
            print("Sorry, Mr. User. Try to be a little more careful. \nTypos are understandable. Please check your .h5 file name or path.")
            sys.exit(1)
    elif (source[-8:]==".feather"):
        print("Reading in feather file...")
        try:
            df = pd.read_feather(source)
        except (IOError,OSError):
            print("Sorry, Mr. User. Try to be a little more careful. \nTypos are understandable. Please check your .feather file name or path.")
            sys.exit(1)
    else:
        print("Invalid file. Please input parquet, csv, msgpack, hdf or feather file.")
        sys.exit(1)
        
    # memory_usage_pandas(df)
#    print(df)
    return df

def savedata(df,source):
    """Saves pandas dataframe in an output file
    Default outputfile (known as source parameter) is of .csv
    Will autosave file as other formats if the extension is as such:
        .parquet > Parquet file
        .csv > csv file
        .msgpack > msgpack file
        .h5 > hdf5 file
        .feather > feather file        
    """
    if (source[-8:]==".parquet"):
        print("Writing to parquet file...")
        df.to_parquet(source)
    elif (source[-8:]==".msgpack"):
        print("Writing to msgpack file...")
        df.to_msgpack(source)
    elif (source[-3:]==".h5"):
        print("Writing to hdf5 file...")
        df.to_hdf(source,'table')
    elif (source[-8:]==".feather"):
        print("Writing to feather file...")
        df.to_feather(source)
    else:
        df.to_csv(source)
    
    print("Data saved as ", source)

def read_console_arguments(argv):    
    input_file = ''
    output_file = 'output.csv'
    nrows = 10        
    mcols = None
    mmax = [9e6]
    mmin = [-9e6]
    
    msgstring = 'reduceexcel.py -i <inputfile> -o <outputfile> -n <numberofrows> -m <columnstotake> --mmax <maxcolvalues> --mmin <mincolvalues> \n'
    
    try:
        opts, args = getopt.getopt(argv,"hi:o:n:m:",["ifile=","ofile=","nrows=","mcols=","mmax=","mmin="])
    except getopt.GetoptError:
        print('Invalid arguments! Use format as follows: \n')
        print(msgstring)
        print('Type reduceexcel.py -h for help.')
        sys.exit(2)
        
    if len(opts) < 1:
        print('You must put in an input filename.')
        print(msgstring)
        print('Type reduceexcel.py -h for help.')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print(msgstring)
            print("<colstointake> are the columns to intake. Only intakes integer values with each number separated by a comma with no spaces. e.g. [1,2,5]")
            print("<maxcolvalues> are the largest values in the columns to intake non-inclusive.")
            print("<mincolvalues> are the smallest values in the columns to intake non-inclusive.")
            print("Default output file is named output.csv")
            sys.exit(0)
        elif opt in ("-i", "--ifile"):
            input_file = arg            
        elif opt in ("-o","--ofile"):
            output_file = arg
        elif opt in ("-n","--nrows"):
            nrows = int(arg)
        elif opt in ("-m","--mcols"):
#            print(arg)
            mcols = list(map(int, arg.strip('[]').split(',')))
        elif opt in ("--mmax"):
#            print(arg)            
            mmax = list(map(float, arg.strip('[]').split(',')))            
#            print(arg)
        elif opt in ("--mmin"):
#            print(arg)
            mmin = list(map(float, arg.strip('[]').split(',')))
            
    print("Input file: ", input_file)
    print("Output file: ", output_file)
    print("Number of rows to read in: ", nrows)    
    print("Columns to read in: ", mcols)
    print("Max bound of column values: ", mmax)
    print("Min bound of column values: ", mmin)
    return input_file, output_file, nrows, mcols, mmax, mmin


######## DATA REDUCTION FUNCTIONS ##########
def filtercols(df,mcols,mthres,ttype=0):
    """Extracts only relevant columns and removes rows of floats & ints that fall outside of thresholds.
    :param df: data (dataframe)
    :param mcols: columns to take from data (list of floats)
    :param mthres: thresholds for the respective columns (list of floats)
    :param ttype: type of threshold defined as such:
        0 means mthres defines minimum bounds (default)
        1 means mthres defines maximum bounds
    :return dfr: reduced df with defined thresholds and selective columns
    """
    # reduce down the columns
    dfr = df.iloc[:,mcols]
#    print(df)    
    
    # reduce rows that fall below thresholds defined for each column
    for x in range(len(mcols)):
        if ttype == 1:
            # ignore if the dtype is not a float or int
            if np.issubdtype(dfr.iloc[:,x].dtype, np.number):
                dfr = dfr[dfr.iloc[:,x] < mthres[x]]
                print("Maximum: ")
        else:
            if np.issubdtype(dfr.iloc[:,x].dtype, np.number):
                dfr = dfr[dfr.iloc[:,x] > mthres[x]]
                print("Minimum: ")

        print("Reduced data: ")
        print(mthres[x])
        print(dfr)
    
    return dfr

def splitter(df,idxcol,valrow,delrow):
    """Splits dataframe into smaller dataframes dependent on row val threshold. Recursive function."""
    try:
        print(df.iloc[0,idxcol])
    except:
        print("End of file!")
        return df
        
    if df.iloc[0,idxcol] > valrow:
        print("VALROW: ", valrow)
        dfc = df[df.iloc[:,idxcol].between(valrow,valrow+delrow)]
        df = df[~df.iloc[:,idxcol].between(valrow,valrow+delrow)]
        print(dfc)
        
        ### for specialized case. comment out if not needed:
        if valrow < 0:
            valrowpos = valrow + 360
        else:
            valrowpos = valrow
        
        valname = str(valrowpos) + '.csv'
        if valrowpos < 10:
            valname = '00' + str(valrowpos) + '.csv'
        elif valrowpos < 100:
            valname = '0' + str(valrowpos) + '.csv'
        
        ###
        
        # save data
#         valname = str(valrowpos) + '.csv'
        savedata(dfc,valname)
        
        # increment to next in-between value
        valrow += delrow
        splitter(df,idxcol,valrow,delrow)
    return df

def combinecsv(csv1,csv2,outputcsv):
    """Combine two csv files into one. Remove duplicates."""
    df1 = readdata(csv1)
    df2 = readdata(csv2)
    
    full_df = pd.concat([df1,df2])
    df12 = full_df.drop_duplicates(keep='last')
    
    savedata(df12,outputcsv)
    return df12

######## MAIN FUNCTION ##########
def main(argv):
    input_file, output_file, nrows, mcols, mmax, mmin = read_console_arguments(argv)    
    mmax = mmax*len(mcols)
    mmin = mmin*len(mcols)

    # read in data and convert to pandas dataframe
    df = readdata(input_file,nrows)
#    print(df.iloc[:,[1,2]])
    # just take all columns if no argument for mcols
    if mcols is None:
        mcols = list(range(1,len(df.columns)))
#        print(mcols)
    
    # do data reduction on imported pandas dataframe
    
    # max thresholds for every single column    
    dfr = filtercols(df,mcols,mmax,1)
    
    # min thresholds
    mcols = list(range(0,len(dfr.columns)))
    dfr = filtercols(dfr,mcols,mmin,0)
    
    # save reduced pandas dataframe as an xls, csv or whatnot
    savedata(dfr,output_file)


if __name__ == "__main__":
    print("Starting!")
    # possible files:
    main(sys.argv[1:])
    sys.exit(0)