import json
import requests
from bs4 import BeautifulSoup

# URL of the API endpoint (hypothetical example)
api_url = "https://webshop.broodenbanketmartens.be/be-nl/martens"

# Make a GET request to the API endpoint
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Process the data as needed
    print(json.dumps(data, indent=4))
else:
    print("Failed to fetch data from the API")
