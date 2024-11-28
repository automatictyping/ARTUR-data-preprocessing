import json
import random
from shapely.geometry import Point, Polygon
import geopandas as gpd
import numpy as np
from faker import Faker

# generate random points within the city's boundary
def generate_random_point_in_polygon(polygon, num_points=10):
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < num_points:
        random_point = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(random_point):
            points.append(random_point)
    return points
# generate a random polygon within the city's boundary
def generate_random_polygon_in_boundary(polygon, num_polygons=5):
    polygons = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(polygons) < num_polygons:
        # Randomly create a small box-like polygon
        random_center = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        size = random.uniform(0.001, 0.005)  # Adjust the size of the polygons as needed
        random_polygon = Polygon([
            (random_center.x - size, random_center.y - size),
            (random_center.x + size, random_center.y - size),
            (random_center.x + size, random_center.y + size),
            (random_center.x - size, random_center.y + size),
            (random_center.x - size, random_center.y - size)
        ])
        # Ensure the random polygon is within the city's boundary
        if polygon.contains(random_polygon):
            polygons.append(random_polygon)
    return MultiPolygon(polygons)
# generate layers
def generate_emergency_water_point(boundary_polygon, city):
    # Generate Emergency Water Data Set
    num_points = 5 if city == "nikopol" else 10
    points = generate_random_point_in_polygon(boundary_polygon, num_points)
    # Create GeoJSON feature collection
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }
    # Constants
    tank_types = ["elevated tank", "underground tank/cistern", "mobile tank/tanks"]
    user_types = ["residential", "commercial", "industry", "public use", "other"]
    for i, point in enumerate(points):
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [point.x, point.y]
            },
            "properties": {
                "id": i + 1,
                "tank_type": random.choice(tank_types), # Random type from tank_types
                "capacity": np.random.randint(1000, 4000),  # Random numerical attribute
                "user_type": random.choice(user_types) # Random type from user_types
            }
        }
        geojson_data["features"].append(feature)
    # Save to file
    geojson_string = json.dumps(geojson_data, indent=2)
    with open(f'generated_{city}_emergency_water.geojson', 'w') as f:
        f.write(geojson_string)
def generate_water_source(boundary_polygon, city):
    num_points = 10 if city == "nikopol" else 20
    points = generate_random_point_in_polygon(boundary_polygon, num_points)
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }
    # Constants
    usage = ["drinking", "irrigation", "industry"]
    # Step 1: Generate initial random values for share_total_service
    initial_values = [random.uniform(1, 10) for _ in range(num_points)]
    # Step 2: Scale values so that their sum is exactly 100
    total_initial = sum(initial_values)
    share_total_service_values = [(value / total_initial) * 100 for value in initial_values]
    for i, (point,share_value) in enumerate(zip(points, share_total_service_values)):
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [point.x, point.y]
            },
            "properties": {
                "id": i + 1,
                "location_intake": [point.x, point.y],
                "capacity [m*3]": np.random.randint(30, 1000),
                "share_total_service [%]": round(share_value, 2),
                "usage": random.choice(usage) # Random type from user_types
            }
        }
        geojson_data["features"].append(feature)
    
    # Adjust final sum to ensure it's exactly 100 (due to rounding)
    sum_share_total_service = sum(f["properties"]["share_total_service [%]"] for f in geojson_data["features"])
    difference = 100 - sum_share_total_service
    geojson_data["features"][-1]["properties"]["share_total_service [%]"] += round(difference, 2)
    # Save to file
    geojson_string = json.dumps(geojson_data, indent=2)
    with open(f'generated_{city}_water_source.geojson', 'w') as f:
        f.write(geojson_string)
def generate_emergency_energy_supply(boundary_polygon, city):
    num_points = 1 if city == "nikopol" else 2
    points = generate_random_point_in_polygon(boundary_polygon, num_points)
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }
    type_source = ["microgrid", "battery", "solar", "thermal"]
    user_types = ["residential", "commercial", "industry", "public use", "other"]
    for i, point in enumerate(points):
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [point.x, point.y]
            },
            "properties": {
                "id": i + 1,
                "type_source": random.choice(type_source),
                "capacity [GWh]": np.random.randint(3000, 5000),
                "user_type": random.choice(user_types)
            }
        }
        geojson_data["features"].append(feature)

    geojson_string = json.dumps(geojson_data, indent=2)
    with open(f'generated_{city}_emergency_energy_supply.geojson', 'w') as f:
        f.write(geojson_string)    
def generate_energy_supply(boundary_polygon, city):
    num_points = 4 if city == "nikopol" else 8
    points = generate_random_point_in_polygon(boundary_polygon, num_points)
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }
    energy_source_type = ["smallCHP", "wind", "solar", "mediumCHP"]
    user_types = ["residential", "commercial", "industry", "public use", "other"]
    for i, point in enumerate(points):
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [point.x, point.y]
            },
            "properties": {
                "id": i + 1,
                "energy_source_type": random.choice(energy_source_type),
                "capacity [GWh]": np.random.randint(3000, 5000),
                "user_type": random.choice(user_types)
            }
        }
        geojson_data["features"].append(feature)

    geojson_string = json.dumps(geojson_data, indent=2)
    with open(f'generated_{city}_energy_supply.geojson', 'w') as f:
        f.write(geojson_string)      
def generate_heat_line(city):
    # Load the existing GeoJSON file
    input_file = f"{city}_road.geojson"
    output_file = f"generated_{city}_heating_network.geojson"

    with open(input_file, "r") as f:
        geojson_data = json.load(f)

    # Update each feature: delete original properties and add new random properties
    for feature in geojson_data["features"]:
        # Delete the original properties
        feature["properties"] = {}

        # Add new random properties
        feature["properties"]["heat_line_density [Mwh/m*a)]"] =  np.random.randint(1, 30)
    # Save the updated GeoJSON file
    with open(output_file, "w") as f:
        json.dump(geojson_data, f, indent=2)
def generate_waste_water_system(city):
    # Load the existing GeoJSON file
    input_file = f"{city}_road.geojson"
    output_file = f"generated_{city}_waste_water_system.geojson"

    with open(input_file, "r") as f:
        geojson_data = json.load(f)

    service = ["by neighbourhood", "by network connection"]
    pipeline_type = ["main", "secondary", "tertiary"]
    material = ["concrete", "metal", "PVC"]
    for i, feature in enumerate(geojson_data["features"]):
        feature["properties"] = {}
        feature["properties"]["id"] =  i + 1
        feature["properties"]["location_service"] = random.choice(service)
        feature["properties"]["year_of_construction"] = np.random.randint(1940, 2024)
        feature["properties"]["pipeline_type"] = random.choice(pipeline_type)
        feature["properties"]["material"] = random.choice(material)
    # Save the updated GeoJSON file
    with open(output_file, "w") as f:
        json.dump(geojson_data, f, indent=2)

citys = ["kryvyirih","nikopol"]
for city in citys:
    # generate_waste_water_system(city)
    gdf = gpd.read_file(f'{city}_boundary.geojson')
    boundary_polygon = gdf.geometry[0]
    # generate_emergency_water_point(boundary_polygon, city)
    # generate_water_source(boundary_polygon,city)
    # generate_emergency_energy_supply(boundary_polygon, city)
    generate_energy_supply(boundary_polygon, city)