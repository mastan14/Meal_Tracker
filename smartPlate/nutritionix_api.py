# nutritionix_api.py
import requests

# Nutritionix API credentials
APP_ID = "1c9ab77d"  # Replace with your APP_ID
APP_KEY = "4549252b1b6144f7fad45d504e1eace1"  # Replace with your APP_KEY

def get_nutritional_info(food_query):
    """
    Fetch nutritional information for a food item using the Nutritionix API.
    """
    # API endpoint
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"

    # Request headers
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": APP_KEY,
        "Content-Type": "application/json"
    }

    # Request body
    data = {
        "query": food_query
    }

    # Send the request
    response = requests.post(url, json=data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        result = response.json()
        return result["foods"]
    else:
        # Handle errors
        print(f"Error: {response.status_code} - {response.text}")
        return None