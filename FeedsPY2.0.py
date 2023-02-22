import re
import time
import requests
from bs4 import BeautifulSoup

# Define the output file path
output_file = 'Output_Feeds.txt'

# Read the list of URLs from a file
with open('urls.txt') as f:
    urls = [line.strip() for line in f.readlines()]

# Read the list of excluded IP addresses from a file
with open('exclude_list.txt') as f:
    exclude_list = [line.strip() for line in f.readlines()]

# Define a regular expression pattern to match IP addresses
ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

# Loop indefinitely and update the output file every 30 minutes
while True:
    # Create an empty set to store the IP addresses
    ip_addresses = set()
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for element in soup.find_all(['p', 'div']):
            for ip in element.get_text().split():
                if ip not in exclude_list and ip not in ip_set:
                    ip_set.add(ip)

    # Loop over the URLs and extract IP addresses from each
    for url in urls:
        # Fetch the contents of the URL
        response = requests.get(url)
        content = response.text

        # Use the regular expression pattern to find IP addresses in the content
        matches = re.findall(ip_pattern, content)
        print(f'Found {len(matches)} IP addresses in URL {url}')

        # Add the matches to the set of IP addresses
        for match in matches:
            ip_addresses.add(match)

    # Remove the IP addresses to exclude
    ip_addresses = ip_addresses.difference(set(exclude_list))

    # Write the IP addresses to the output file
    with open(output_file, 'w') as f:
        for ip in ip_addresses:
            f.write(ip + '\n')

    # Sleep for 30 minutes before running the loop again
    print('Updated output file at', time.ctime())
    time.sleep(1800)