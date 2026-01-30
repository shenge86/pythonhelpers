# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 23:12:35 2026

@author: sheng
@name: Markov Chain 
    
@description:
    A politician campaigns on a long east-west chain of islands33. At the end of each day she decides to stay on her current island, move to the island to the east, 
    or move to the island to the west. Her goal is to visit all the islands proportional to their population, so that she spends the most days on the most populated island,
    and proportionally fewer days on less populated islands. But, 
    
    (1) she doesn’t know how many islands there are, and 
    (2) she doesn’t know the population of each island. 
    
    However, when she visits an island she can determine its population. And she can send a scout to the east/west adjacent islands to determine their population before visiting.
    How can the politician achieve her goal in the long run?
    
    Suppose that every day, the politician makes her travel plans according to the following algorithm.

    She flips a fair coin to propose travel to the island to the east (heads) or west (tails). (If there is no island to the east/west, treat it as an island with population zero below.)
    If the proposed island has a population greater than that of the current island, then she travels to the proposed island.
    If the proposed island has a population less than that of the current island, then:

    She computes  
    a
    ,the ratio of the population of the proposed island to the current island.
    
    She travels to the proposed island with probability  
    a
    ,
    
    And with probability  
    1 − a
    she spends another day on the current island.
    
@references:
    https://bookdown.org/kevin_davisross/bayesian-reasoning-and-methods/mcmc.html
"""

