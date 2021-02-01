"""
Created on Sat Oct  5 18:19:48 2019
@author: Shen Ge 

Calculates word frequency from a text file

NOTE:
This is part of the learn-as-we-go series with many comments to help a newbie programmer understand what's happening.
https://developers.google.com/edu/python/dict-files
https://www.pythoncentral.io/how-to-sort-python-dictionaries-by-key-or-value/
https://thomas-cokelaer.info/tutorials/python/dicts.html
"""


import re
import string

# Python's efficient key/value hash table structure is called a "dict". 
# The dict (dictionary) class object in Python is a very versatile and useful container type, able to store a collection of values and retrieve them via keys.
# The values can be objects of any type (dictionaries can even be nested with other dictionaries) and the keys can be any object so long as it's hashable, 
# meaning basically that it is immutable (so strings are not the only valid keys, but mutable objects like lists can never be used as keys). 
# The contents of a dict can be written as a series of key:value pairs within braces { }, e.g. dict = {key1:value1, key2:value2, ... }. 
# The "empty dict" is just an empty pair of curly braces {}.
frequency = {}

document_text = open('test.txt', 'r')
text_string = document_text.read().lower()
match_pattern = re.findall(r'\b[a-z]{4,15}\b', text_string)
 
for word in match_pattern:
    # The string field is unique, so that is the key of the dictionary.
	count = frequency.get(word,0)
	frequency[word] = count + 1
    
# filter out the frequency dictionary to only items greater than a certain word count
frequency = dict((k, v) for k, v in frequency.items() if v >= 1)

frequency_list = frequency.keys()
 
## Common case -- loop over the values in sorted order accessing each key/value
for words in sorted(frequency_list, key=frequency.get, reverse=True):
	print(words, frequency[words])
