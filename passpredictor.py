# passpredictor.py is a file that provides functionality
# for combining tles and a specific satellite to provide orbital
# data for a set of upcoming times.
#
# written by Ryan Deaton (rad53@calvin.edu) for Calvin Hackathon '26 on March 2026

import tlefetch
import convertfromtle
from collections import deque


def get_satellites():
    sats = []
    sources = ["https://www.amsat.org/tle/dailytle.txt"]
    tles = tlefetch.fetch_all_tles(sources)
    for satellite in tles:
        sats.append(satellite)
    return sats

class passPredictor:
    def __init__(self, selected_satellites):
        self.tleSources = ["https://www.amsat.org/tle/dailytle.txt"]
        self.selected_satellites = selected_satellites
        self.update_tles()
        
        
    def update_tles(self):
        self.tles = tlefetch.fetch_all_tles(self.tleSources)
        self.satellites = dict()
        for satellite in self.selected_satellites:
            print(self.tles[satellite])
            self.satellites[satellite] = satelliteData(satellite, self.tles[satellite])
            
    
    def update_selected(self, new_selected):
        # Find what's been added and removed
        current = set(self.selected_satellites)
        updated = set(new_selected)

        added   = updated - current
        removed = current - updated

        # Remove deselected satellites
        for satellite in removed:
            del self.satellites[satellite]

        # Add newly selected satellites
        for satellite in added:
            self.satellites[satellite] = satelliteData(satellite, self.tles[satellite])

        # Update the selected list
        self.selected_satellites = new_selected
        
    def get_path(self, satellite):
        return self.satellites[satellite].get_path() # this is a list of tuples of (lat, long, alt)
            

class satelliteData:
    def __init__(self, name, tles, future_predictions = 6480, dt = 5):
        self.name = name
        self.dt = dt
        self.tle = tles
        self.future_predictions = future_predictions
        self.positions = deque()
        self.predict_full_future()

    def get_path(self):
        positions_list = list(self.positions)
        curr = convertfromtle.TLEtoGeodeticSecOffset(self.tle["line1"], self.tle["line2"], self.dt*self.future_predictions)
        self.positions.popleft()
        self.positions.append(curr)
        return positions_list

    def get_dt(self):
        return self.dt
    
    def get_future_predictions(self):
        return self.future_predictions
    
    def set_tle(self, tle):
        self.tle = tle
        self.positions = dict()
        self.predict_full_future()
        return
    
    def predict_full_future(self):
        for i in range(0, self.future_predictions*self.dt, self.dt):
            curr = convertfromtle.TLEtoGeodeticSecOffset(self.tle["line1"], self.tle["line2"], i)
            self.positions.append(curr)

if __name__ == "__main__":
    print(get_satellites())