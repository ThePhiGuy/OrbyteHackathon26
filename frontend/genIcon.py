# genIcon.py generates an icon on the leaflet UI,
# namely the satellite image on the map
#
# written by Ty Veldhouse (tpv8@calvin.edu) for Calvin Hackathon '26 on March 2026

from nicegui import ui
import genVisbilityCircle

def genIcon (xcoord, ycoord, scalar, radVisible, satelliteImage) :
    m = ui.leaflet(center=(52.5165, 13.4047), zoom=13)
    m.image_overlay(
        url = satelliteImage,
        bounds = [[xcoord + scalar, ycoord + scalar], [xcoord + scalar, ycoord + scalar]],
        options = {'opacity': 0.8},
        genVisibilityCircle.visCircle(xcoord, ycoord, radVis)
    )