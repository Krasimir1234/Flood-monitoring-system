import geopandas as gpd
import matplotlib.pyplot as plt

shapefile_path = "extracted_files/abu_hq30_stmk.shp"

try:
    gdf = gpd.read_file(shapefile_path)
    print("Shapefile loaded successfully!")


    print(gdf.head())


    gdf.plot()
    plt.title("Flood Hazard Areas - HQ30")
    plt.show()
except Exception as e:
    print(f"An error occurred while processing the Shapefile: {e}")
