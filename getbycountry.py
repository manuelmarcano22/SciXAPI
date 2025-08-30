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
from pyzotero import zotero
import requests
from urllib.parse import urlencode, quote_plus
import json
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
import pandas as pd

# %%
ads_token="k2zRbQStkuH0SLXRl3wAujbTY4bpjoWrkILapzbD" # This is for ads/scix

# %%
listapaises = pd.read_csv('countries_codes_and_coordinates.csv')

# %%
listapaises[listapaises['Country'] == "France"]

# %%
dic = {}



for j,pais in listapaises.iterrows():


    country = pais['Country']
    code = pais['Alpha-3 code'].strip().strip('"')
    year = "2015-2025"
    

    
    query = f'pos(aff:"{country}",1) AND =ack:"Astrophysics Data System" AND year:{year}'
    
    #query = f'doi:{doi}'
    encoded_query = urlencode({"q":query,
                               "fl": "title,id,ack",                          
                               "sort": "date desc",
                               "rows":'1000'
                              })
    
    results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), \
                           headers={'Authorization': 'Bearer ' + ads_token})
    
    results.json()
    
    
    
    data = results.json()
    numincountry = data['response']['numFound']

    dic[f'{code}'] = numincountry

    if numincountry > 0:
        print(query)
        print(country,code,numincountry)

        



# %%

# %%
data_dict = dic


# Convert dict to DataFrame
df = pd.DataFrame(list(data_dict.items()), columns=["ISO_A3", "value"])

# Load Natural Earth shapefile (downloaded manually)
world = gpd.read_file("110m_cultural/ne_110m_admin_0_countries.shp")

#France is weird
dondeF = world[world['SOVEREIGNT'] == 'France'].index
world.loc[dondeF,'SOV_A3'] = 'FRA'



# Merge with your values
world = world.merge(df, on="ISO_A3", how="left")

world.loc[dondeF,'value'] = data_dict['FRA']


# Plot
fig, ax = plt.subplots(1, 1, figsize=(12, 6))

# Plot countries with values > 0
world[world["value"] > 0].plot(
    column="value",
    ax=ax,
    cmap="viridis",
    legend=True,
)

# Plot countries with value == 0 (blank or grey)
world[world["value"] == 0].plot(
    ax=ax,
    color="lightgrey",
    edgecolor="black",
    hatch="...",
)

ax.set_ylim(-60, 80)     # latitudes


#ax.set_title("Country values map", fontsize=15)
plt.show()

fig.savefig('ADSAck.png')

# %% [markdown]
# # All Publications

# %%
data_dict = dic


# Convert dict to DataFrame
df = pd.DataFrame(list(data_dict.items()), columns=["ISO_A3", "value"])

# Load Natural Earth shapefile (downloaded manually)
world = gpd.read_file("110m_cultural/ne_110m_admin_0_countries.shp")

#France is weird
dondeF = world[world['SOVEREIGNT'] == 'France'].index
world.loc[dondeF,'SOV_A3'] = 'FRA'



# Merge with your values
world = world.merge(df, on="ISO_A3", how="left")

world.loc[dondeF,'value'] = data_dict['FRA']


# Plot
fig, ax = plt.subplots(1, 1, figsize=(12, 6))

# Plot countries with values > 0
world[world["value"] > 0].plot(
    column="value",
    ax=ax,
    cmap="summer",
    legend=True,
)

# Plot countries with value == 0 (blank or grey)
world[world["value"] == 0].plot(
    ax=ax,
    color="lightgrey",
    edgecolor="black",
    hatch="...",
)

# Set zoom to Americas (lon, lat ranges)
ax.set_xlim(-170, -30)   # longitudes
ax.set_ylim(-60, 80)     # latitudes


#ax.set_title("Country values map", fontsize=15)
plt.show()


# %%
data_dict = dic


# Convert dict to DataFrame
df = pd.DataFrame(list(data_dict.items()), columns=["ISO_A3", "value"])

# Load Natural Earth shapefile (downloaded manually)
world = gpd.read_file("110m_cultural/ne_110m_admin_0_countries.shp")

#France is weird
dondeF = world[world['SOVEREIGNT'] == 'France'].index
world.loc[dondeF,'SOV_A3'] = 'FRA'



# Merge with your values
world = world.merge(df, on="ISO_A3", how="left")

world.loc[dondeF,'value'] = data_dict['FRA']


# Plot
fig, ax = plt.subplots(1, 1, figsize=(12, 6))

# Plot countries with values > 0
world[world["value"] > 0].plot(
    column="value",
    ax=ax,
    cmap="summer",
    legend=True,
)

# Plot countries with value == 0 (blank or grey)
world[world["value"] == 0].plot(
    ax=ax,
    color="lightgrey",
    edgecolor="black",
    hatch="...",
)




for idx, row in world.iterrows():
    if pd.notnull(row["value"]):  # only annotate countries with data
        x, y = row["geometry"].centroid.x, row["geometry"].centroid.y
        ax.text(
            x, y, 
            f"{int(row['value'])}",  # format as int
            ha="center", va="center",
            fontsize=7, color="black", weight="bold"
        )

# Set zoom to Americas (lon, lat ranges)
ax.set_xlim(-170, -30)   # longitudes
ax.set_ylim(-60, 80)     # latitudes


#ax.set_title("Country values map", fontsize=15)
plt.show()


# %%
