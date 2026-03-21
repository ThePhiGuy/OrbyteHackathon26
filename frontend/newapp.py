from nicegui import ui
import os 
import sys
import drawSatellite as ds
import getRadVisibility as grv
from datetime import datetime, timezone, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import passpredictor
import riseset

# API object
API = passpredictor.passPredictor(())
# list of all satellites
satellite_dict = {"ISS": (), "Hubble": (), "Starlink-1": (), "Landsat": ()} # lil test
# set dict to satellite names
my_list = passpredictor.get_satellites()
satellite_dict = {item: None for item in my_list} # set dict to have the sat names as keys
# list of selected satellites to show on map
selected_satellites = set() 
# satellite times
satellite_labels = {}
# user's current location
user_loc = (0, 0)

cycle_counter = 59
force_update = False
user_marker = None
my_map = None
@ui.page('/')
def main_page():
    # resets on page reload
    satellite_ui_elements = {}

    # filter satellites
    def filter_satellites(e):
        search_term = e.value.lower()
        #This now toggles the visibility of the ENTIRE row, collapsing the empty space
        for name, row_container in satellite_ui_elements.items():
            row_container.set_visibility(search_term in name.lower())
    
    # select satellite
    def select_satellite(sat_name, btn_object):
        global force_update
        # deselect if selected
        if sat_name in selected_satellites:
            selected_satellites.remove(sat_name)
            btn_object.props('color=grey-4') # Back to light grey
            btn_object.classes(replace='w-full mb-2 text-black') # change text color for readability
        # If it's not selected, select it
        else:
            selected_satellites.add(sat_name) 
            btn_object.props('color=grey-9') # Turn dark grey
            btn_object.classes(replace='w-full mb-2 text-white') # change text color for readability
        force_update = True
        print(force_update)
        # Popup for tracking
        #ui.notify(f'Tracking: {list(selected_satellites)}')

    # update satellite time labels
    def get_countdown_string(target_time_str):
        # Get current UTC time
        now_utc = datetime.now(timezone.utc)
        
        # Parse target hours and minutes
        target_hours, target_minutes = map(int, target_time_str.split(':'))
        
        # Create target datetime object for today
        target_time = now_utc.replace(hour=target_hours, minute=target_minutes, second=0, microsecond=0)
        
        # Handle midnight rollover: if target time has passed, it occurs tomorrow
        if target_time < now_utc:
            target_time += timedelta(days=1)
            
        # Calculate time remaining
        time_remaining = target_time - now_utc
        
        # Convert to hours and minutes
        total_seconds = int(time_remaining.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes = remainder // 60
        
        # Format output as HH:MM
        return str(f"{hours:02d}:{minutes:02d}")


    def update_countdown_times():
        global user_loc
        global satellite_labels
        # This will run every 60 seconds
        rise_times = riseset.nextRiseTimeDict(user_loc)
        #current_utc_time = datetime.now(timezone.utc)
        for sat_name, label in satellite_labels.items():
            try:
                #loc = user_marker.props.get('latlng')
                #print("it works")
                sat_utc_arrival_string = rise_times[sat_name]
                #print(get_countdown_string(sat_utc_arrival_string))
                time_left = get_countdown_string(sat_utc_arrival_string)
    
                label.text = f"{time_left}"
            except:
                print("fail")
                continue

    # Sidebar sort function
    def sort_satellites(e):
        sort_method = e.value
        
        # Get the current list of satellite names
        sat_names = list(satellite_ui_elements.keys())
        
        if sort_method == "Alphabetical":
            sat_names.sort(key=str.lower)
            
        elif sort_method == "Acquisition of Signal":
            # Helper function to turn "MM:SS" or "HH:MM:SS" into pure seconds for sorting
            def get_seconds(name):
                time_text = satellite_labels[name].text
                if time_text == '--:--' or not time_text:
                    return float('inf') # Push invalid/empty times to the very bottom
                
                try:
                    parts = time_text.split(':')
                    if len(parts) == 2:
                        return int(parts[0]) * 60 + int(parts[1])
                    elif len(parts) == 3:
                        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                except ValueError:
                    pass
                return float('inf')
                
            sat_names.sort(key=get_seconds)
            
        else:
            # "Unsorted" - fallback to the original dictionary order
            sat_names = list(satellite_dict.keys())
            
        # Reorder the UI elements by moving them inside the list container
        for i, name in enumerate(sat_names):
            satellite_ui_elements[name].move(list_container, i)

    # Sidebar 
    with ui.left_drawer(value=True).classes('bg-gray-100 p-4 flex flex-col'):
        
        # 2. Search Bar
        ui.input('Search satellites...', on_change=filter_satellites).classes('w-full mb-4')
        
        # 3. Sorting dropdown menu - NOW WIRED UP!
        select1 = ui.select(
            ["Unsorted", "Alphabetical", "Acquisition of Signal"], 
            value="Unsorted", 
            on_change=sort_satellites
        ).classes('w-full mb-4')
        
        # The scroll area for the buttons
        with ui.scroll_area().classes('w-full flex-grow border p-2'):
            
            # EXTRA: We need a specific container inside the scroll area to shuffle items around in
            list_container = ui.column().classes('w-full gap-0')
            
            with list_container:
                for key in satellite_dict.keys():
                    
                    row = ui.row().classes('w-full items-center justify-between mb-2 gap-2 flex-nowrap')
                    
                    with row:
                        if key in selected_satellites:
                            btn = ui.button(key, color="grey-9").classes('flex-1 text-white truncate')
                        else:
                            btn = ui.button(key, color="grey-4").classes('flex-1 text-black truncate')
                        
                        time_label = ui.label('--:--').classes('text-sm text-gray-600 w-12 text-right font-mono')
                    
                    satellite_ui_elements[key] = row
                    satellite_labels[key] = time_label
                    
                    btn.on_click(lambda e, k=key, b=btn: select_satellite(k, b))


    
    # User location marker
    def submit_location():
        global user_marker
        global user_loc
        try:
            lat = float(lat_input.value)
            lon = float(lon_input.value)
            user_loc = (lat, lon)
            # Use the map to remove the layer, not the marker itself
            if user_marker:
                my_map.remove_layer(user_marker)

            # Add new marker
            user_marker = my_map.marker(latlng=(lat, lon))

            # Center map on user
            #my_map.set_center((lat, lon))

            ui.notify(f'Location set to: ({lat}, {lon})')
            ui.timer(0.1, update_countdown_times, once=True)

        # 3. Specifically catch ValueError so we don't accidentally hide other bugs
        except ValueError: 
            ui.notify('Invalid input! Please enter numbers.', color='negative')

    # User Location
    with ui.row().classes('w-full items-center gap-4'):
        ui.label('Input Your Location').classes('mr-6')

        # 3. 'w-24' gives them identical widths
        # 4. props('dense') shrinks their height to perfectly match the button
        lat_input = ui.input(label='Lat').classes('w-24').props('dense')
        lon_input = ui.input(label='Long').classes('w-24').props('dense')

        ui.button('Submit', on_click=submit_location)

    # Map & Starting Marker
    # Initialize the map 
    my_map = ui.leaflet(center=(20, 0), zoom=2, options={
        'maxBounds': [[-90, -180], [90, 180]], 
        'maxBoundsViscosity': 1.0              
    }).classes('w-full h-screen')

    # Delete the default, infinite-wrapping map images
    my_map.clear_layers()

    # Add the exact same map images back, but strictly forbid them from wrapping
    my_map.tile_layer(
        url_template='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        options={
            'noWrap': True,
            'bounds': [[-90, -180], [90, 180]]
        }
    )

    # setup nighttime
    async def setup_nighttime():
        # Wait for NiceGUI to finish building the map
        await my_map.initialized() 
        
        js_code = f'''
            // 1. Create a script tag dynamically
            var script = document.createElement('script');
            script.src = 'https://unpkg.com/@joergdietrich/leaflet.terminator/L.Terminator.js';
            
            // 2. Tell the browser what to do AFTER the script finishes downloading
            script.onload = function() {{
                // Grab the specific map using NiceGUI's getElement method
                var my_leaflet_map = getElement({my_map.id}).map;
                
                // Attach the shadow!
                var shadow = L.terminator();
                shadow.addTo(my_leaflet_map);
                
                // Update the shadow every 60 seconds
                setInterval(function() {{
                    shadow.setTime();
                }}, 60000);
            }};
            
            // 3. Inject the script into the page to start the download
            document.head.appendChild(script);
        '''
        ui.run_javascript(js_code)

    ui.timer(0.1, setup_nighttime, once=True)


    # every five seconds, update all drawn lines

    def update_cycle():
        global cycle_counter
        global force_update
        cycle_counter+=1

        #print("working")
        #print(force_update)
        if (force_update == True):
            print("updating...")
            for layer in list(my_map.layers)[1:]:
                if layer != user_marker:
                    my_map.remove_layer(layer)
            API.update_selected(list(selected_satellites))
            API.update_tles()
            for sat in selected_satellites:
                path = API.get_path(sat)
                ds.drawSatellite(my_map, path[0][0], path[0][1], grv.getVisRad(path[0][2]), path, 'rgb(250, 0, 0)')
            force_update = False
            
        if (cycle_counter % 60 == 0):
            # update countdowns every minute
            # clear map except for actual map layer
            for layer in list(my_map.layers)[1:]:
                if layer != user_marker:
                    my_map.remove_layer(layer)
            # update list of selected sats in API class
            API.update_selected(list(selected_satellites))
            # loop through sats, updating there path and drawing the update path, icon, and circle.
            for sat in selected_satellites:
                path = API.get_path(sat)
                ds.drawSatellite(my_map, path[0][0], path[0][1], grv.getVisRad(path[0][2]), path, 'rgb(250, 0, 0)')
            cycle_counter = 0
                

    # main loop of webpage
    ui.timer(1.0, update_cycle)
    #ui.timer(60.0, update_countdown_times)

    



if __name__ in {"__main__", "__mp_main__"}:
    markers = []
    ui.run(title="Satellite App", reload=False)