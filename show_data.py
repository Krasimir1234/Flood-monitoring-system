import xml.etree.ElementTree as ET

# Parse the XML file
file_path = "response.xml"  # Replace with the correct file path
tree = ET.parse(file_path)
root = tree.getroot()

# Namespace mapping
namespace = {
    "inspire": "https://gis.lfrz.gv.at/inspire",
    "gml": "http://www.opengis.net/gml/3.2"
}

# Print headers
print("{:<20} {:<10} {:<10} {:<25} {:<15} {:<15}".format(
    "Gewaesser", "Wert", "Einheit", "Zeitpunkt", "Longitude", "Latitude"
))
print("=" * 90)

# Extract data
for elem in root.findall(".//inspire:pegelaktuell", namespace):
    # Extract elements and default to "N/A" if None
    gewaesser = elem.find("inspire:gewaesser", namespace)
    wert = elem.find("inspire:wert", namespace)
    einheit = elem.find("inspire:einheit", namespace)
    zeitpunkt = elem.find("inspire:zeitpunkt", namespace)
    longitude = elem.find("inspire:lon", namespace)
    latitude = elem.find("inspire:lat", namespace)

    gewaesser_text = gewaesser.text if gewaesser is not None else "N/A"
    wert_text = wert.text if wert is not None else "N/A"
    einheit_text = einheit.text if einheit is not None else "N/A"
    zeitpunkt_text = zeitpunkt.text if zeitpunkt is not None else "N/A"
    longitude_text = longitude.text if longitude is not None else "N/A"
    latitude_text = latitude.text if latitude is not None else "N/A"

    # Print data, now guaranteed to be safe
    print("{:<20} {:<10} {:<10} {:<25} {:<15} {:<15}".format(
        gewaesser_text, wert_text, einheit_text, zeitpunkt_text, longitude_text, latitude_text
    ))
