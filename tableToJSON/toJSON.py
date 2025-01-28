import csv
import json
from typing import List, Dict

def parse_csv_to_echarts_json(file_path: str) -> Dict:
    """
    Parse a CSV table into the ECharts JSON structure with simplified categories and indicators.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        Dict: The resulting JSON structure.
    """
    # Initialize the ECharts structure
    echarts_data = {}

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract key details from the row
            dimension = row['dimension'].lower()
            category = row['category']
            indicator = row['indicator']
            values = [
                int(row['robustness']),
                int(row['redundancy']),
                int(row['inclusiveness']),
                int(row['diversity']),
                int(row['flexibility']),
                int(row['resourcefulness']),
                int(row['integration']),
                int(row['reflectiveness']),
                int(row['transparency'])
            ]

            # Ensure the dimension exists in the structure
            if dimension not in echarts_data:
                echarts_data[dimension] = {"name": dimension.upper()}

            # Initialize the category counter for each dimension
            if "category_counter" not in echarts_data[dimension]:
                echarts_data[dimension]["category_counter"] = 1

            # Create the category if it doesn't exist (based on the name)
            category_number = None
            for key, value in echarts_data[dimension].items():
                if isinstance(value, dict) and value.get("name") == category:
                    category_number = key
                    break
            
            if category_number is None:
                category_number = echarts_data[dimension]["category_counter"]
                echarts_data[dimension][category_number] = {"name": category}
                # Increment the category counter
                echarts_data[dimension]["category_counter"] += 1

            # Initialize the indicator counter for this category
            if "indicator_counter" not in echarts_data[dimension][category_number]:
                echarts_data[dimension][category_number]["indicator_counter"] = 1

            # Add the indicator to the correct category and dimension
            indicator_number = echarts_data[dimension][category_number]["indicator_counter"]
            echarts_data[dimension][category_number][indicator_number] = {
                "name": indicator,
                "capacities": values
            }

            # Increment the indicator counter
            echarts_data[dimension][category_number]["indicator_counter"] += 1

    # Remove the category_counter and indicator_counter from the final output
    for dimension in echarts_data:
        if "category_counter" in echarts_data[dimension]:
            del echarts_data[dimension]["category_counter"]
        for category_key in echarts_data[dimension]:
            if isinstance(echarts_data[dimension][category_key], dict):
                if "indicator_counter" in echarts_data[dimension][category_key]:
                    del echarts_data[dimension][category_key]["indicator_counter"]

    return echarts_data

def export_to_json(data: Dict, file_path: str) -> None:
    """
    Export the data to a JSON file.
    
    Args:
        data (Dict): The data to export.
        file_path (str): The output JSON file path.
    """
    with open(file_path, mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)
    print(f"Data successfully exported to {file_path}")


# Example Usage
csv_file_path = 'capacity_all.csv'  # Path to your input CSV file
output_file_path = 'en.json'  # Path to save the resulting JSON file

# Convert the CSV to the desired JSON structure
echarts_json = parse_csv_to_echarts_json(csv_file_path)

# Export the JSON data to a file
export_to_json(echarts_json, output_file_path)
