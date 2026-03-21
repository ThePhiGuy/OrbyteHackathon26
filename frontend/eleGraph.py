# eleGraph.py updates the graph of
#
# written by Ty Veldhouse (tpv8@calvin.edu) for Calvin Hackathon '26 on March 2026

import numpy as np
from nicegui import ui

def update_graph (time_alt) :
    # Goal: Update/Draw the graph of the visibility of a selected Satellite
    # Parameters: time_alt - List of tuples (Time, Altitude)

    # Position of graph
    with ui.row().classes('w-full justify-center'):

        # Drawing Graph
        with ui.matplotlib(figsize=(3, 2)).figure as fig:

            # Creation and naming of axes
            axes = fig.gca()
            axes.set_title('Satellite Elevation Over Time')
            axes.set_xlabel('Time')
            axes.set_ylabel('Elevation (degrees)')

            # Unzipping Tuples
            times = []
            alts = []

            for i in range(len(time_alt)):
                times.append(int(print(time_alt[i][0])))
                alts.append(time_alt[i][1])

            # Plots on the map
            axes.plot(times, alts, '-')

# Needed?
# ui.run()