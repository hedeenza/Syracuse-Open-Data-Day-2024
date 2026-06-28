import geopandas as gpd
import pandas as pd
import folium
import folium.plugins
import webbrowser

# Load in the Neighborhood outlines and Lead Pipe Counts by Neighborhood
syr_nhood = gpd.read_file('../Data/Syracuse_Neighborhoods_2327829995554664018.geojson')
# Converting the GeoJSON file to a JSON file
syr_nhood_json = syr_nhood.to_json(drop_id = True)

lead_pipes_by_neighborhood = pd.read_csv('lead_pipes_by_neighborhood.csv')

# Point the map to Syracuse
map = folium.Map(
    location = [43.035, -76.1455],
    tiles = None,
    zoom_start = 13
)

# Set the base map parameters and add to the map
base_map = folium.FeatureGroup(name = 'Base',
                               overlay = True,
                               control = False)
folium.TileLayer(tiles = 'cartodb positron').add_to(base_map)
base_map.add_to(map)



# Add a Choropleth layer representing Lead Pipe Counts by Neighborhood
folium.Choropleth(
    geo_data = syr_nhood_json, 
    name = 'Lead Pipes', 
    data = lead_pipes_by_neighborhood, 
    columns = ['Neighborhood', 'Count'], # specify the data frame's columns we want to use
    key_on = 'feature.properties.Name', 
    bins = 10,
    fill_color = 'YlOrRd',
    fill_opacity = 0.7,
    line_opacity = 0.2,
    overlay = False,
    control = True,
    show = True,
    legend_name = 'Lead Pipe Locations by Neighborhood, 2023'
).add_to(map) 



# Adding the Layer Control
folium.LayerControl(collapsed = False).add_to(map)

# Adding Mouse-Position Coordinates Support
folium.plugins.MousePosition().add_to(map)

# Adding Full-Screen Support
folium.plugins.Fullscreen(
        position = 'bottomright',
        title = 'Full Screen',
        title_cancel = 'Return',
        force_separate_button = True
).add_to(map)



# Display the map by saving it as an html, then opening it with the browser
map.save('lead_nhood.html')
webbrowser.open('lead_nhood.html')
