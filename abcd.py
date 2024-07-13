import requests

# Define the endpoint and API key
endpoint = "https://netbox.comtelindia.com:10750/api/"
api_key = "b1ee29670a7d598abb41f232d7fb01de6f2c470e"

# Define headers with the API key for authentication
headers = {
    "Authorization": f"Token {api_key}",
    "Content-Type": "application/json",
}

# Attempt to make a request to the API to test the connection
try:
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()  # Raise error for bad responses
    print("Success! Connected to NetBox API.")
except requests.exceptions.RequestException as e:
    print(f"Error connecting to NetBox API: {e}")
