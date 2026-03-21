# eleGraph.py updates the graph of
#
# written by Ty Veldhouse (tpv8@calvin.edu) for Calvin Hackathon '26 on March 2026

def latlon_to_cart(lat, lon, earthRad):
    # Goal: Calculate the satellite's Cartesian Coordinates from Latitude and Longitude
    # Parameters: Satellite Latitude & Longitude and Radius of the Earth

    # Convert lat & lon to radians
    lat = math.radians(lat)
    lon = math.radians(lon)

    # x y z coordinate calculations
    x = earthRad * math.cos(lat) * math.cos(lon)
    y = earthRad * math.cos(lat) * math.sin(lon)
    z = earthRad * math.sin(lat)

    return (x, y, z)

def update_graph (user_lat, user_lon, sat_lat, sat_lon, alt) :
    # Goal: Update/Draw the graph of the visibility of a selected Satellite
    # Parameters: User Latitude & Longitude, Satellite Latitude & Longitude, Altitude
