# genSatellite.py generates one Satellite on the leaflet UI,
# first the satellite marker and icon on the map,
# then the visibility circle around it, then the flight path
#
# written by Ty Veldhouse (tpv8@calvin.edu) for Calvin Hackathon '26 on March 2026

from nicegui import ui

def drawVisCircle(my_map, lat, lon, radVis, color) :
    # Goal: Display the Area of where the given Satellite could be Seen Currently with a Circle
    # Parameters: Latitude, Longitude, Radian of Visible Area Currently
    my_map.generic_layer(
        name='circle', 
        args=[[lat, lon], {'color': color, 'radius': radVis}]
    )
    
def drawFlightPath(my_map, coords, color):
    # Goal: To draw the pre-calculated future flightpath the satellite using a polyline
    # Parameters: coords - a List of tuples/lists [lat, lon]
    
    segments = []
    current_segment = []

    for i, coord in enumerate(coords):
        if i > 0:
            prev_lon = coords[i-1][1]
            curr_lon = coord[1]
            
            # If the jump is larger than 180 degrees, we crossed the map edge!
            if abs(curr_lon - prev_lon) > 180:
                segments.append(current_segment) # Save the line we were drawing
                current_segment = []             # Start a new line
                
        current_segment.append(coord)
        
    # Append the final segment after the loop finishes
    if current_segment:
        segments.append(current_segment)

    # Draw each segment as its own separate polyline
    for segment in segments:
        if len(segment) > 1: # Only draw if there are enough points to make a line
            my_map.generic_layer(
                name='polyline', 
                args=[segment, {'color': color, 'weight': 4, 'opacity': 0.8}]
            )

def drawSatellite (my_map, lat, lon, radVisible, coords, color,
             imageURL= "https://img.freepik.com/premium-psd/satellite-isolated-transparent-background_1073071-13672.jpg") :
    # Goal: Generate map marker object and return it for future changes
    # Parameters: Latitude, Longitude, Radian of Visible Area Currently, Flightpath Coordinates, Icon Image URL
    # Returns: Marker object
    # Calls: Current Visibility Circle around itself

    marker = my_map.marker(latlng = (lat, lon))#.tooltip(name) # initialize marker
    # custom marker icon javascript
    custom_icon_js = f'''L.icon({{
    iconUrl: '{imageURL}',
    iconSize: [40, 40], // width and height of the icon
    iconAnchor: [20, 20], // point of the icon which will correspond to marker's location
    }})'''
    # apply custom marker js
    marker.run_method(':setIcon', custom_icon_js)

    drawVisCircle(my_map, lat, lon, radVisible, color)
    drawFlightPath(my_map, coords, color)
    return marker