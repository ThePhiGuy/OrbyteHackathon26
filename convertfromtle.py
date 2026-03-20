# convertfromtle.py provides the ability to take in TLEs of satellites and 
# convert them to ECI, then to cartesian lat/long and alt
# written by Joshua Rogan (jbr25@calvin.edu) for Calvin Hackathon 2026

from sgp4.api import Satrec, jday
import numpy as np
from datetime import datetime

# Example TLE (ISS)
line1 = "1 25544U 98067A   19343.69339541  .00001764  00000-0  38792-4 0  9991"
line2 = "2 25544  51.6439 211.2001 0007417  17.6667  85.6398 15.50103472202482"

sat = Satrec.twoline2rv(line1, line2)

# Time you want position for
dt = datetime.utcnow()
jd, fr = jday(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

# Propagate
e, r, v = sat.sgp4(jd, fr)

if e != 0:
    print("Error:", e)

# r = position (km) in TEME frame
# v = velocity (km/s)
print("Position (km):", r)
print("Velocity (km/s):", v)