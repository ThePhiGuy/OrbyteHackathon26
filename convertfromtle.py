# convertfromtle.py provides the ability to take in TLEs of satellites and 
# convert them to ECI, then to Geodetic (cartesian lat/long and alt)
# written by Joshua Rogan (jbr25@calvin.edu) for Calvin Hackathon 2026

from sgp4.api import Satrec, jday
import numpy as np
from datetime import datetime
from skyfield.api import EarthSatellite, load

# line1, line2 are TLE components of a satellite
# returns tuple of r (km from earth center) and v (velocity in km/s)
# default arg dt to allow manual datetime input
# def TLEtoECI(line1, line2, dt = datetime.utcnow()):
#     sat = Satrec.twoline2rv(line1, line2)

#     # Time you want position for
#     jd, fr = jday(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

#     # Propagate
#     e, r, v = sat.sgp4(jd, fr)

#     # if e != 0:
#         #theres an error code on the sat, throw some exception or smthg

#     return r, v

def ECItoGeodetic(line1, line2):
    ts = load.timescale()
    t = ts.now()

    satellite = EarthSatellite(line1, line2)

    geocentric = satellite.at(t)
    lat, lon = satellite.latlon_of(geocentric)
    return lat, lon
    # subpoint = geocentric.subpoint()

    # lat = subpoint.latitude.degrees
    # lon = subpoint.longitude.degrees
    # alt = subpoint.elevation.km

    # print("Lat:", lat)
    # print("Lon:", lon)
    # print("Alt (km):", alt)

    # return lat, lon, alt 


# Example TLE (ISS)
line1 = "1 25544U 98067A   26079.87218434  .00009590  00000-0  18573-3 0  9991"
line2 = "2 25544  51.6346  17.0785 0006366 213.2716 146.7873 15.48402839558062"

print(ECItoGeodetic(line1, line2))

# sat = Satrec.twoline2rv(line1, line2)

# Time you want position for
# dt = datetime.utcnow()
# jd, fr = jday(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

# # Propagate
# e, r, v = sat.sgp4(jd, fr)

# if e != 0:
#     print("Error:", e)

# r = position (km) in ECI/TEME frame
# v = velocity (km/s)
# print("Position (km):", r)
# print("Velocity (km/s):", v)