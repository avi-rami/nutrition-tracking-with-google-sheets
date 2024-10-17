# below is the link to the google sheet where the nutrition data goes
# https://docs.google.com/spreadsheets/d/1JZEgfo2denvivUNznoXYhPpinrkn-qpL5A8HtoX9veY/edit?usp=sharing

import requests
from datetime import datetime
import os

# Your API credentials for Nutritionix and Sheety
API_KEY = "20925788aa5c85ad22ca989a46d2c70c"
API_ID = "fc0c3937"

# Get the current date and time in the format "DD/MM/YYYY" and "HH:MM:SS"
date = datetime.now().strftime("%d/%m/%Y")
time = datetime.now().strftime("%H:%M:%S")

# Nutritionix API endpoint to retrieve nutrition data based on natural language queries
nutrition_endpoint = "https://trackapi.nutritionix.com/v2/natural/nutrients"

# Headers required by Nutritionix API, including content type, app ID, and API key
nutrition_headers = {
    "Content-Type": "application/json",
    "x-app-id": API_ID,
    "x-app-key": API_KEY
}

# Prompt the user to input the food items they ate
food_item = input("Tell me what food items you ate: ")

# Payload for the Nutritionix API, containing the user's food item input
nutrition_inputs = {
    "query": food_item
}

# Send a POST request to the Nutritionix API with the user's input and headers
r = requests.post(url=nutrition_endpoint, json=nutrition_inputs, headers=nutrition_headers)

# Parse the JSON response to get the list of food items and their nutritional information
food_data = r.json()["foods"]

# Sheety API endpoint to log the nutrition data into a Google Sheets document
sheety_endpoint = "https://api.sheety.co/dec0cb07ed88834cf675fc8a9bb97b2e/myFoodLog/nutritionFacts"

# Headers required by the Sheety API, specifying the content type
sheety_headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer thisissuperdupersecret"
}

# Loop through each food item in the response data
for item in food_data:
    # Create a dictionary with the nutrition facts for the current food item
    sheety_inputs = {
        "nutritionFact": {
            "date": date,
            "time": time,
            "quantity": item["serving_qty"],
            "unit": item["serving_unit"],
            "foodItem": item["food_name"],
            "calories": item["nf_calories"],
            "weight": item["serving_weight_grams"]
        }
    }
    # Send a POST request to the Sheety API to log the nutrition data in the Google Sheets document
    r = requests.post(url=sheety_endpoint, json=sheety_inputs, headers=sheety_headers)

    # Print the response from the Sheety API to verify the data was logged
    print(r.text)

