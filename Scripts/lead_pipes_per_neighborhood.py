import geopandas as gpd
import json
import pandas as pd
import time
from shapely.geometry import shape, GeometryCollection, Point



# Reading in the GeoJSON file as a JSON file
with open('../Data/Syracuse_Neighborhoods_2327829995554664018.geojson', 'r') as n:
    syr_nhood_json = json.load(n)
with open('../Data/syracuse_zip_codes.geojson', 'r') as z:
    syr_zip_json = json.load(z)



# Read in the Lead Pipe Locations data; 41,126 Pipes
pipes = pd.read_csv("../Data/Water_Services.csv")

# Selecting only the Coordinates and pipe type
pipes = pipes[['X', 'Y', 'PTYPE']]

# Filtering for only the LEAD pipes; 17,143 Lead Pipes
lead_pipes = pipes.loc[pipes['PTYPE'] == 'LEAD     ']

# Rename the X and Y Columns
lead_pipes.rename(columns = {'X':'Longitude', 'Y':'Latitude'}, inplace = True)



# Translating Pipe Coordinates to their Neighborhoods
# Start Timer
start = time.time()

# Create a blank list to hold the name of the neighborhood the pipe is located in
neighborhood_list = []

# For each lead pipe...
for row in lead_pipes.iterrows():
    # Format the Pipe Longitude and Latitude as a Point Object
    coordinates = lead_pipes.loc[row[0], ['Longitude', 'Latitude']]
    pipe_location = Point(coordinates)

    # Set the default neighborhood name to match the case where the pipe is not
    # in any of the map bounds
    pipe_neighborhood = 'Outside Bounds'

    # For each of the neighborhoods in the shape file...
    for feature in syr_nhood_json['features']:
        # Set the bounds to the coordinates of the neighborhood
        neighborhood_boundaries = shape(feature['geometry'])

        # If the pipe location is within the bounds of the neighborhood...
        # Change the default neighborhood name to the one it is in
        if neighborhood_boundaries.contains(pipe_location):
            pipe_neighborhood = feature['properties']['Name']

    # Append the name of the neighborhood that contains the pipe if any match,
    # or the default "Outside Bounds" tag if not
    neighborhood_list.append(pipe_neighborhood)

# Set the neighborhood column equal to the neighborhood List
lead_pipes['Neighborhood'] = neighborhood_list

# End Timer
end = time.time()

# Print Translation Operation Time
print(f'Time Elapsed: {round(end - start, 1)} seconds')



# Get the lead pipe counts for each neighborhood
neighborhood_counts = lead_pipes.groupby(['Neighborhood']).size().to_frame(name = 'Count').reset_index()
# Sort the rows by the Count
sorted_counts = neighborhood_counts.sort_values(['Count'], ascending = False).reset_index(drop = True)

print(sorted_counts)
