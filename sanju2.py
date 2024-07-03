import os
import csv
import time
import requests

# Replace with your VirusTotal API key
API_KEY = "6e5c456afb4a8640ffbd5ef6c17837b5394be901bd3ea372d79268f23d634056"
# IP Geolocation API key
GEO_API_KEY = "afc515eeb1b34f0cbcb283de92e153e0"

def generate_api_url(ip_address):
    base_url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}"
    return base_url

def get_ip_location(ip_address):
    geo_url = f"https://api.ipgeolocation.io/ipgeo?apiKey={GEO_API_KEY}&ip={ip_address}"
    response = requests.get(geo_url)
    if response.status_code == 200:
        data = response.json()
        return f"{data.get('city', 'N/A')}, {data.get('country_name', 'N/A')}"
    return "N/A"

def main():
    # File path where IP addresses are stored
    ip_file_path = "IP List-1.txt"
    output_csv_file = "IP_Security_Vendors_Analysis.csv"  # Output CSV file name

    # Check if file exists
    if not os.path.exists(ip_file_path):
        print(f"Error: File {ip_file_path} does not exist.")
        return

    # Read IP addresses from file
    with open(ip_file_path, "r") as f:
        ip_addresses = [line.strip() for line in f.readlines() if line.strip()]

    # Counter for IPs processed
    ip_count = 0

    # Open CSV file for writing
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['IP Address', 'Location', 'Status', 'Last Analysis Date', 'Detection Details']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write CSV header
        writer.writeheader()

        # Iterate through IP addresses
        for ip in ip_addresses:
            try:
                # Generate API URL for the current IP address
                api_url = generate_api_url(ip)
                
                # Make GET request to VirusTotal API
                headers = {'x-apikey': API_KEY}
                response = requests.get(api_url, headers=headers)
                response_data = response.json()

                # Extract relevant information from response
                last_analysis_date = response_data.get('data', {}).get('attributes', {}).get('last_analysis_date', 'N/A')
                security_vendors_analysis = response_data.get('data', {}).get('attributes', {}).get('last_analysis_results', {})

                # Determine status based on security vendors' analysis
                status = "Good"
                if security_vendors_analysis:
                    detection_details = "\n".join(f"{vendor}: {verdict.get('category', 'N/A')}" for vendor, verdict in security_vendors_analysis.items())
                    for verdict in security_vendors_analysis.values():
                        if verdict.get('category') in ['malicious', 'harmful', 'suspicious']:
                            status = "Malicious"
                            break
                else:
                    detection_details = "No security vendors' analysis available"

                # Get IP location
                location = get_ip_location(ip)

                # Write IP details to CSV
                writer.writerow({
                    'IP Address': ip,
                    'Location': location,
                    'Status': status,
                    'Last Analysis Date': last_analysis_date,
                    'Detection Details': detection_details
                })

                print(f"IP Address: {ip}")
                print(f"Location: {location}")
                print(f"Status: {status}")
                print(f"Last Analysis Date: {last_analysis_date}")
                print("Security Vendors' Analysis:")
                print(detection_details)
                print("-" * 50)

                # Increment IP count
                ip_count += 1

                # Check if 4 IPs have been processed (rate limit)
                if ip_count % 4 == 0:
                    print("Pausing for 60 seconds to respect rate limit...")
                    time.sleep(60)  # Pause execution for 60 seconds

            except Exception as e:
                print(f"Error fetching details for {ip}: {str(e)}")

    print(f"All IP addresses processed. Results saved to {output_csv_file}")

if __name__ == "__main__":
    main()
