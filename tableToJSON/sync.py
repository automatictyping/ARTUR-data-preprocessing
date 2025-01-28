import json

def copy_capacities_to_ukrainian(english_data: dict, ukrainian_data: dict) -> dict:
    """
    Copy the capacities from the English JSON to the Ukrainian JSON.
    Replace the Ukrainian indicator strings with a dictionary containing the name and capacities.
    
    Args:
        english_data (dict): The English JSON structure containing the capacities.
        ukrainian_data (dict): The Ukrainian JSON structure to be updated.
    
    Returns:
        dict: The updated Ukrainian JSON with capacities added.
    """
    for dimension_key, dimension_value in english_data.items():
        if dimension_key in ukrainian_data:
            # Iterate over categories
            for category_key, category_value in dimension_value.items():
                if isinstance(category_value, dict) and category_key in ukrainian_data[dimension_key]:
                    ukrainian_category = ukrainian_data[dimension_key][category_key]
                    # Iterate over indicators
                    for indicator_key, indicator_value in category_value.items():
                        if isinstance(indicator_value, dict) and indicator_key in ukrainian_category:
                            # Replace string with a dictionary containing name and capacities
                            ukrainian_category[indicator_key] = {
                                "name": ukrainian_category[indicator_key],
                                "capacities": indicator_value["capacities"]
                            }
    return ukrainian_data


def export_to_json(data: dict, file_path: str) -> None:
    """
    Export the data to a JSON file.
    
    Args:
        data (dict): The data to export.
        file_path (str): The output JSON file path.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    print(f"Data successfully exported to {file_path}")


# Example usage
english_file_path = "en.json"  # Path to the English JSON file
ukrainian_file_path = "ua.json"  # Path to the Ukrainian JSON file
output_file_path = "echarts_ua_updated.json"  # Path to save the updated Ukrainian JSON file

# Load the data
with open(english_file_path, "r", encoding="utf-8") as english_file:
    english_data = json.load(english_file)

with open(ukrainian_file_path, "r", encoding="utf-8") as ukrainian_file:
    ukrainian_data = json.load(ukrainian_file)

# Process the data
updated_ukrainian_data = copy_capacities_to_ukrainian(english_data, ukrainian_data)

# Export the updated Ukrainian data
export_to_json(updated_ukrainian_data, output_file_path)
