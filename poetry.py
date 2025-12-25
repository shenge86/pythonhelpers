# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 19:40:42 2025

@author: sheng
@name: Generates random poetry
"""
import os, sys
import pickle
from datetime import datetime
from wonderwords import RandomWord, RandomSentence

if __name__ == '__main__':
    print('Please use -load in command line argument to load existing!')
    file_path = 'words.pkl'
    if '-load' in sys.argv:
        with open(file_path, 'rb') as file:
            words = pickle.load(file)
        print('Words loaded: ', words)
    else:        
        w = RandomWord()
        word_start = w.word()            
        adjective1 = w.word(include_categories=["adjective"])
        noun1      = w.word(include_categories=["noun"])
        verb1      = w.word(include_categories=["verb"])
    
        loc_start  = w.filter(word_min_length=4, starts_with="loc")
        
        others     = [word_start] + loc_start
                
        # custom types
        humans  = ["Shen", "human", "woman", "supermodel", "physicist", "gym rat"]
        sexuals = ["kiss", "fondle", "slap", "grasp", "penetrate", "fuck", "suck", "grope", "massage", "make love with"]
        fruits  = ["apple", "orange", "banana", "strawberry"]
        generator = RandomWord(fruit=fruits, sexual=sexuals, human=humans)        
        
        # random sentences
        s = RandomSentence()
        sentences = []
        sentences.append(s.bare_bone_sentence())
        sentences.append(s.simple_sentence())
        sentences.append(s.sentence())
        
        line_manual = 'A ' + generator.word(include_categories=['human']) + ' loves to ' + generator.word(include_categories=['sexual']) + ' ' + generator.word(include_categories=['fruit'])        
        
        sentences.append(line_manual)
        
        
        words = {
            'adjectives': [adjective1],
            'nouns': [noun1],
            'verbs': [verb1],            
            'others': others,
            'sentences': sentences,
            }
    #%%            
    result = ' '.join([words['adjectives'][0], words['nouns'][0], words['verbs'][0]])
    result2 = ' '.join([words['others'][1], words['others'][2]])
    
    
    lines_to_save = [
        words['others'][0]+'\n',
        '----------------'+'\n',
        result.capitalize()+'\n',
        result2.capitalize()+'\n',
        words['sentences'][0]+'\n',
        words['sentences'][1]+'\n',
        words['sentences'][2]+'\n',
        words['sentences'][3]+'\n',
        '=======================',
        ]
    
    for line in lines_to_save:
        print(line)

    os.makedirs('poetry', exist_ok=True)    
    current_datetime = datetime.now()
    filename = current_datetime.strftime("%Y-%m-%d_%H-%M-%S.%f") + ".txt"
    filepath = 'poetry/' + filename
    
    with open(filepath, 'w') as f:
        f.writelines(lines_to_save)
        
    #%%
    print('Word database saved: ', words)
    with open(file_path, 'wb') as file:
        pickle.dump(words, file)
        
    print(f'Words have been saved to {file_path}')