import os
import geopandas as gpd
import pandas as pd
import numpy as np
import requests
import zipfile
import plotly.graph_objects as go

# Define dataset URL and local paths
DATA_URL = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
DATA_DIR = "data"
ZIP_PATH = os.path.join(DATA_DIR, "ne_110m_admin_0_countries.zip")
SHP_PATH = os.path.join(DATA_DIR, "ne_110m_admin_0_countries.shp")

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Download dataset if not present
if not os.path.exists(SHP_PATH):
    print("Dataset not found. Downloading...")
    response = requests.get(DATA_URL, stream=True)

    if response.status_code == 200:
        with open(ZIP_PATH, "wb") as file:
            file.write(response.content)
        print("Download complete.")

        # Extract the ZIP file
        print("Extracting dataset...")
        with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
            zip_ref.extractall(DATA_DIR)
        print("Extraction complete.")
    else:
        raise Exception(f"Failed to download dataset (HTTP {response.status_code})")

# Load world data
world = gpd.read_file(SHP_PATH)

# Convert to a projected coordinate system for correct area calculations
world = world.to_crs(epsg=3857)  # Web Mercator projection

# Calculate country areas in square km
world["area_km2"] = world.geometry.area / 1e6

# Ensure valid population density calculation (handle missing data)
world["pop_est"] = pd.to_numeric(world["POP_EST"], errors="coerce")
world["pop_density"] = world["pop_est"] / world["area_km2"]

# Apply log scale to population density (use log1p to avoid log(0) issues)
world["pop_density_log"] = np.log1p(world["pop_density"])

# Convert geometries to latitude/longitude for Plotly
world = world.to_crs(epsg=4326)

# Create 3D interactive globe
fig = go.Figure()

fig.add_trace(go.Choropleth(
    geojson=world.__geo_interface__,  # Convert to GeoJSON for Plotly
    locations=world.index,
    z=world["pop_density_log"].fillna(0),  # Fill missing values with 0
    colorscale="plasma",  # Adjusted for better contrast with log scale
    zmin=world["pop_density_log"].min(),
    zmax=world["pop_density_log"].max(),
    marker_line_color="black",
    marker_line_width=0.3,
    colorbar_title="Log(Pop Density)",
))

fig.update_geos(
    projection_type="orthographic",  # 3D Sphere Projection
    showcoastlines=True,
    showland=True,
    showcountries=True,
)

fig.update_layout(
    title="Interactive Rotating Globe - Log Scaled Population Density",
    height=400,
    width=400,
)

# Show the interactive globe
fig.show()
