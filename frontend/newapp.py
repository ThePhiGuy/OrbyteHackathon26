from nicegui import ui

# list of all satellites
satellite_list = {"ISS": (), "Hubble": (), "Starlink-1": (), "Landsat": ()}

# list of selected satellites to show on map
selected_satellites = set()

@ui.page('/')
def main_page():
    # We will define this INSIDE the page so it resets cleanly on reload
    satellite_ui_elements = {}

    # filter satellites
    def filter_satellites(e):
        # e.value gets the text typed into the input
        search_term = e.value.lower()
        for name, button in satellite_ui_elements.items():
            button.set_visibility(search_term in name.lower())
    
    # select satellite
    def select_satellite(sat_name, btn_object):
        # If it's already selected, DESELECT it
        if sat_name in selected_satellites:
            selected_satellites.remove(sat_name)
            btn_object.props('color=grey-4') # Back to light grey
        # If it's not selected, SELECT it
        else:
            selected_satellites.add(sat_name) # Sets use .add(), not .append()!
            btn_object.props('color=grey-9') # Turn dark grey
            
        # Popup for tracking
        ui.notify(f'Tracking: {list(selected_satellites)}')

    # 1. Sidebar 
    with ui.left_drawer(value=True).classes('bg-gray-100 p-4 flex flex-col'):
        
        # 2. Search Bar
        ui.input('Search satellites...', on_change=filter_satellites).classes('w-full mb-4')
        
        # The scroll area for the buttons
        with ui.scroll_area().classes('w-full flex-grow border p-2'):
            for key in satellite_list.keys():
                # Create button with default light grey color
                btn = ui.button(key, color="grey-4").classes('w-full mb-2')
                
                # Add to our dictionary so the search bar can find it
                satellite_ui_elements[key] = btn
                
                # The lambda trick: lock in 'key' and 'btn' for this specific loop iteration
                btn.on_click(lambda e, k=key, b=btn: select_satellite(k, b))
            
    # 3. Map & Starting Marker
    my_map = ui.leaflet(center=(20, 0), zoom=2).classes('w-full h-screen')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Satellite App", reload=False)