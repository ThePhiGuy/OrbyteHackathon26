# this file contains riseSetTimes() which provides 
# the times a satellite rises above and sets below the horizon
# written by Joshua Rogan (jbr25@calvin.edu) for Calvin Hackathon 2026

import numpy as np
import convertfromtle
from datetime import datetime, timezone, timedelta
from skyfield.api import EarthSatellite, load, wgs84

# myLocation should be tuple of lat and lon
def riseSetTimesOneDay(satelliteName, myLocation):
    loc = convertfromtle.TLEtoGeodetic(satellites[satelliteName].data)
    
    loc = wgs84.latlon(myLocation)
    t0 = datetime.now(timezone.utc)
    t1 = t0 + timedelta(days = 1)
    t, events = satelliteName.find_events(loc, t0, t1, altitude_degrees=0.0)
    return t, events


