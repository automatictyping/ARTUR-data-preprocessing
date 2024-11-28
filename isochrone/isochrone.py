import csv
import requests
import json
import subprocess

def dissolve_geojson(input_file, output_file, range):
    sql_query = f"SELECT {range}, ST_Union(geometry) AS geometry FROM {input_file} GROUP BY {range}"
    # ogr2ogr command to dissolve polygons
    command = [
        'ogr2ogr',
        '-f', 'GeoJSON',
        output_file + ".geojson", 
        input_file + ".geojson",
        '-dialect', 'sqlite',
        '-sql', sql_query
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Polygons dissolved successfully into: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error dissolving polygons: {e}")
def import_geojson_to_db(table_name):
    geojson = table_name + ".geojson"
    postgis_connection = "PG:host=localhost dbname=ARTUR user=postgres password=123456 port=5432"

    try:
        subprocess.run(["ogr2ogr", "-f", "PostgreSQL", postgis_connection, geojson, "-nln", table_name, "-append"], check=True)
        print(f"Successfully imported {geojson} into PostGIS DB ARTUR")
    except subprocess.CalledProcessError as e:
        print(f"Error importing GeoJSOnN to postGIS: {e}")

def valhallaAPI(points, minutes, name, mode):
    # generate the result json files via time interval
    for minute in minutes:
        for point in points:
            # url for valhalla
            setting = {"locations":[{"lat":point[2],"lon":point[1]}],"costing":mode,"contours":[{"time":minute}],"polygons":True, "reverse":True}
            url = "http://localhost:8002/isochrone"

            try:
                # Send the request
                response = requests.post(url, json=setting)

                # Ensure that the request was successful
                if response.status_code != 200:
                    print(f"Error: Received status code {response.status_code} for point {point}")
                    continue

                # Parse the response JSON
                data = response.json()

                # Check if 'features' exist in the response
                if 'features' in data:
                    for feature in data['features']:
                        # Remove unnecessary properties
                        del feature['properties']['fillOpacity']
                        del feature['properties']['fill-opacity']
                        del feature['properties']['fill']
                        del feature['properties']['fillColor']
                        del feature['properties']['opacity']
                        del feature['properties']['color']
                        del feature['properties']['metric']

                    features = data['features']
                    combined_features.extend(features)
                else:
                    print(f"Warning: 'features' key not found in the response for point {point}. Full response: {data}")

            except requests.exceptions.RequestException as e:
                print(f"Error: Failed to connect to Valhalla API for point {point}. Exception: {e}")

        combined_geojson = {
            "type": "FeatureCollection",
            "features": combined_features
        }
    input_geojson = f"{name}_Hospital_{mode}_Isochrone_Original"
    output_geojson =  f"{name}_Hospital_{mode}_Isochrone"
    # Store geojson data to file
    with open(input_geojson + ".geojson", "w") as json_file:
        json.dump(combined_geojson, json_file, indent=2)
    # Call the dissolve function
    dissolve_geojson(input_geojson, output_geojson, "contour")
    # import dissolved polygons to postgis database
    import_geojson_to_db(output_geojson)
def geoapifyAPI(points, minutes, name, mode):
    # api key for Geoapify API
    API_KEY = "12e631cf1f4d432eb0c40b4c642cc511"
    combined_features = []
    for minute in minutes:
        for point in points:
            # url for Geoapify API
            url = f"https://api.geoapify.com/v1/isoline?lat={point[2]}&lon={point[1]}&type=time&mode={mode}&range={minute*60}&apiKey={API_KEY}"

            # response for Geoapify and Mapbox API
            response = requests.get(url)
            data = response.json()
            # modify json data from Geoapify
            for feature in data['features']:
                del feature['properties']['type']
                del feature['properties']['mode']
                del feature['properties']['lat']
                del feature['properties']['lon']
                del feature['properties']['id']
                feature['properties']['range'] /= 60

            features = data['features']
            combined_features.extend(features)

        combined_geojson = {
            "type": "FeatureCollection",
            "features": combined_features
        }
    # store geojson data to file
    input_geojson = f"{name}_Hospital_{mode}_Isochrone_Geoapify_Original"
    output_geojson = f"{name}_Hospital_{mode}_Isochrone_Geoapify"
    with open(input_geojson + ".geojson", "w") as json_file:
        json.dump(combined_geojson, json_file, indent=2)
    # dissolve the polygons via time range
    dissolve_geojson(input_geojson, output_geojson, "range")
    # import the dissolved data to postgis database
    import_geojson_to_db(output_geojson)
# def mapboxAPI(points, minutes, name, mode):
#     # access token for Mapbox API
#     ACCESS_TOKEN = "pk.eyJ1IjoiYmFyZGJvIiwiYSI6ImNrZzkxbnlsZzA5M3gzMnF4NDgwOTV2YjEifQ.WqJJ6FosmvYhPj828tPUDw"
#     url = f"https://api.mapbox.com/isochrone/v1/mapbox/walking/{point[1]}%2C{point[2]}?contours_minutes={minute}&polygons=true&access_token={ACCESS_TOKEN}"
if __name__ == "__main__":
    name = "Nikopol"
    mode = "bicycle"
    f = open(f'{name}_Hospital.csv', 'r')
    csvreader = csv.reader(f)
    points = list(csvreader)[1:]
    minutes = [1,2,3,4,5,6,7,8,9,10]
    combined_features = []
    valhallaAPI(points, minutes, name, mode)
    # geoapifyAPI(points, minutes, name, mode)