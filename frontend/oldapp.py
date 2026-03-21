from nicegui import ui
import random

# Keep track of where the satellite has been
path_history = [[20, 0, 10]]
orbit_coordinates = [
        [34.0522, -118.2437, 100], # Los Angeles
        [39.7392, -104.9903], # Denver
        [41.8781, -87.6298],  # Chicago
        [40.7128, -74.0060]   # New York
]

@ui.page('/')
def main_page():
    
    # 1. Sidebar
    with ui.left_drawer(value=True).classes('bg-gray-100 p-4'):
        ui.label('Satellite Tracker').classes('text-xl font-bold mb-4')
        coord_label = ui.label('Waiting for data...')
    

    # 2. Map & Starting Marker
    my_map = ui.leaflet(center=(20, 0), zoom=2).classes('w-full h-screen')
    sat_marker = my_map.marker(latlng=(20, 0))
    
    # 3. Create the Polyline (The Path)
    # We pass the history list, plus standard Leaflet styling options
    sat_path = my_map.generic_layer(name='polyline', args=[path_history, {'color': 'red', 'weight': 3}])
    my_map.generic_layer(
        name='polyline', 
        args=[orbit_coordinates, {'color': 'red', 'weight': 4, 'opacity': 0.8}]
    )
    # 4. Update Function
    def update_satellite():
        print("Running...")
        # Get the last known coordinate and move slightly from there
        last_lat, last_lon = path_history[len(path_history)-1]
        new_lat = last_lat + random.uniform(-5, 5)
        new_lon = last_lon + random.uniform(-5, 5)
        
        # Move the physical marker
        sat_marker.move(new_lat, new_lon)
        
        # Add the new coordinate to our history list
        path_history.append([new_lat, new_lon])
        
        # Push the updated history list directly to Leaflet to extend the line!
        #sat_path.run_layer_method('addLatLng', [new_lat, new_lon])
        sat_path = my_map.generic_layer(name='polyline', args=[path_history, {'color': 'red', 'weight': 3}])
        # Update the UI text
        coord_label.set_text(f'Lat: {new_lat:.2f}, Lon: {new_lon:.2f}')

    ui.timer(30.0, update_satellite)

if __name__ in {"__main__", "__mp_main__"}:
    # As long as PyQt6 is installed, this will open in a native app window!
    ui.run(title="Satellite App", reload=False)