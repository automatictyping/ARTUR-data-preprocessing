import geopandas as gpd
import subprocess

def import_geojson_to_db(table_name):
    geojson = f"{table_name}.geojson"
    postgis_connection = "PG:host=localhost dbname=ARTUR user=postgres password=123456 port=5432"

    try:
        subprocess.run(["ogr2ogr", "-f", "PostgreSQL", postgis_connection, geojson, "-nln", table_name, "-append"], check=True)
        print(f"Successfully imported {geojson} into PostGIS DB ARTUR")
    except subprocess.CalledProcessError as e:
        print(f"Error importing GeoJSON to PostGIS: {e}")
def update_population_with_coverage(population_file, catchment_file, output_file):
    population_gdf = gpd.read_file(population_file)
    catchment_gdf = gpd.read_file(catchment_file)
    
    # Ensure both layers have the same CRS (coordinate reference system)
    if population_gdf.crs != catchment_gdf.crs:
        catchment_gdf = catchment_gdf.to_crs(population_gdf.crs)
    
    # Create a new attribute 'covered' to record coverage status
    population_gdf['covered'] = 0  # Initialize as 0 (not covered)
    
    # Check for coverage using spatial overlay
    for idx, pop_geom in population_gdf.iterrows():
        if catchment_gdf.intersects(pop_geom.geometry).any():
            population_gdf.at[idx, 'covered'] = 1
    
    population_gdf.to_file(output_file, driver='GeoJSON')
    print(f"Updated population GeoJSON file saved to: {output_file}")

cities = ["nikopol", "kryvyirih"]
for city in cities:
    population_file = f"{city}_population_vector.geojson"
    catchment_file = f"generated_{city}_water_source_Isochrone.geojson"
    output_file = f"generated_{city}_water_source_catchment_population.geojson"
    # Run the function
    update_population_with_coverage(population_file, catchment_file, output_file)
    import_geojson_to_db(f"generated_{city}_water_source_catchment_population")
