import csv
import json

def add_capacities_to_english(english_data: dict, csv_file_path: str) -> dict:
    """
    Add capacities from the CSV file to the English JSON structure.

    Args:
        english_data (dict): The English JSON structure to be updated.
        csv_file_path (str): Path to the CSV file containing capacities.

    Returns:
        dict: The updated English JSON with capacities added.
    """
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extract details from CSV row
            dimension = row['dimension'].lower()
            category = row['category']
            indicator = row['indicator']
            capacities = [
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

            # Find the dimension, category, and indicator in the English JSON
            if dimension in english_data:
                dimension_data = english_data[dimension]
                for category_key, category_data in dimension_data.items():
                    if isinstance(category_data, dict) and category_data.get("name") == category:
                        for indicator_key, indicator_data in category_data.items():
                            if isinstance(indicator_data, dict) and indicator_data.get("name") == indicator:
                                # Add capacities to the corresponding indicator
                                indicator_data["capacities"] = capacities
    return english_data


def copy_capacities_to_ukrainian(english_data: dict, ukrainian_data: dict) -> dict:
    """
    Copy the capacities from the English JSON to the Ukrainian JSON.

    Args:
        english_data (dict): The English JSON structure containing the capacities.
        ukrainian_data (dict): The Ukrainian JSON structure to be updated.

    Returns:
        dict: The updated Ukrainian JSON with capacities added.
    """
    for dimension_key, dimension_value in english_data.items():
        if dimension_key in ukrainian_data:
            for category_key, category_value in dimension_value.items():
                if isinstance(category_value, dict) and category_key in ukrainian_data[dimension_key]:
                    ukrainian_category = ukrainian_data[dimension_key][category_key]
                    for indicator_key, indicator_value in category_value.items():
                        if isinstance(indicator_value, dict) and indicator_key in ukrainian_category:
                            ukrainian_indicator = ukrainian_category[indicator_key]
                            ukrainian_indicator["capacities"] = indicator_value.get("capacities", [])
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
csv_file_path = "capacity_all.csv"  # Path to the CSV file
english_file_path = "basic_en.json"  # Path to the English JSON file
ukrainian_file_path = "basic_ua.json"  # Path to the Ukrainian JSON file
updated_english_file_path = "basic_en_updated.json"  # Path to save the updated English JSON file
updated_ukrainian_file_path = "basic_ua_updated.json"  # Path to save the updated Ukrainian JSON file

# Load the data
with open(english_file_path, "r", encoding="utf-8") as english_file:
    english_data = json.load(english_file)

with open(ukrainian_file_path, "r", encoding="utf-8") as ukrainian_file:
    ukrainian_data = json.load(ukrainian_file)

# Add capacities to the English JSON
english_data_with_capacities = add_capacities_to_english(english_data, csv_file_path)

# Save the updated English JSON
export_to_json(english_data_with_capacities, updated_english_file_path)

# Update the Ukrainian JSON with the capacities from the updated English JSON
updated_ukrainian_data = copy_capacities_to_ukrainian(english_data_with_capacities, ukrainian_data)

# Save the updated Ukrainian JSON
export_to_json(updated_ukrainian_data, updated_ukrainian_file_path)
