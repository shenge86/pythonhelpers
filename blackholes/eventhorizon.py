# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 18:35:35 2023

@author: Shen
@name: Schwarzschild Radius calculator and other calcs
"""
import sys

#%% Calculate event horizon radius
# gravitational constant
G = 6.67e-11 # N*m^2/kg^2

# speed of light
c = 3e8 # m/s^2

# solar mass in kilograms
Msun = 2e30 # kg

# mass
try:
    M = sys.argv[1]
    M = float(M)
except:
    M = input('Enter mass of object in solar masses: ')
    M = float(M)

M *= Msun

# calculate event horizon
R_eventhorizon = 2*M*G/(c**2)
print('Event horizon radius (m): ', R_eventhorizon)
print('Event horizon radius in kilometers: ', R_eventhorizon/1000)

#%% Calculate tidal force
# length of the object or person
try:
    d = sys.argv[2]
    d = float(d)
except:
    d = input('Enter length of person (or object) in meters: ')
    d = float(d)

R = input('Enter distance away from singularity (km): ')
R = float(R)

a = 2*G*M*d/(R**3)
print('Acceleration (m/s^2): ', a)
print('Acceleration in number of Earth g: ', a/9.8)
