#!/usr/bin/env python
# coding: utf-8

# In[4]:


import matplotlib.cm


# In[5]:


import pandas as pd
import numpy as np
import folium
from scipy.interpolate import griddata

# parameters
n = 250                     # number of points
lat0 = 40.7
lon0 = -73.9
eps = 0.1
v_min, v_max = 0, 100       # min, max values

# generating values
lat = np.random.normal(lat0, eps, n)
lon = np.random.normal(lon0, eps, n)
value = np.random.uniform(v_min, v_max, n)

# set up the grid
step = 0.02
xi, yi = np.meshgrid(
    np.arange(lat.min() - step/2, lat.max() + step/2, step),
    np.arange(lon.min() - step/2, lon.max() + step/2, step),
)

# interpolate and normalize values
zi = griddata((lat, lon), value, (xi, yi), method='linear')
zi /= np.nanmax(zi)
g = np.stack([
    xi.flatten(),
    yi.flatten(),
    zi.flatten(),
], axis=1)

# geo_json returns a single square
def geo_json(lat, lon, value, step):
    cmap = mpl.cm.RdBu
    return {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {
            'color': 'white',
            'weight': 1,
            'fillColor': mpl.colors.to_hex(cmap(value)),
            'fillOpacity': 0.5,
          },
          "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [lon - step/2, lat - step/2],
                [lon - step/2, lat + step/2],
                [lon + step/2, lat + step/2],
                [lon + step/2, lat - step/2],
                [lon - step/2, lat - step/2],
              ]]}}]}


# generating a map...
m = folium.Map(location=[lat0, lon0], zoom_start=9, width=400, height=400)

# ...with squares...
for gi in g:
    if ~np.isnan(gi[2]):
        folium.GeoJson(geo_json(gi[0], gi[1], gi[2], step),
                       lambda x: x['properties']).add_to(m)


m


# In[6]:


m.save("hello.html")


# In[ ]:




