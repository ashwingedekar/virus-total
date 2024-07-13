import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Disable SSL verification warnings (not recommended for production)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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

# Function to fetch device type ID
def get_device_type_id(device_type_name):
    return get_object_id_by_name('dcim/device-types', device_type_name)

# Function to fetch device role ID
def get_device_role_id(device_role_name):
    return get_object_id_by_name('dcim/device-roles', device_role_name)

# Function to fetch site ID
def get_site_id(site_name):
    return get_object_id_by_name('dcim/sites', site_name)

# Function to fetch rack ID
def get_rack_id(rack_name):
    return get_object_id_by_name('dcim/racks', rack_name)

# Example usage to get IDs
try:
    # Fetch IDs for specific objects
    device_type_name = "FortiGate 60F"
    device_type_id = get_device_type_id(device_type_name)
    print(f"Device type '{device_type_name}' has ID: {device_type_id}")

    device_role_name = "Switch"
    device_role_id = get_device_role_id(device_role_name)
    print(f"Device role '{device_role_name}' has ID: {device_role_id}")

    site_name = "CDC-TP"
    site_id = get_site_id(site_name)
    print(f"Site '{site_name}' has ID: {site_id}")

    rack_name = "L-15"
    rack_id = get_rack_id(rack_name)
    print(f"Rack '{rack_name}' has ID: {rack_id}")

except Exception as e:
    print(f"Error: {e}")
