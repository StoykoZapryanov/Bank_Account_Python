### Project Name: Traffic Estimation API

## Description:
The Traffic Estimation API is designed to estimate web traffic based on opportunities associated with various dimensions such as countries, browsers, platforms, and verticals. It provides a simple HTTP API endpoint /estimate_traffic to receive request parameters and return estimated traffic counts.

## Usage:
The API endpoint /estimate_traffic accepts GET requests with the following parameters:

total_request_count: Total number of requests to estimate traffic for.
browser: List of browser names to filter the opportunities (optional).
platform: List of platform names to filter the opportunities (optional).
vertical: List of vertical names to filter the opportunities (optional).
country: List of country names to filter the opportunities (optional).

## Example Request:
GET /estimate_traffic?total_request_count=1000000&browser=Chrome&platform=Android&vertical=280000000000

## Example Response:

{
    "estimated_traffic": 9918736
}


Contributions are welcome! Feel free to fork the repository, make improvements, and submit pull requests.

Support:
For any questions or issues, please contact [stoyko.zapryanov@gmail.com].