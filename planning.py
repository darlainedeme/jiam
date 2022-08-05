# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 16:36:58 2022

@author: EDEME_D
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import datetime as dt

places = pd.read_csv('places.csv', encoding="ISO-8859-1", index_col=0)
places = places[places['Latitude'].notna()]
places = gpd.GeoDataFrame(places, geometry=gpd.points_from_xy(places['Longitude'], places['Latitude']))
# center on Liberty Bell
long = places.geometry.x.mean()
lat = places.geometry.y.mean()
   
option = st.sidebar.selectbox('How would you like to filter the places?',
                              ['By city',
                               'By type',
                               'By day'], index=1)         
     