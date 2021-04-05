# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 21:44:26 2021

@author: Shen Ge
@name: Date Time Replacer
@description:
    Replaces date time formats in a text file with another date time format.
    For instance, if a csv file has dates in the format of 20-Nov-2021 and you want it as Nov 20, 2021
    this code can do that for all the dates.

    Sure, you can use regex to do this but who has time to learn that?
"""
import sys
import re
from datetime import datetime

import pandas as pd

def conversion(datetime_str,dateform):
    '''Converts particular date time from one format to a date form
    param datatime_str: date time 
    param dateform: format of date time desired
    type datetime_new: string
    type dateform: int
    return: datetime_new: string
    '''
    if dateform == 1:
        print('Converting to form 1: MM-DD-YYYY')
        #print(datetime_str)
        #datetime_obj = datetime.strptime(datetime_str,"%m/%d/%y").date()
        #try:
        #    datetime_obj = datetime.strptime(datetime_str,"%m/%d/%y").date()
        #    datetime_new = datetime.strftime(datetime_obj,"%m-%d-%y")
        #except:
        #    datetime_new = datetime_str

    return datetime_new

if __name__ == "__main__":
    print("Date Time Manipulator")
    #filename = input("Text file input: ")
    #outname = input("Text file output: ")
    filename = 'date_input.txt'
    outname = 'data_output.txt'
    print('''Input desired output date format: 
    0. YYYY-MM-DD (e.g. 2020-10-15)
    1. MM-DD-YYYY (e.g. 10-15-2020)
    2. DD-MMM-YYYY (e.g. 15-OCT-2020)
    3. MMM DD, YYYY (e.g. OCT 15, 2020)
    4. MM/DD/YYYY (e.g. 10/15/2020)
    5. DD/MM/YYYY (e.g. 15/10/2020)
    ''')
    dateform = input("Date format: ")
    dateform = int(dateform)
    assert 0 <= dateform <= 5, "Must be one of the choices from 1 to 5"

    with open(filename,mode='r') as f, \
            open(outname,mode='w') as o:
        for line in f:
            line2 = line
            pattern = r"(\d{2})['-/|\\'](\d{2})['-/|\\'](\d{4})"
            matches = re.findall(pattern,line2)
            print(matches)

            if dateform == 1:
                for match in matches:
                    if int(match[0]) > 12 and int(match[1]) < 12:
                        print('First entry is greater than 12. Assuming that it is month.')
                        line2 = re.sub(pattern,r'\2-\1-\3',line2)
                        print(line2)
                    elif int(match[0]) < 12:
                        print('First entry is less than 12. Assuming that it is day.')
                        line2 = re.sub(pattern,r'\1-\2-\3',line2)
                        print(line2)
                    else:
                        print('Invalid datetime found.')
            elif dateform == 4:
                line2 = re.sub(pattern,r'\1/\2/\3',line2)

            o.write(line2)
        
