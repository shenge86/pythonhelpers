# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 20:04:57 2020

@author: Shen Ge
@name: Extract Data
@description: 
    Extracts data from a text file with defined markers.
    Generally adaptable - nimble and small.
    Main shows an example
"""
def extract_basic(identifiers,delimiter,file_name,output):
    '''Extracts every line with identifiers after the identifier word.'''
    i=0
    with open(file_name,mode='r') as file, \
        open(output,mode='w') as out_file:
    
      string = '#,'+','.join(identifiers)+'\n'
      out_file.write(string)
      
      for fovstr in file:
          for identifier in identifiers:
              if fovstr.find(identifier) != -1:
                  i+=1
                  data = fovstr.split(delimiter)[1][:-1]
                  print(f'{i},{data}')
                  out_file.write(f'{i},{data}\n')

def extract_lines(identifier,delimiter,headers,numlines,file_name,output,timecalc=False):
    i=0
    with open(file_name,mode='r') as file, open(output,mode='w') as out_file:
        string = '#,'+','.join(headers)+'\n'
        out_file.write(string)
        #out_file.write('#,Phase,Start,End,Duration(s)\n')
        for fovstr in file:
            if fovstr.find(identifier)!=-1:
                i+=1
                data[0]=fovstr.split(delimiter)[1][:-1]
                string = f'{i},{data[0]}'
                
                for count,dat in enumerate(data[1:]):
                    nextline=next(file)
                    dat=nextline.split(delimiter)[1][:-1]
                    data[count+1]=dat
                    string+=f',{dat}'
                
                # if last read in line is seconds
                if timecalc:
                    hourminsec = convert(data[-1])
                    print(hourminsec)
                    string+=f',{hourminsec}'
                
                string+='\n'
                print(string)
                out_file.write(string)

### miscellaneous functions
def convert(seconds):
    seconds = float(seconds)
    min, sec = divmod(seconds,60)
    hour, min = divmod(min,60)
    day, hour = divmod(hour,24)
    if day != 0:
        return "%dd%d:%02d:%02d" % (day, hour, min, sec) 
    else:
        return "%02d:%02d:%02d" % (hour, min, sec) 

#%%
if __name__ == "__main__":    
    file_name = 'input.txt'    
    output = 'output.csv'
    
    # Define the identifiers. These are words that indicate these lines need to be extracted.
    identifiers = ['phase','start','end','period']
    delimiter = ':'
    
    #extract_basic(identifiers,delimiter,file_name,output)
    
    #%%
    identifier = 'phase'
    delimiter = ':'    
    numlines = 4
    headers = [identifier,'start','end','duration(s)','duration(hh:mm:ss)']
    data = 4*[0]
    
    extract_lines(identifier,delimiter,headers,numlines,file_name,output,timecalc=True)