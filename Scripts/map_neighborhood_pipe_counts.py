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



# Adding Neighborhood Name Markers
neighborhood_markers = folium.FeatureGroup(
        name = 'Neighborhood Names',
        control = True,
        overlay = True,
        show = True
).add_to(map)

# Set the icon size
icon_size_values = (3, 3)

# Set the anchor values
icon_anchor_values = (25, 3)

# Create a dictionary that holds the neighborhood names and name locations
neighborhood_names = {
    'Lakefront': [43.06739, -76.17575],
    'Court-Woodlawn': [43.07755, -76.14449],
    'Washington Square': [43.07052, -76.15995],
    'Northside': [43.06563, -76.14518],
    'Sedgwick': [43.06726, -76.13058],
    'Eastwood': [43.06475, -76.10653],
    'Lincoln Hill': [43.0566, -76.12972],
    'Hawley-Green': [43.05359, -76.14054],
    'Prospect Hill': [43.05635, -76.14913],
    'Franklin Square': [43.05835, -76.15892],
    'Salt Springs': [43.05196, -76.10207],
    'Meadowbrook': [43.03953, -76.0988],
    'Near Eastside': [43.0492, -76.1241],
    'Westcott': [43.04079, -76.12079],
    'University Neighborhood': [43.02711, -76.12044],
    'South Campus': [43.01744, -76.11718],
    'University Hill': [43.04116, -76.13539],
    'Outer Comstock': [43.0182, -76.13298],
    'Downtown': [43.04782, -76.15033],
    'Southside': [43.02899, -76.14913],
    'Brighton': [43.01744, -76.14792],
    'North Valley': [43.00652, -76.14792],
    'South Valley': [42.99421, -76.14569],
    'Park Ave': [43.05171, -76.1718],
    'Near Westside': [43.04204, -76.16458],
    'Southwest': [43.03401, -76.15874],
    'Elmwood': [43.01832, -76.16201],
    'Strathmore': [43.02648, -76.17558],
    'Winkworth': [43.02849, -76.19121],
    'Skunk City': [43.03539, -76.1809],
    'Tipp Hill': [43.04512, -76.18537],
    'Far Westside': [43.05578, -76.19395],
}

# Add each name at the specified location
for neighborhood, location in neighborhood_names.items():
    folium.Marker(location = [location[0], location[1]],
                icon = folium.features.DivIcon(
                    icon_size = icon_size_values,
                    icon_anchor = icon_anchor_values,
                    html = f'<div style="font-size: 12; color:black;">{neighborhood}</div>')
    ).add_to(neighborhood_markers)



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
map.save('map_lead_pipes_by_neighborhood.html')
webbrowser.open('map_lead_pipes_by_neighborhood.html')
