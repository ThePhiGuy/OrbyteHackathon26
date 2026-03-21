# genIcon.py generates a circle around the satellite icon on the leaflet UI,
# namely the satellite image on the map
#
# written by Ty Veldhouse (tpv8@calvin.edu) for Calvin Hackathon '26 on March 2026

from nicegui import ui

def visCircle(lat, lon, radVis) :
    # Goal: Display the Area of where the given Satellite could be Seen Currently
    # Parameters: Latitude, Longitude, Radian of Visible Area Currently

    m = ui.leaflet(center=(lat, lon)).classes('h-32')
    m.generic_layer(name='satellites', args=[m.center, {'color': 'yellow', 'radius': radVis}])

ui.run()