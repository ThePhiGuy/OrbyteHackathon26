# this file contains riseSetTimes() which provides 
# the times a satellite rises above and sets below the horizon
# written by Joshua Rogan (jbr25@calvin.edu) for Calvin Hackathon 2026

import numpy as np
import convertfromtle, tlefetch
from datetime import datetime, timezone, timedelta
from skyfield.api import EarthSatellite, load, wgs84

# myLocation should be tuple of lat and lon
# satelliteName should be from amsat linked below
# outputs tuple of list of utcTimes and list of events
def riseSetTimesHoursOffset(satelliteName, myLocation, hrs = 8):
    satDict = tlefetch.fetch_tles("https://www.amsat.org/tle/dailytle.txt")

    l1 = satDict.get(satelliteName)["line1"]
    l2 = satDict.get(satelliteName)["line2"]
    satellite = EarthSatellite(l1, l2)
    # make satellite obj for use in find_events()

    loc = wgs84.latlon(myLocation[0], myLocation[1])
    # format location parameter
    
    ts = load.timescale()
    t0 = ts.from_datetime(datetime.now(timezone.utc))
    t1 = ts.from_datetime(datetime.now(timezone.utc) + timedelta(hours = hrs))
    # set time vars

    t, events = satellite.find_events(loc, t0, t1, altitude_degrees=0.0)
    # store find_events data

    utcTimes = []
    for time in t:
        # utcTimes.append(time.utc_datetime().strftime())
        utcTimes.append(time.utc_strftime("%Y-%m-%d %H:%M:%S"))

    return utcTimes, events

# returns next rise time in utc format given
def nextRiseTime(utcTimes, events):
    i = 0
    while i < len(events):
        if events[i] == 0:
            return utcTimes[i]
    # look for event 0 (rise) and return
    return -1

if __name__ == "__main__":
    t, events = riseSetTimesHoursOffset("AO-07", (42.9634, -85.6681))
    print(t, events)
    print(nextRiseTime(t, events))