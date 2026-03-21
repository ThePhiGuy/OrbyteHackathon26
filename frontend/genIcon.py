# genIcon.py generates an icon on the leaflet UI,
# namely the satellite image on the map
#
# written by Ty Veldhouse (tpv8@calvin.edu) for Calvin Hackathon '26 on March 2026

from nicegui import ui
import genVisbilityCircle

def genIcon (lat, lon, radVisible, 
             imageURL= "https://img.freepik.com/premium-psd/satellite-isolated-transparent-background_1073071-13672.jpg") :
    # Goal: Generate map icon
    # Returns: marker object
    # Calls: Current Visibility Circle around itself
    # Parameters: Latitude, Longitude, Radian of Visible Area Currently, Icon Image URL

    marker = map_obj.marker(
        location=(lat, lon),
        icon={
            'iconUrl': imageURL,
            'iconSize': [40, 40],      # width, height in pixels
            'iconAnchor': [lat, lon],    # where the "point" of the marker is
        }     
    )
    genVisbilityCircle.visCircle(lat, lon, radVisible)
    return marker