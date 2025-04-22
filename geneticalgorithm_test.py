# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 20:36:40 2025

@author: Shen Ge
@name: Genetic Algorithm Tester
"""

import numpy as np
import random

def f(x):
    return np.sin(np.pi * x / 256)

def gen_random(n=8):
    return ''.join(str(random.randint(0, 1)) for _ in range(n))

def populate(n=8,m=8):
    population = ['']*n
    i = 0
    while i < n:
        population[i] = gen_random(m)
        i+=1
    return population

def calc_decimal(population):
    population_dec = np.zeros(len(population))
    for i,element in enumerate(population):
        population_dec[i] = int(element,2) # convert to decimal
    return population_dec

def calc_fitness(population):
    fitness = np.zeros(len(population))
    for i,element in enumerate(population):
        element_dec= int(element,2) # convert to decimal
        fitness[i] = f(element_dec)
    return fitness

def calc_fnorm(population):
    fitness = calc_fitness(population)
    return fitness / sum(fitness)


#%%
if __name__ == '__main__':
    print('''Genetic Algorithm Tester
    Find an x that maximizes the function f(x) = sin(pi * x / 256)
    where x is an integer between 0 and 255
    
    The answer done analytically is obviously x = 128 which leads to 
    f(x) = sin(pi/2) = 1
    
    We want to do it by using genetic algorithms with random guesses
    ''')    
#    num_binary = gen_random(8)    
#    num_decima = int(num_binary,2)
    
    population = populate(4,8)
#    fitness    = calc_fitness(population)
    f_norm     = calc_fnorm(population)
    