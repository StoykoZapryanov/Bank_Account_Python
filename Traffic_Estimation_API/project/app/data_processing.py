import csv

def parse_csv_file(file_path, key_field_name='key', value_field_name='opps'):
    """
    Parse a CSV file into a dictionary.
    
    Args:
    - file_path (str): Path to the CSV file.
    - key_field_name (str): Name of the field containing keys.
    - value_field_name (str): Name of the field containing values.
    
    Returns:
    - data (dict): Dictionary containing key-value pairs parsed from the CSV file.
    """
    data = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row[key_field_name]
            value = float(row[value_field_name])  # Assuming the value field contains float values
            data[key] = value
    return data
