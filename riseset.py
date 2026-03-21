# this file contains methods to calculate the 
# times a satellite rises above, peaks, and sets below the horizon
# and the satellite's next rise time
# 
# nextRiseTime()
# nextPassDuration()
#
#  written by Joshua Rogan (jbr25@calvin.edu) for Calvin Hackathon 2026

import numpy as np
import convertfromtle, tlefetch
from datetime import datetime, timezone, timedelta
from skyfield.api import EarthSatellite, load, wgs84

# primarily helper for 
# myLocation should be tuple of lat and lon
# satelliteName should be from amsat linked below
# hrs (int) for offset from current time, default is 24
# outputs tuple of list of utcTimes and list of events
def riseSetTimesHoursOffset(satelliteName, myLocation, hrs = 24):
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

    return t, events

# returns next rise time in utc format given
# takes same params as riseSetTimesHoursOffset
def nextRiseTime(satelliteName, myLocation):
    t, events = riseSetTimesHoursOffset(satelliteName, myLocation)
    i = 0
    while i < len(events):
        if events[i] == 0:
            return formatUTC(t[i])
        i += 1
    # look for event 0 (rise) and return
    return datetime.max

#  returns time of pass in seconds as float
#  takes same params as riseSetTimesHoursOffset
def nextPassDuration(satelliteName, myLocation):
    t, events = riseSetTimesHoursOffset(satelliteName, myLocation)
    i = 0
    while i < len(events):
        if events[i] == 0:
            j = i
            while j < len(events):
                if events[j] == 2:
                    duration = (t[j].utc_datetime() - t[i].utc_datetime())
                    return float(duration.total_seconds())
                j += 1
        i += 1
    # find rise time, then find next set time, return difference
    return -1 

# helper method to format time nicely
def formatUTC(utcTime):
    return utcTime.utc_strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    t, events = riseSetTimesHoursOffset("AO-07", (42.9634, -85.6681))
    print(t, events)
    print(nextRiseTime("AO-07", (42.9634, -85.6681)))
    print(nextPassDuration("AO-07", (42.9634, -85.6681)))