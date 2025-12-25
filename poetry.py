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
        # TYPE 1
        humans  = ["Shen", "human", "man", "woman", "supermodel", "physicist", "gym rat"]
        sexuals = ["kiss", "fondle", "slap", "grasp", "penetrate", "fuck", "suck", "grope", "massage", "make love with"]
        fruits  = ["apple", "orange", "banana", "strawberry"]
        generator = RandomWord(fruit=fruits, sexual=sexuals, human=humans)
        
        
        # TYPE 2
        bodyparts = ['body',
                     'breast',
                     'butt'
                     'eyes',
                     'face',
                     'hair',
                     'legs',
                     'nipples',
                     'pussy']
        
        models = ['Allie Haze',
                  'Camryn',
                  'Ceara Lynch',
                  'Emma Kuziara', 
                  'Leanna Lovings',
                  'Lexi Belle',
                  'Melanie Rios']
        
        actions= ['eyeballing',                  
                  'imagining making love to',
                  'pleasuring oneself to',
                  'salivating over',
                  'watching',
                  'worshiping']
        
        generator_x = RandomWord(bodypart=bodyparts, model=models, action=actions)
        
        # TYPE 3
        times = ['eternal',
                 'infinite',
                 'long'
                 'short',
                 'temporal',
                 'temporary',]
        
        generator_time = RandomWord(time=times)
        
        # random sentences
        s = RandomSentence()
        sentences = []
        sentences.append(s.bare_bone_sentence())
        sentences.append(s.simple_sentence())
        sentences.append(s.sentence())
        
        line000 = 'The lines above are mechanically created with uncuration except in adjective, verb and noun formation'
        line001 = 'What follows is more deliberate.'
        line01 = 'A ' + generator.word(include_categories=['human']) + ' loves to ' + generator.word(include_categories=['sexual']) + ' ' + generator.word(include_categories=['fruit'])        
        line02 = f"Yet, to a {generator.word(include_categories=['human'])}, nothing feels quite as good as spending hours"
        line03 = 'staring at a screen and ' + generator_x.word(include_categories=['action']) + ' the ' + generator_x.word(include_categories=['bodypart']) + ' of ' + generator_x.word(include_categories=['model'])
        line04 = 'The euphoria may be ' + generator_time.word() + ' and the shame may be ' + generator_time.word()
        line05 = 'The cycle repeats...'
        
        sentences.append(line000)
        sentences.append(line001)
        sentences.append(line01)
        sentences.append(line02)
        sentences.append(line03)
        sentences.append(line04)
        sentences.append(line05)
        
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
        words['others'][0],
        '----------------'+'\n',
        result.capitalize()+'\n',
        result2.capitalize()+'\n',
        ]
    
    lines_to_save2 = []
    for sentence in words['sentences']:
        lines_to_save2.append(sentence+'\n')
    
    lines_to_save.extend(lines_to_save2)    
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