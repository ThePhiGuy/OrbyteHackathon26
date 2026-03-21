# convertfromtle.py provides the ability to take in TLEs of satellites and 
# convert them to ECI, then to Geodetic (cartesian lat/long and alt)
# written by Joshua Rogan (jbr25@calvin.edu) for Calvin Hackathon 2026

from sgp4.api import Satrec, jday
import numpy as np
from datetime import datetime, timezone, timedelta
from skyfield.api import EarthSatellite, load

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

# Example TLE (ISS)
line1 = "1 25544U 98067A   26079.87218434  .00009590  00000-0  18573-3 0  9991"
line2 = "2 25544  51.6346  17.0785 0006366 213.2716 146.7873 15.48402839558062"

print(TLEtoGeodetic(line1, line2, datetime.now(timezone.utc)))
print(TLEtoGeodeticSecOffset(line1, line2, 5))

# = datetime.now(timezone.utc)