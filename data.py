import requests
import xml.etree.ElementTree as ET
import json

def fetch_and_parse_data():
    url = "https://gis.lfrz.gv.at/wmsgw/?key=a64a0c9c9a692ed7041482cb6f03a40a&VERSION=2.0.0&REQUEST=GetFeature&SERVICE=WFS&TYPENAME=inspire:pegelaktuell"

    response = requests.get(url)

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")

    if response.status_code == 200:
        try:
            root = ET.fromstring(response.content)
            namespace = {"inspire": "https://gis.lfrz.gv.at/inspire"}

            data = []
            for elem in root.findall(".//inspire:pegelaktuell", namespace):
                entry = {}
                gewaesser = elem.find("inspire:gewaesser", namespace)
                wert = elem.find("inspire:wert", namespace)
                einheit = elem.find("inspire:einheit", namespace)
                zeitpunkt = elem.find("inspire:zeitpunkt", namespace)
                longitude = elem.find("inspire:lon", namespace)
                latitude = elem.find("inspire:lat", namespace)

                entry["gewaesser"] = gewaesser.text if gewaesser is not None else "N/A"
                entry["wert"] = float(wert.text) if wert is not None else None
                entry["einheit"] = einheit.text if einheit is not None else "N/A"
                entry["zeitpunkt"] = zeitpunkt.text if zeitpunkt is not None else "N/A"
                entry["longitude"] = (
                    float(str(longitude.text).replace(",", "."))
                    if longitude is not None and longitude.text is not None
                    else None
                )
                entry["latitude"] = (
                    float(str(latitude.text).replace(",", "."))
                    if latitude is not None and latitude.text is not None
                    else None
                )


                if entry["wert"] is not None:
                    if entry["wert"] > 200:
                        entry["level"] = "critical"
                    elif entry["wert"] > 100:
                        entry["level"] = "medium"
                    else:
                        entry["level"] = "normal"


                if entry["longitude"] is not None and entry["latitude"] is not None:
                    data.append(entry)


            with open("static/data.json", "w") as json_file:
                json.dump(data, json_file, indent=4)

            print(f"Data saved to static/data.json with {len(data)} entries.")

        except ET.ParseError as e:
            print(f"Failed to parse XML data: {e}")
    else:
        print("Failed to fetch data.")


if __name__ == "__main__":
    fetch_and_parse_data()
