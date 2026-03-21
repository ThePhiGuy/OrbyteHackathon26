# convertfromtle.py provides the ability to take in TLEs of satellites and 
# convert them to ECI, then to Geodetic (cartesian lat/long and alt)
# 
# methods:
# TLEtoGeodetic(line1, line2, dt)
# TLEtoGeodeticSecOffset(line1, line2, secOffset)
# TLEtoGeodeticDTSecOffset(line1, line2, dt, secOffset)
# 
# written by Joshua Rogan (jbr25@calvin.edu) for Calvin Hackathon 2026

from sgp4.api import Satrec, jday
import numpy as np
from datetime import datetime, timezone, timedelta
from skyfield.api import EarthSatellite, load, wgs84

# line1, line2 are TLE components of a satellite
# returns lat, long (in deg), and alt (km) 
# dt (datetime) for allow manual datetime input
def TLEtoGeodetic(line1, line2, dt):
    ts = load.timescale()
    #creates timescale
    t = ts.from_datetime(dt)
    #gets time from datetime

    satellite = EarthSatellite(line1, line2)
    #create satellite obj from TLEs

    geocentric = satellite.at(t)
    subpoint = geocentric.subpoint()
    #turn into subpoint, get lat, lon, alt

    lat = subpoint.latitude.degrees
    lon = subpoint.longitude.degrees
    alt = subpoint.elevation.km

    return float(lat), float(lon), float(alt) 

# line1, line2 are TLE components of a satellite
# returns lat, long (in deg), and alt (km) 
# secOffset (int) allows for sec offset from current time (UTC)
def TLEtoGeodeticSecOffset(line1, line2, secOffset):
    ts = load.timescale()
    #creates timescale
    t = ts.from_datetime(datetime.now(timezone.utc) + timedelta(seconds = secOffset))
    #gets time from datetime

    satellite = EarthSatellite(line1, line2)
    #create satellite obj from TLEs

    geocentric = satellite.at(t)
    subpoint = geocentric.subpoint()
    #turn into subpoint, get lat, lon, alt

    lat = subpoint.latitude.degrees
    lon = subpoint.longitude.degrees
    alt = subpoint.elevation.km

    return float(lat), float(lon), float(alt) 

# line1, line2 are TLE components of a satellite
# returns lat, long (in deg), and alt (km) 
# dt (datetime) for allow manual datetime input
# secOffset (int) allows for sec offset from given time dt (UTC)
def TLEtoGeodeticDTSecOffset(line1, line2, dt, secOffset):
    ts = load.timescale()
    #creates timescale
    t = ts.from_datetime(dt + timedelta(seconds = secOffset))
    #gets time from datetime

    satellite = EarthSatellite(line1, line2)
    #create satellite obj from TLEs

    geocentric = satellite.at(t)
    subpoint = geocentric.subpoint()
    #turn into subpoint, get lat, lon, alt

    lat = subpoint.latitude.degrees
    lon = subpoint.longitude.degrees
    alt = subpoint.elevation.km

    return float(lat), float(lon), float(alt) 

def BatchTLEtoGeodeticSecOffset(line1, line2, secOffset, points):
    ts = load.timescale()
    satellite = EarthSatellite(line1, line2)
    currentTime = datetime.now(timezone.utc)

    #compute all times in one vector
    offsets = np.arange(0, points * secOffset, secOffset)  #(start,stop,step)
    datetimes = [currentTime + timedelta(seconds=int(s)) for s in offsets]
    times = ts.from_datetimes(datetimes)

    #compute geocentric positions for each time
    geocentric = satellite.at(times)
    subpoints = geocentric.subpoint()  #subpoint is projection of geocent onto earth

    #make list of tuples
    tupList = list(zip(
        (float(lat) for lat in subpoints.latitude.degrees),
        (float(lon) for lon in subpoints.longitude.degrees),
        (float(alt) for alt in subpoints.elevation.km)
    ))
    return tupList

# line1, line2 are TLE components
# dt is datetime object (UTC)
# myLoc is tuple of (lat, lon) in degrees
# returns altitude and azimuth in degrees
def getAltAzDeg(line1, line2, dt, myLoc):
    ts = load.timescale()
    t = ts.from_datetime(dt)
    satellite = EarthSatellite(line1, line2)
    
    #user location
    location = wgs84.latlon(myLoc[0], myLoc[1])
    
    #calculate topocentric point from satellite and location
    difference = satellite - location
    topocentric = difference.at(t)
    
    #assign vals and return
    alt, az, distance = topocentric.altaz()
    
    return float(alt.degrees), float(az.degrees)

if __name__ == "__main__":
    # Example TLE (ISS)
    line1 = "1 25544U 98067A   26079.87218434  .00009590  00000-0  18573-3 0  9991"
    line2 = "2 25544  51.6346  17.0785 0006366 213.2716 146.7873 15.48402839558062"
    # print(TLEtoGeodetic(line1, line2, datetime.now(timezone.utc)))
    # print(TLEtoGeodeticSecOffset(line1, line2, 5))
    # print(TLEtoGeodeticDTSecOffset(line1, line2, datetime.now(timezone.utc), 5))
    # print(getAltAzDeg(line1, line2, datetime.now(timezone.utc), (42.9634, -85.6681)))
    temp = (BatchTLEtoGeodeticSecOffset(line1, line2, 5, 5500))
    for tup in temp[:50]:
        print(tup)
    print(len(temp))

# = datetime.now(timezone.utc)