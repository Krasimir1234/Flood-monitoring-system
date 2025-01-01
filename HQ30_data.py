import requests
import xml.etree.ElementTree as ET


def fetch_data(api_url):
    """
    Fetch data from the specified API URL and parse the XML response.
    """
    try:
        response = requests.get(api_url)
        print(f"Status Code: {response.status_code}")

        # Check if the response is successful
        if response.status_code != 200:
            print("Failed to fetch data. Status Code:", response.status_code)
            print("Response Content:", response.text)
            return None

        # Parse the XML response
        try:
            root = ET.fromstring(response.content)  # Parse the XML content
            return root  # Return the parsed XML tree for further processing
        except ET.ParseError as e:
            print("Failed to parse XML. Error:", str(e))
            print("Response Content:", response.text)
            return None

    except Exception as e:
        print("An error occurred while fetching data:", str(e))
        return None


def extract_data(xml_root):
    """
    Extract relevant information from the XML root element.
    """
    if xml_root is None:
        print("No XML data to process.")
        return

    # Define the namespaces
    namespaces = {
        'gmd': 'http://www.isotc211.org/2005/gmd',
        'gco': 'http://www.isotc211.org/2005/gco'
    }

    # Extract organisation names
    organisation_names = xml_root.findall(".//gmd:organisationName/gco:CharacterString", namespaces)
    for org_name in organisation_names:
        print("Organisation Name:", org_name.text.strip() if org_name.text else "No Name Found")

    # Extract other details (e.g., download URLs)
    download_urls = xml_root.findall(".//gmd:URL", namespaces)
    for url in download_urls:
        print("Download URL:", url.text.strip() if url.text else "No URL Found")


# Example Usage
api_url = "https://data.inspire.gv.at/06a75330-49e1-482e-b430-7adf3a8863bc"  # Replace with your actual API URL
xml_data = fetch_data(api_url)

if xml_data is not None:
    extract_data(xml_data)
else:
    print("No data returned.")
