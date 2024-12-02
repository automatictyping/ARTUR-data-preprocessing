import pandas as pd
from dotenv import load_dotenv
import os
import requests
import geopandas as gpd
from shapely.geometry import Point

def get_lat_lon(address):
    # Load environment variables from .env file
    load_dotenv()
    address = address + ", Нікополь"
    mapbox_token = os.getenv("MAPBOX_TOKEN")
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json"

    params = {
        'access_token': mapbox_token,
        'limit': 1,  # Adjust the limit if needed
        'language': 'uk'  # Ukrainian language
    }
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['features']:
            coordinates = data['features'][0]['geometry']['coordinates']
            return coordinates[1], coordinates[0]
        else:
            return None, None
    else:
        print(f"Error: {response.status_code} for address: {address}")
        return None, None

file_path = "Nikopol_stagnent_rainfall"
df = pd.read_excel(file_path  + ".xlsx")

df['latitude'], df['longitude'] = zip(*df['address'].apply(get_lat_lon))

geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# gdf.set_crs("EPSG:4326", allow_override=True, inplace=True)

output_geojson_path = f"{file_path}.geojson"
gdf.to_file(output_geojson_path, driver='GeoJSON')

print(f"GeoJSON file saved as {output_geojson_path}")