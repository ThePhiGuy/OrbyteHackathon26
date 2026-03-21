# genSatellite.py generates one Satellite on the leaflet UI,
# first the satellite marker and icon on the map,
# then the visibility circle around it, then the flight path
#
# written by Ty Veldhouse (tpv8@calvin.edu) for Calvin Hackathon '26 on March 2026

from nicegui import ui

def drawVisCircle(my_map, lat, lon, radVis) :
    # Goal: Display the Area of where the given Satellite could be Seen Currently with a Circle
    # Parameters: Latitude, Longitude, Radian of Visible Area Currently
    visCirc = my_map.leaflet(center=(lat, lon)).classes('h-32')
    visCirc.generic_layer(name='satellites', args=[visCirc.center, {'color': 'yellow', 'radius': radVis}])

def drawFlightPath(my_map, coords) :
    # Goal: To draw the pre-calculated future flightpath the satellite using a polyline
    # Parameters: coords - a List of tuples [lat, lon]
    my_map.generic_layer(
    name = 'polyline', 
    args = [coords, {'color': 'red', 'weight': 4, 'opacity': 0.8}]
    )

def drawSatellite (my_map, lat, lon, radVisible, coords,
             imageURL= "https://img.freepik.com/premium-psd/satellite-isolated-transparent-background_1073071-13672.jpg") :
    # Goal: Generate map marker object and return it for future changes
    # Parameters: Latitude, Longitude, Radian of Visible Area Currently, Flightpath Coordinates, Icon Image URL
    # Returns: Marker object
    # Calls: Current Visibility Circle around itself

    marker = my_map.marker(
        location=(lat, lon),
        icon={
            'iconUrl': imageURL,
            'iconSize': [40, 40],      # width, height in pixels
            'iconAnchor': [lat, lon],    # where the "point" of the marker is
        }     
    )

    drawVisCircle(my_map, lat, lon, radVisible)
    drawFlightPath(my_map, coords)
    return marker