# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 10:49:51 2021

@author: Shen Ge
@name: Union Parser
"""

def overlap(a0,af,b0,bf):
    '''Finds overlap between two intervals.
    Intervals are defined by 2 numbers - start and end'''
    if (b0>af or a0>bf):
        return None
    else:
        c0,cf = max(a0,b0),min(af,bf)
    return c0,cf


def union(a0,af,b0,bf):
    '''Gets union of 2 intervals assuming that they intersect!'''
    if overlap(a0,af,b0,bf) is not None:
        c0,cf = min(a0,b0),max(af,bf)
        return c0,cf
    else:
        return None

def union_arr(et_start,et_end):
    '''Gets union of an array of intervals assuming they intersect!'''
    j=0 # et_interval index
    try:        
        c0,cf = union(et_start[0],et_end[0],et_start[1],et_end[1])         
    except:
        j+=1
        c0,cf = et_start[0],et_end[0]
    et_interval = [(c0,cf)]
        
    for i in range(len(et_start)-2):
        i+=1
        print('Index #: ', i)
        print('Interval: ', j)
        print('et_start: ', et_start[i])
        print('Union:')
        try:
            c0,cf = union(c0,cf,et_start[i+1],et_end[i+1])
            et_interval[j] = c0,cf
        except:
            # No union. Append to interval index and step into new interval start time
            j+=1
            et_interval.append((et_start[i+1],et_end[i+1]))
            c0,cf = et_start[i+1],et_end[i+1]
            print('No union. Updated c0,cf: ', (c0,cf))
        print(c0,cf)
    return et_interval

def verbosity(func):
    info = func(et_start,et_end)
    print('STARTING AND ENDING TIMES:')
    print(et_start)
    print(et_end)
    print('UNION:')
    print(info)
    print('END SCRIPT')

if __name__ == '__main__':    
    #%%
    print('===========')
    et_start = [0,5,10,12,14,16,30,40]
    et_end = [10,8,11,15,19,20,35,47]    
    et_interval = union_arr(et_start,et_end)
    verbosity(union_arr)