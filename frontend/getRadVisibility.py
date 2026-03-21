# getRadVisibility.py generates a circle around the satellite icon on the leaflet UI,
# namely the satellite image on the map
#
# written by Ty Veldhouse (tpv8@calvin.edu) for Calvin Hackathon '26 on March 2026

import math

def getVisRad(heightKM, radEarthKM = 6371.0):
    # Returns: the radius on Earth's surface (in km) from which
    # a satellite at altitude h_km is visible, assuming a spherical Earth.
    print(heightKM)
    psi = math.acos(radEarthKM / (radEarthKM + heightKM))  # central angle in radians
    visRad = radEarthKM * psi                      # great-circle distance
    return visRad
