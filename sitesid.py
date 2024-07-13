import requests

NETBOX_URL = 'https://netbox.comtelindia.com:10750/api'
HEADERS = {
    'Authorization': 'Token b1ee29670a7d598abb41f232d7fb01de6f2c470e',
    'Content-Type': 'application/json',
}
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
    
