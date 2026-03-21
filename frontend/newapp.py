from nicegui import ui
import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import passpredictor

# list of all satellites
satellite_dict = {"ISS": (), "Hubble": (), "Starlink-1": (), "Landsat": ()} # lil test
my_list = passpredictor.get_satellites()
satellite_dict = {item: None for item in my_list} # set dict to have the sat names as keys
# list of selected satellites to show on map
selected_satellites = set()

@ui.page('/')
def main_page():
    # resets on page reload
    satellite_ui_elements = {}

    # filter satellites
    def filter_satellites(e):
        # e.value gets the text typed into the input
        search_term = e.value.lower()
        for name, button in satellite_ui_elements.items():
            button.set_visibility(search_term in name.lower())
    
    # select satellite
    def select_satellite(sat_name, btn_object):
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
            
        # Popup for tracking
        #ui.notify(f'Tracking: {list(selected_satellites)}')

    # 1. Sidebar 
    with ui.left_drawer(value=True).classes('bg-gray-100 p-4 flex flex-col'):
        
        # 2. Search Bar
        ui.input('Search satellites...', on_change=filter_satellites).classes('w-full mb-4')
        
        # The scroll area for the buttons
        with ui.scroll_area().classes('w-full flex-grow border p-2'):
            for key in satellite_dict.keys():
                # Create button with default light grey color
                btn = ui.button(key, color="grey-4").classes('w-full mb-2 text-black')
                
                # Add to our dictionary so the search bar can find it
                satellite_ui_elements[key] = btn
                
                # lock in 'key' and 'btn' for this specific loop iteration
                btn.on_click(lambda e, k=key, b=btn: select_satellite(k, b))
            
    # 3. Map & Starting Marker
    my_map = ui.leaflet(center=(20, 0), zoom=2).classes('w-full h-screen')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Satellite App", reload=False)