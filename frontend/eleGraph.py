# eleGraph.py updates the graph of the Visibility from current location
# The graph will map the visibility of the satellite against
# the horizon so it can be easily translated to realtime viewing
#
# written by Ty Veldhouse (tpv8@calvin.edu) for Calvin Hackathon '26 on March 2026

import numpy as np
from nicegui import ui
import convertfromtle

# Which satellite the dropdown currently holds
selected_satellite = None

def draw_graph_overhead() :
    global selected_satellite

    with ui.row().classes('w-full items-center justify-between p-4'):

        # Dropdown (left side)
        satellite_dropdown = ui.select(
            options=['Satellite A', 'Satellite B', 'Satellite C'],
            label='Select Satellite'
        ).classes('w-1/2')

        # Button (right side)
        ui.button('Update Graph', on_click=lambda: update_graph()).classes('ml-4')


def update_graph (user_loc, time_alt) :
    # Goal: Update/Draw the graph of the visibility of a selected Satellite
    # Parameters: 
    #   user_loc, a tuple of the user Locations
    #   time_alt - List of tuples (Time, Altitude)
    global selected_satellite

    if not selected_satellite:
        return

    # Grabs which Satellite
    convertfromtle.getTupListAltDeg(selected_satellite, user_loc)

    # Position of graph
    with ui.row().classes('w-full justify-center'):

        # Drawing Graph
        with ui.matplotlib(figsize=(3, 2)).figure as fig:

            # Creation and naming of axes
            axes = fig.gca()
            axes.clear()
            axes.set_title('Visible Satellite Elevation Over Time')
            axes.set_xlabel('Time')
            axes.set_ylabel('Elevation (degrees)')

            # Unzipping Tuples
            times = []
            alts = []

            for i in range(len(time_alt)):
                times.append(int(time_alt[i][0]))
                alts.append(time_alt[i][1])

            # Plots on the map
            axes.plot(times, alts, '-')

# Needed?
# ui.run()