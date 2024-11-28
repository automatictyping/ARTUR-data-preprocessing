import csv
import requests
import json
import subprocess

def dissolve_geojson(input_file, output_file, range_column):
    sql_query = f"SELECT {range_column}, ST_Union(geometry) AS geometry FROM {input_file} GROUP BY {range_column}"
    command = [
        'ogr2ogr',
        '-f', 'GeoJSON',
        f"{output_file}.geojson", 
        f"{input_file}.geojson",
        '-dialect', 'sqlite',
        '-sql', sql_query
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Polygons dissolved successfully into: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error dissolving polygons: {e}")

def import_geojson_to_db(table_name):
    geojson = f"{table_name}.geojson"
    postgis_connection = "PG:host=localhost dbname=ARTUR user=postgres password=123456 port=5432"

    try:
        subprocess.run(["ogr2ogr", "-f", "PostgreSQL", postgis_connection, geojson, "-nln", table_name, "-append"], check=True)
        print(f"Successfully imported {geojson} into PostGIS DB ARTUR")
    except subprocess.CalledProcessError as e:
        print(f"Error importing GeoJSON to PostGIS: {e}")

def determine_max_distance_water(capacity):
    """Determine maximum distance based on capacity."""
    if capacity <= 500:
        return 5
    elif capacity <= 1000:
        return 10
    return 0

def determine_max_distance_energy(capacity):
    """Determine maximum distance based on capacity."""
    if capacity <= 500:
        return 5
    elif capacity <= 5000:
        return 10
    return 0

def valhallaAPI(points, name, mode):
    combined_features = []
    for point in points:
        try:
            lat, lon, capacity = float(point[1]), float(point[2]), float(point[3])
            max_distance = determine_max_distance_energy(capacity)
            
            # Generate five isochrone ranges proportionally up to the max distance
            ranges = [max_distance * fraction for fraction in [0.2, 0.4, 0.6, 0.8, 1]]
            
            for range_distance in ranges:
                # Prepare the request payload
                setting = {
                    "locations": [{"lat": lat, "lon": lon}],
                    "costing": mode,
                    "contours": [{"distance": range_distance}],
                    "polygons": True
                }
                url = "http://localhost:8002/isochrone"
                try:
                    # Send the request
                    response = requests.post(url, json=setting)

                    # Ensure that the request was successful
                    if response.status_code != 200:
                        print(f"Error: Received status code {response.status_code} for point {point}")
                        continue
                    data = response.json()
                    if 'features' in data:
                        # Modify JSON data from the response
                        for feature in data['features']:
                            feature['properties']['range_km'] = range_distance
                            feature['properties']['capacity'] = capacity
                        combined_features.extend(data['features'])
                    else:
                        print(f"Warning: 'features' key not found in the response for point {point}. Full response: {data}")
                except requests.RequestException as e:
                    print(f"Error making request for point {point}: {e}")
        except ValueError as e:
            print(f"Error processing point {point}: {e}")

    combined_geojson = {
        "type": "FeatureCollection",
        "features": combined_features
    }

    # Store GeoJSON data to file
    input_geojson = f"generated_{name}_energy_supply_Catchment_Original"
    output_geojson = f"generated_{name}_energy_supply_Catchment"
    with open(f"{input_geojson}.geojson", "w") as json_file:
        json.dump(combined_geojson, json_file, indent=2)
    # Dissolve the polygons via range_km
    dissolve_geojson(input_geojson, output_geojson, "range_km")
    # Optionally import the dissolved data to PostGIS database
    import_geojson_to_db(output_geojson)

if __name__ == "__main__":
    names = ["kryvyirih","nikopol"]
    mode = "auto"
    for name in names:
        try:
            with open(f'generated_{name}_energy_supply.csv', 'r') as f:
                csvreader = csv.reader(f)
                points = list(csvreader)[1:]  # Skip header
            valhallaAPI(points, name, mode)
        except FileNotFoundError as e:
            print(f"Error: {e}")
