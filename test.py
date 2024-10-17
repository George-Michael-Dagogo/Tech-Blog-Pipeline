import requests

# Your API key

# Define the Google Places API endpoint for nearby searches
endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

# Define parameters for your request
params = {
    'location': '9.0820,8.6753',  # Latitude and longitude for a location in Nigeria (Abuja example)
    'radius': 5000000,               # Search within a 5km radius
    'type': 'school',             # Type of place (school)
    'key': api_key                # Your API key
}

# Make the request to the Places API
response = requests.get(endpoint_url, params=params)
print(response.json())
# Parse the response
if response.status_code == 200:
    school_data = response.json()
    schools = school_data.get('results', [])
    
    # Print out details of the schools
    for school in schools:
        print(f"School Name: {school['name']}")
        print(f"Address: {school.get('vicinity', 'N/A')}")
        print(f"Location: {school['geometry']['location']}")
        print("-" * 40)
else:
    print("Failed to retrieve data:", response.status_code)
