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
        for satelite in selected_satelites:
            self.satelites[satelite] = sateliteData(satelite, )
    # def update_tle(self):

    def predict_pass(self, satelite, dt = 5, future_predictions = 64800):
        line1 = self.tles[satelite]
        def ECItoGeodetic(line1, line2):
            

class sateliteData:
    def __init__(self, name):
        self.name = name
        self.positions =
    def get_current_position():
        