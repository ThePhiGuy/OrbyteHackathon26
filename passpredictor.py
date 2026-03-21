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
    def __init__(self, name, tles, future_predictions = 3000, dt = 5): #6480, 5
        self.name = name
        self.dt = dt
        self.tle = tles
        self.future_predictions = future_predictions
        self.positions = deque()
        self.predict_full_future()

    def get_path(self):
        positions_list = list(self.positions)
        curr = convertfromtle.TLEtoGeodeticSecOffset(self.tle["line1"], self.tle["line2"], self.future_predictions)
        self.positions.popleft()
        self.positions.append(curr)
        return positions_list

    def get_dt(self):
        return self.dt
    
    def get_future_predictions(self):
        return self.future_predictions
    
    def set_tle(self, tle):
        self.tle = tle
        # self.positions = dict() we prob want deque here
        self.positions = deque()
        self.predict_full_future()
        return
    
    def predict_full_future(self):
        # for i in range(0, self.future_predictions, self.dt):
        #     curr = convertfromtle.TLEtoGeodeticSecOffset(self.tle["line1"], self.tle["line2"], i)
        #     self.positions.append(curr)
        
        num_points = self.future_predictions / self.dt
        # adjusts to avoid insanely long path since point-based, not time-based
        self.positions.extend(convertfromtle.BatchTLEtoGeodeticSecOffset(self.tle["line1"], self.tle["line2"], self.dt, num_points))

if __name__ == "__main__":
    # print(get_satellites())

    # Get TLEs
    tles = tlefetch.fetch_tles("https://www.amsat.org/tle/dailytle.txt")

    # Pick a satellite (make sure name exists!)
    sat_name = list(tles.keys())[0]  # first satellite
    sat_tle = tles[sat_name]

    print("Testing satellite:", sat_name)

    # Create object (this runs predict_full_future automatically)
    sat = satelliteData(sat_name, sat_tle)

    # Check results
    print("Number of positions:", len(sat.positions))
    print("First 5 positions:")
    for p in list(sat.positions)[:5]:
        print(p)

    # First call
    path1 = sat.get_path()
    print("Length of path:", len(path1))
    print("First 3 points:", path1[:3])

    # Second call (should shift)
    path2 = sat.get_path()

    print("\nAfter second call:")
    print("First element changed:", path1[0] != path2[0])
    print("Last element changed:", path1[-1] != path2[-1])