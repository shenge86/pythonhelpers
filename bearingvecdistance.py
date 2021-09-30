# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 15:11:03 2021

@author: Shen Ge
@name: Bearing vector and Distnce calculator
@description:
    
    Calculates distance and bearing vector for two points
    Minimalistic function that takes in 4 arguments
"""
import sys
import numpy as np

#### GIS Math Functions #####
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

if __name__ == '__main__':
    try:
        lat1,lon1,lat2,lon2 = sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
    except:
        print('You must enter in 4 arguments which represent lat/lon of 2 coordinates. Run code as follows: ')
        print('python bearingvecdistance.py <lat1> <lon1> <lat2> <lon2>')
        
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)
    
    R = 1737400    
    d = calcDist(lat1,lon1,lat2,lon2)
    phi = calcAzimuth(lat1,lon1,lat2,lon2)
    
    print('========================')
    print('ASSUMPTIONS: ')
    print('Assuming spherical radius of: ', R)
    print('For moon, radius is 1737400 meters')
    print('INPUT: ')
    print(f'Coordinate 1: {lat1} N, {lon1}E')
    print(f'Coordinate 2: {lat2} N, {lon2}E')
    print('OUTPUT:')
    print('Azimuth (deg): ', phi)    
    print('Distance: ', d)
    print('========================')