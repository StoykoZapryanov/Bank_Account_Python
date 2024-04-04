from flask import request, jsonify, Blueprint
from .data_processing import parse_csv_file

# Create a Blueprint object
main_bp = Blueprint('main', __name__)

# Load data from CSV files
country_data = parse_csv_file('project/data/opportunities_country.csv', key_field_name='country', value_field_name='opps')
browser_data = parse_csv_file('project/data/opportunities_browser.csv', key_field_name='browsername', value_field_name='opps')
platform_data = parse_csv_file('project/data/opportunities_platform.csv', key_field_name='platformname', value_field_name='opps')
vertical_data = parse_csv_file('project/data/opportunities_vertical.csv', key_field_name='publishernewthematic', value_field_name='opps')

# Precompute total opportunities
total_opportunities = sum(country_data.values())

@main_bp.route('/estimate_traffic', methods=['GET'])
def estimate_traffic():
    def filter_data(selected_items, data): # If needed
        """
        Filter data based on selected items.
        """
        print("Selected Items:", selected_items)
        if not selected_items:
            return data
        filtered_data = {key: value for key, value in data.items() if key in selected_items}
        return filtered_data

    def combine_filtered_data(filtered_browser_data, filtered_platform_data, filtered_vertical_data):
        """
        Combine filtered data from different dimensions.
        """
        combined_data = {}
        # Combine the filtered data from different dimensions
        for browser, browser_value in filtered_browser_data.items():
            for platform, platform_value in filtered_platform_data.items():
                for vertical, vertical_value in filtered_vertical_data.items():
                    key = f"{browser}-{platform}-{vertical}"
                    combined_value = min(browser_value, platform_value, vertical_value)
                    combined_data[key] = combined_value
        return combined_data

    browser = request.args.getlist('browser')
    platform = request.args.getlist('platform')
    vertical = request.args.getlist('vertical')
    country = request.args.getlist('country')
    total_request_count = int(request.args.get('total_request_count', 0))

    # Filter data based on user-defined *if needed* criteria
    filtered_browser_data = filter_data(browser, browser_data)
    filtered_platform_data = filter_data(platform, platform_data)
    filtered_vertical_data = filter_data(vertical, vertical_data)

    # Combine the filtered data from different dimensions
    filtered_data = combine_filtered_data(filtered_browser_data, filtered_platform_data, filtered_vertical_data)

    # Calculate total filtered opportunities
    total_filtered_opportunities = sum(filtered_data.values())

    # Calculate estimated traffic count
    estimated_traffic = calculate_traffic(filtered_data, total_request_count)

    return jsonify({'estimated_traffic': estimated_traffic})

def calculate_traffic(filtered_data, total_request_count):
    """
    Calculate estimated traffic count based on filtered data.
    """
    total_filtered_opportunities = sum(filtered_data.values())
    
    if total_filtered_opportunities == 0:
        return 0
    
    return int(total_request_count * total_filtered_opportunities / total_opportunities)