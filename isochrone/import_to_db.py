import subprocess

def import_geojson_to_db(table_name):
    geojson = table_name + ".geojson"
    postgis_connection = "PG:host=localhost dbname=ARTUR user=postgres password=123456 port=5432"

    try:
        subprocess.run(["ogr2ogr", "-f", "PostgreSQL", postgis_connection, geojson, "-nln", table_name, "-append"], check=True)
        print(f"Successfully imported {geojson} into PostGIS DB ARTUR")
    except subprocess.CalledProcessError as e:
        print(f"Error importing GeoJSOnN to postGIS: {e}")

if __name__ == "__main__":
    import_geojson_to_db("generated_nikopol_energy_supply")