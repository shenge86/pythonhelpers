# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 12:16:59 2021

@author: sheng
"""
import sys
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

def getOnline(url):
    # only if requesting url from online
    #req = Request("https://en.wikipedia.org/wiki/Python_(programming_language)")
    req = Request(url)
    html_page = urlopen(req)
    return html_page


def parse(html_page):
    soup = BeautifulSoup(html_page, "html.parser")
    
    html_text = soup.get_text()
    
    f = open("html_text.txt", "w")         # Creating html_text.txt File
    
    for line in html_text:
    	f.write(line)
    
    f.close()
    return html_text
    
def parselocal(html_page):
    file = open(html_page,'r',encoding='utf8')
    soup = BeautifulSoup(file,'html.parser')
    html_text = soup.get_text()
    return soup, html_text

if __name__ == '__main__':
    
    default = 'default.html'
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        try:
            print('Trying to get url online')
            html_page = getOnline(url)
            print("Loaded in: ", html_page)
            parse(html_page)
        except:
            print('Failed! Trying to get local file.')
            html_page = default
    else:
        print('No argument inputted. Assuming default html_page')
        html_page = default
    
    # local file
    print("Loaded in: ", html_page)
    soup, html_text = parselocal(html_page)
    
    info = soup.find_all("script")