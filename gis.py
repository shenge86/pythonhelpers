#!/usr/bin/env python3

"""
Geographic Information Systems (GIS) suite of functions
and analysis for surface calculations
"""
import sys,os
import numpy as np

def calcDist(lat1,lon1,lat2,lon2,R=1737400):
    """Calculate distance between two lat and lons (inputted in degrees)
    note this is the points at sea level below each of the peaks and not the straight-line distance between the peaks
    # This is the method recommended for calculating short distances by Bob Chamberlain (rgc@jpl.nasa.gov) of Caltech and NASA's Jet Propulsion Laboratory as described on the U.S. Census Bureau Web site. 
    # This formula does not take into account the non-spheroidal (ellipsoidal) shape of the Earth. It will tend to overestimate trans-polar distances and underestimate trans-equatorial distances.
    # References: 
    # http://tchester.org/sgm/analysis/peaks/how_to_get_view_params.html
    # https://andrew.hedges.name/experiments/haversine/
    # https://cs.nyu.edu/visual/home/proj/tiger/gisfaq.html # detailed explanation of different calculation methods
    :param lat1: latitude of baseline coordinate in degrees (float)
    :param lon1: longitude of baseline coordinate in degrees (float)
    :param lat2: latitude of 2nd coordinate in degrees (float)
    :param lon2: longitude of 2nd coordinate in degrees (float)
    :param R: radius of spherical body; default is 1737400 meters which is that of moon used by LOLA / Kaguya data (float) 
    :return d: distance between the two coordinates (float)
    """
    if np.abs(lat1) > 90 or np.abs(lat2) > 90:
        print('Latitude must be between -90 and 90 degrees.')
        return 0
    
    if np.abs(lon1) > 360 or np.abs(lon2) > 360:
        print('Longitude must be between -360 and 360 degrees.')
        return 0
        

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

def calcCoord(lat1,lon1,phi,d,R=1737400):
    """returns another coordinate knowing the baseline coordinate and the local azimuth angle
    :param lat1: latitude of baseline (float)
    :param lat2: longitude of baseline (float)
    :param phi: local azimuth angle (float)
    :param d: distance (float)
    :param R: radius of planetary body (default is 1737400 meters for that of the moon) (int)
    """
    R = abs(R)
    lat1 = np.deg2rad(lat1)
    lon1 = np.deg2rad(lon1)
    phi = np.deg2rad(phi)
    
    # angular distance
    alpha = d/R
    
    lat2 = np.arcsin(np.sin(lat1)*np.cos(alpha)+np.cos(lat1)*np.sin(alpha)*np.cos(phi))
    lon2 = lon1 + np.arctan2(np.sin(phi)*np.sin(alpha)*np.cos(lat1), np.cos(alpha)-np.sin(lat1)*np.sin(lat2))
    
    lat2 = np.rad2deg(lat2)
    lon2 = np.rad2deg(lon2)
    return lat2,lon2

def calcElvangle(d,elv1,elv2,R=1737400,precise=False):
    """Returns elevation angle (in rad) knowing two elevations and the distance between them as well as the radius of the body
       accounting for curvature of moon with small angle approximation, i.e. arcsin(theta) = theta when theta is small
       NOTE: This is an approximation that should give very good answers for all elevation differences << radius of planetary body
       References:
           http://tchester.org/sgm/analysis/peaks/how_to_get_view_params.html
    
    :param d: distance to the other coordinate
    :type d: float
    :param elv1: elevation at baseline coordinate
    :type elv1: float
    :param elv2: elevation at second corodinate
    :type elv2: float
    :param R: radius of spherical body; default is 1737400 meters which is that of moon used by LOLA / Kaguya data
    :type R: float
    :param precise: assuming that the drop in height is significant enough
    :type precise: boolean
    :returns: elevation angle in degrees
    :rtype: float
    """
    try: 
        # apparent drop in height due to curvature of planetoid
        if precise is False:
            hdrop = d**2/(2*R)
        else:
            hdrop = np.sqrt(R**2+d**2)-R
        thetadrop = hdrop / d
        theta = (elv2 - elv1)/d - thetadrop
        theta = np.rad2deg(theta)
        
        # debugging only for non-lists:
#        if (elv2 - elv1) < 600:
#            print("Elevation is: ", elv2)
#            print("Elevation difference is: ", elv2-elv1)
    except ZeroDivisionError:
        print("Distance inputted should not be 0. Assuming theta is 0 degrees.")
        theta = 0

    return theta


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Requires 4 arguments.')
        print('python3 gis.py <lat1> <lon1> <lat2> <lon2>')
        print('lat lon coordinates must be integers or floats')
        print('latitudes must be between -90 and 90 degrees')
        print('longitudes must be between -360 to 360 degrees')
        sys.exit(2)

    lat1 = float(sys.argv[1])
    lon1 = float(sys.argv[2])
    lat2 = float(sys.argv[3])
    lon2 = float(sys.argv[4])
    
    d = calcDist(lat1,lon1,lat2,lon2,R=1737400)
    print('Distance (km): ', d/1000)