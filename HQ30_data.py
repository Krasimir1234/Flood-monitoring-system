import requests


resource_url = "https://service.stmk.gv.at/ogd/OGD_Data_ABT17/geoinformation/abu_hq30_stmk.zip"
file_name = "abu_hq30_stmk.zip"

try:
    response = requests.get(resource_url, stream=True)
    if response.status_code == 200:
        with open(file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"File downloaded successfully as '{file_name}'")
    else:
        print(f"Failed to download file. HTTP Status Code: {response.status_code}")
except requests.RequestException as e:
    print(f"An error occurred while downloading the file: {str(e)}")
