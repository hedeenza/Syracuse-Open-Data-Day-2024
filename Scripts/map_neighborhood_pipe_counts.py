import folium
import webbrowser

# Point the map to Syracuse
map = folium.Map(
    location = [43.0493, -76.1455],
    tiles = None,
    zoom_start=12
)

# Set the base map parameters and add to the map
base_map = folium.FeatureGroup(name = 'Base',
                               overlay = True,
                               control = False)
folium.TileLayer(tiles = 'cartodb positron').add_to(base_map)
base_map.add_to(map)

# Display the map by saving it as an html, then opening it with the browser
map.save('lead_nhood.html')
webbrowser.open('lead_nhood.html')
