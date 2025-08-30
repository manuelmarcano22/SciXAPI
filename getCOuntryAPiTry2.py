# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import pandas as pd

# %%
listapaises = pd.read_csv('countries_codes_and_coordinates.csv')

# %%
pais

# %%
for j,pais in listapaises.iterrows():
    #print(pais['Country'],pais['Alpha-3 code'])

# %%

# Example dictionary: ISO_A3 -> values
data_dict = {
    "USA": 50,
    "CAN": 30,
    "BRA": 70,
    "FRA": 60,
    "CHN": 90,
    "IND": 80,
}

# Convert dict to DataFrame
df = pd.DataFrame(list(data_dict.items()), columns=["ISO_A3", "value"])

# Load Natural Earth shapefile (downloaded manually)
world = gpd.read_file("110m_cultural/ne_110m_admin_0_countries.shp")

# Merge with your values
world = world.merge(df, on="ISO_A3", how="left")

# Plot
fig, ax = plt.subplots(1, 1, figsize=(12, 6))
world.boundary.plot(ax=ax, linewidth=0.5, color="black")
world.plot(
    column="value",
    ax=ax,
    legend=True,
    cmap="viridis",
    missing_kwds={
        "color": "lightgrey",
        "edgecolor": "black",
        "hatch": "///",
        "label": "No data",
    },
)

ax.set_title("Country values map", fontsize=15)
plt.show()


# %%
