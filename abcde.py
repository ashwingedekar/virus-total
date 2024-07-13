import requests


# Disable SSL verification warnings (not recommended for production)

# Configuration
NETBOX_URL = 'https://netbox.comtelindia.com:10750/api'
HEADERS = {
    'Authorization': 'Token b1ee29670a7d598abb41f232d7fb01de6f2c470e',
    'Content-Type': 'application/json',
}

# Function to fetch object ID by name
def get_object_id_by_name(endpoint, name):
    url = f'{NETBOX_URL}/{endpoint}/?name={name}'
    response = requests.get(url, headers=HEADERS, verify=False)  # Disable SSL verification

    if response.status_code == 200:
        data = response.json()
        if data['count'] > 0:
            return data['results'][0]['id']
        else:
            raise Exception(f"Object '{name}' not found.")
    else:
        raise Exception(f"Failed to fetch object. Status code: {response.status_code}, Error: {response.text}")

# Example usage to get device type ID
try:
    device_type_name = "FortiGate 60F"
    device_type_id = get_object_id_by_name('dcim/device-types', device_type_name)
    print(f"Device type '{device_type_name}' has ID: {device_type_id}")
except Exception as e:
    print(f"Error: {e}")
