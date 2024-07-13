import requests

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

# Function to create a new device type
def create_device_type(name, slug, model=None, vendor=None, part_number=None):
    url = f'{NETBOX_URL}/dcim/device-types/'
    payload = {
        'name': name,
        'slug': slug,
        'model': model,
        'vendor': vendor,
        'part_number': part_number,
    }
    response = requests.post(url, json=payload, headers=HEADERS, verify=False)  # Disable SSL verification

    if response.status_code == 201:
        data = response.json()
        return data['id']
    else:
        raise Exception(f"Failed to create device type. Status code: {response.status_code}, Error: {response.text}")

# Example usage to create a new device type for PDU non-racked device
try:
    device_type_name = "PDU non-racked device"
    device_type_slug = "pdu-non-racked-device"
    device_type_id = create_device_type(device_type_name, device_type_slug)
    print(f"Device type '{device_type_name}' created with ID: {device_type_id}")
except Exception as e:
    print(f"Error: {e}")

def get_site_id(site_name):
    return get_object_id_by_name('dcim/sites', site_name)

try:
    # Fetch IDs for specific objects
   
    site_name = "CDC-TP"
    site_id = get_site_id(site_name)
    print(f"Site '{site_name}' has ID: {site_id}")


except Exception as e:
    print(f"Error: {e}")