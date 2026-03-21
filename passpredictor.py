# passpredictor.py is a file that provides functionality
# for combining tles and a specific satelite to provide orbital
# data for a set of upcoming times.
#
# written by Ryan Deaton (rad53@calvin.edu) for Calvin Hackathon '26 on March 2026

import tlefetch
import convertfromtle
from collections import deque

class passPredictor:
    def __init__(self, selected_satelites):
        self.tleSources = ["https://www.amsat.org/tle/dailytle.txt"]
        self.tles = tlefetch.fetch_all_tles(self.tleSources)
        self.satelites = dict()
    # def update_tle(self):
    def predict_pass(self, satelite, dt = 5, future_predictions = 64800):
        self.tles[satelite]
            

class sateliteData:
    def __init__(self, name, future_predictions = 64800, dt = 5, tles):
        self.name = name
        self.dt = dt
        self.future_predictions = future_predictions
        self.positions = deque([])
        self.predict_full_future()

    def get_current_position(self):
        
    def get_path():

    def get_dt(self):
        return self.dt
    
    def predict_full_future(self):
        self.positions.append()