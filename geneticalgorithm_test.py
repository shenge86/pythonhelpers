# -*- coding: utf-8 -*-
"""
Created on Mon Apr 21 20:36:40 2025

@author: Shen Ge
@name: Genetic Algorithm Tester

This simple tester is supposed to solve for a maximum of a mathematical function
based on genetic algorithms.
"""

import sys

import numpy as np
import random
import bisect

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

def cumulative_sum_list(original_list,highest=True,lowest=False):
    cumulative_list = []
    current_sum = 0    
    for num in original_list:
        cumulative_list.append(current_sum)
        current_sum += num
        
    print(current_sum)
    # add in the final number
    if highest:
        cumulative_list.append(1)
        
    # remove initial 0
    if not lowest:
        cumulative_list.pop(0)
    return cumulative_list

def find_element_between_values(ordered_list, target_number):
       """
       Finds the element in an ordered list where a target number falls between.

       Args:
           ordered_list: A sorted list of numbers.
           target_number: The number to check.

       Returns:
           The element in the list where the target number falls between, or None if no such element is found.
       """

       insertion_point = bisect.bisect_left(ordered_list, target_number)

       if 0 <= insertion_point < len(ordered_list):
           return ordered_list[insertion_point]

       return None


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
    
    # generate a population of n samples, each that is an 8-bit string
    # 8-bit string since it can represent all numbers between 0 and 255
    n = 8
    population = populate(n,8)
    print('Generated a population of size: ', n)
    print('Population: ', population)
    
#    fitness    = calc_fitness(population)
    f_norm     = calc_fnorm(population)
    f_norm_cum = cumulative_sum_list(f_norm)
    
    # Generate 8 random numbers from 0 to 1
    random_numbers = [random.random() for _ in range(8)]
    
    #%% See how these 8 numbers fit into the bucket for each fitness score
    # Example if assuming cumulative fnorm associated with members 1 through 8 is:
    # 0.144
    # 0.237
    # 0.421
    # 0.469
    # 0.635
    # 0.790
    # 0.872
    # 1.000
    # if random number is 0.05, then 1 is chosen
    # if random number is 0.7, then 6 is chosen
    # if random number is 0.9, then 8 is chosen
    elements = []
    for r in random_numbers:
        index = bisect.bisect(f_norm_cum, r)
        elements.append(index)