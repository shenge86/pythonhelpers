# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 21:44:26 2021

@author: sheng
@name: Distance and azimuth calculator
"""
import sys
import csv

import numpy as np


#%% GIS Math Functions
def calcDist(lat1,lon1,lat2,lon2,R=1737400):
    """Calculate distance between two lat and lons (inputted in degrees)
    note this is the points at sea level below each of the peaks and not the straight-line distance between the peaks
    # This is the method recommended for calculating short distances by Bob Chamberlain (rgc@jpl.nasa.gov) of Caltech and NASA's Jet Propulsion Laboratory as described on the U.S. Census Bureau Web site. 
    # This formula does not take into account the non-spheroidal (ellipsoidal) shape of the Earth. It will tend to overestimate trans-polar distances and underestimate trans-equatorial distances.
    # References: 
    # http://tchester.org/sgm/analysis/peaks/how_to_get_view_params.html
    # https://andrew.hedges.name/experiments/haversine/
    # https://cs.nyu.edu/visual/home/proj/tiger/gisfaq.html # detailed explanation of different calculation methods
    :param lat1: latitude of baseline coordinate (float)
    :param lon1: longitude of baseline coordinate (float)
    :param lat2: latitude of 2nd coordinate (float)
    :param lon2: longitude of 2nd coordinate (float)
    :param R: radius of spherical body; default is 1737400 meters which is that of moon used by LOLA / Kaguya data (float) 
    :return d: distance between the two coordinates (float)
    """
    lat1 = np.deg2rad(lat1)
    lon1 = np.deg2rad(lon1)
    lat2 = np.deg2rad(lat2)
    lon2 = np.deg2rad(lon2)
    dlon = lon2-lon1
    dlat = lat2-lat1

#    print(dlon)
#    print(dlat)
    a = np.sin(dlat/2)**2+np.cos(lat1)*np.cos(lat2)*(np.sin(dlon/2)**2)
#    c2 = 2*np.arcsin(np.min([1,np.sqrt(a)])) # http://tchester.org/sgm/analysis/peaks/how_to_get_view_params.html
    c = 2*np.arctan2(np.sqrt(a),np.sqrt(1-a)) # https://andrew.hedges.name/experiments/haversine/
    d = R*c
#    d2 = R*c2
#    print(d)
#    print(d2)
    return d

def calcAzimuth(lat1,lon1,lat2,lon2):
    """ returns azimuth angle (in degrees) of a coordinate with respect to baseline coordinate
    # References:
        https://www.igismap.com/formula-to-find-bearing-or-heading-angle-between-two-points-latitude-longitude/
    # Use for checking:
        https://www.omnicalculator.com/other/azimuth
    result is with respect to local azimuth frame 
    for instance, if original is 85S, 40E then along the 40E longitude is considered 0 degrees
    heading to 85S, 220E will give 180 degrees for azimuth angle
    calcAzimuth(-85,40,-70,220) will yield 180
    :param lat1: latitude of baseline coordinate (float)
    :param lon1: longitude of baseline coordinate (float)
    :param lat2: latitude of 2nd coordinate (float)
    :param lon2: longitude of 2nd coordinate (float)
    :return phi: local azimuth angle (float)
    """
    # azimuth angle difference
#    x = np.arccos((np.sin(lat2)-np.sin(lat1)*np.cos(d)) / (np.sin(d)*cos(lat1)))
#    if sin(lon2-lon1)<0:
#        phidiff = x
#    elif sin(lon2-lon1)>0:
#        phidiff = 2*np.pi-x
    lat1 = np.deg2rad(lat1)
    lon1 = np.deg2rad(lon1)
    lat2 = np.deg2rad(lat2)
    lon2 = np.deg2rad(lon2)
    dlon = lon2-lon1
#    dlat = lat2-lat1

    X = np.cos(lat2)*np.sin(dlon)
    Y = np.cos(lat1)*np.sin(lat2)-np.sin(lat1)*np.cos(lat2)*np.cos(dlon)

    phi = np.arctan2(X,Y)
    phi = np.rad2deg(phi)
    return phi

#%% input functions
def acquirelatlon(latlon):        
    try:
        lat = float(latlon.split(',')[0])
        if lat > 90 or lat < -90:
            print("You entered for latitude: ", lat)
            print("Latitude must be between -90 and 90 degrees inclusive.")
            sys.exit(2)
    except:
        print("Latitude value must be inputted.")
        lat = input("Latitude: ")
        lat = float(lat)
    
    try:
        lon = float(latlon.split(',')[1])
        if lon >= 360 or lon <= -360:
            print("You entered for longitude: ", lon)
            print("Longitude must be between -360 and 360 degrees non-inclusive.")
            sys.exit(2)
    except:
        print("Longitude value must be inputted.")
        lon = input("Longitude: ")
        lon = float(lon)
        # sys.exit(2)   
    
    return lat,lon

def acquireR(R):
    if R == "":
        R = 1737400 # meters
        print("Assuming default radius (km): ", R/1000)    
    else:
        R = float(R)
        R*=1000 # meters
        print("Assuming radius (km): ", R/1000)
    return R

def acquire_input(i):
    if i == 'q' or i=="quit":
        print("Exiting program.")
        sys.exit(1)
    else:
        lat,lon = acquirelatlon(i)
        return lat,lon

#%% output functions



#%%
if __name__ == "__main__":
    #%%
    print("Distance and Local Azimuth Calculator")    
    print("Please enter latitude followed by longitude with a comma separating the two numbers.")
    print("Assuming all inputs are in degrees and all outputs are in degrees.")
    print("Assuming radius is the moon's average radius: 1737.4 km.")
    R = input("If not correct, please enter the planetary body's radius in km:")
    R = acquireR(R)    
        
    fields = ['lat1','lon1','lat2','lon2','distance(m)','azimuth(deg)']
    with open('latloncalcs.csv',mode='w',newline='') as file:
        csvwriter = csv.writer(file,delimiter=',')
        csvwriter.writerow(fields)
    
    run = True
    while run:
        latlon1 = input("Enter starting coordinate (lat,lon): ")
        lat1,lon1 = acquire_input(latlon1)
        
        latlon2 = input("Enter ending coordinate (lat,lon): ")    
        lat2,lon2 = acquire_input(latlon2)
        
        print('===INPUT===')
        print('Radius: ', R)
        print('From (lat,lon): ', (lat1,lon1))
        print('To (lat,lon): ', (lat2,lon2))
        print('============')
        print('===OUTPUT===')
        d = calcDist(lat1,lon1,lat2,lon2,R)
        print('Distance (m): ',d)
        phi = calcAzimuth(lat1,lon1,lat2,lon2)
        print('Local azimuth angle (degrees): ', phi)
        print('============')
        
        # append to next line
        with open('latloncalcs.csv',mode='a',newline='') as file:
            csvwriter = csv.writer(file,delimiter=',')
            csvwriter.writerow([lat1,lon1,lat2,lon2,d,phi])        
        
        print('Type q or quit anytime to exit the program.')