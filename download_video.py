# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 11:26:01 2021

@author: Shen Ge
@name: downloads videos
"""

import requests
import sys

def downloadfile(name,url):
    name=name+".mp4"
    r=requests.get('url')
    print("****Connected****")
    f=open(name,'wb')
    
    print("Downloading.....")
    for chunk in r.iter_content(chunk_size=255): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    print(f'Downloaded {url} to {name}')
    f.close()

def downloadFile(AFileName):
    # extract file name from AFileName
    #filename = AFileName.split("/")[-1] 
    filename = AFileName.split("/")[-1].split("mp4")[0]+'mp4'
    #filename = 'download.mp4'
    print(filename)
    
    # download image using GET
    rawImage = requests.get(AFileName, stream=True)
    
    # check successful
    if (rawImage.status_code != 200):
        print('Error! Did not acquire URL')
        print(rawImage.status_code)
        sys.exit(2)
    
    # save the image recieved into the file
    with open(filename, 'wb') as fd:
        fd.write(rawImage.content)
        
        # alternative method
        # for chunk in rawImage.iter_content(chunk_size=1024):
        #     print(chunk)
        #     fd.write(chunk)
            
    return

def downloadFileURLLIB(url):
    # imported the urllib library
    import urllib
    
    filename = url.split("/")[-1].split("mp4")[0]+'mp4'
    #filename = 'download.mp4'    
     
    # Copy a network object to a local file
    urllib.request.urlretrieve(url, filename)
    return

def message(name):
    print('python download_video.py <url>')

if __name__ == '__main__':
    args = sys.argv[1:]
    
    if len(args) < 1:
        print('You must input an URL')        
        sys.exit(2)
    else:
        url = args[0]
        
    try:
        print('Trying with request')
        downloadFile(url)
    except:
        print('Failed! Trying with URLLib')
        downloadFileURLLIB(url)