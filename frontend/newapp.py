from nicegui import ui
import random

# list of all satellites
satellite_list = {"ISS" : (1)}


@ui.page('/')
def main_page():
    # 1. Sidebar
    with ui.left_drawer(value=True).classes('bg-gray-100 p-4'):
        with ui.column():
            with ui.scroll_area().classes('w-64 h-1000 border'):
                for key, value in satellite_list.items():
                    ui.chip(key, selectable=True)
            
    # 2. Map & Starting Marker
    my_map = ui.leaflet(center=(20, 0), zoom=2).classes('w-full h-screen')




if __name__ in {"__main__", "__mp_main__"}:
    # As long as PyQt6 is installed, this will open in a native app window!
    ui.run(title="Satellite App", reload=False)