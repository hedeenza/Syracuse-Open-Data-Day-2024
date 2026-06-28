import geopandas as gpd
import json
import pandas as pd



# Read in the Zip Codes & NEIGHBORHOODS GeoJSON shape-files using Geopandas
syr_zip = gpd.read_file("../Data/syracuse_zip_codes.geojson")
# Read in the NEIGHBORHOODS GeoJSON shape-file using Geopandas
syr_nhood = gpd.read_file('../Data/Syracuse_Neighborhoods_2327829995554664018.geojson')

# Converting the GeoJSON file to a JSON file
syr_zip_json = syr_zip.to_json(drop_id = True)
syr_nhood_json = syr_nhood.to_json(drop_id = True)



# Read in the Lead Pipe Locations data; 41,126 Pipes
pipes = pd.read_csv("../Data/Water_Services.csv")

# Selecting only the Coordinates and pipe type
pipes = pipes[['X', 'Y', 'PTYPE']]

# Filtering for only the LEAD pipes; 17,143 Lead Pipes
lead_pipes = pipes.loc[pipes['PTYPE'] == 'LEAD     ']

# Rename the X and Y Columns
lead_pipes.rename(columns = {'X':'Longitude', 'Y':'Latitude'}, inplace = True)
