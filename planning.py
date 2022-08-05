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
     
m = folium.Map(location=[lat, long], zoom_start=9)
tile = folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri Satellite',
    overlay=False,
    control=True
).add_to(m)

tile = folium.TileLayer(
    tiles='http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}',
    attr='Google',
    name='Google Hybrid',
    overlay=False,
    control=True
).add_to(m)

tile = folium.TileLayer(
    tiles='http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}',
    attr='Google',
    name='Google Maps',
    overlay=False,
    control=True
).add_to(m)
     

def plotcase(point):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a CircleMarker and adds it to your this_map'''
    folium.CircleMarker(location=[point.Latitude, point.Longitude],
                        popup=str(point.Dove) 
                        + "\n" 
                        + "\n" 
                        + str(point.Nome)
                        + "\n" 
                        + "\n" 
                        + str(point.Descrizione),
                        color = 'green',
                        radius=2,
                        weight=5).add_to(feature_group_1)

def plotnegril(point):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a CircleMarker and adds it to your this_map'''
    folium.CircleMarker(location=[point.Latitude, point.Longitude],
                        popup="<a href=" + str(point.Link) + ">" + str(point.Nome) + "</a>",
                        color = 'red',
                        html='<div style="font-size: 24pt">' + str(point.Nome) + '</div>',
                        radius=2,
                        weight=5).add_to(feature_group_2)


def plotantonio(point):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a CircleMarker and adds it to your this_map'''
    folium.CircleMarker(location=[point.Latitude, point.Longitude],
                        popup=str(point.Dove) 
                        + "\n" 
                        + "\n" 
                        + str(point.Nome)
                        + "\n" 
                        + "\n" 
                        + str(point.Descrizione),
                        color = 'blue',
                        radius=2,
                        weight=5).add_to(feature_group_3)

def plotanna(point):
    '''input: series that contains a numeric named latitude and a numeric named longitude
    this function creates a CircleMarker and adds it to your this_map'''
    folium.CircleMarker(location=[point.Latitude, point.Longitude],
                        popup=str(point.Dove) 
                        + "\n" 
                        + "\n" 
                        + str(point.Nome)
                        + "\n" 
                        + "\n" 
                        + str(point.Descrizione),
                        color = 'yellow',
                        radius=2,
                        weight=5).add_to(feature_group_4)

# case
feature_group_1 = folium.FeatureGroup(name='Case', show=True)
case_gdf = places[places.Cosa == 'CASA']
case_gdf.apply(plotcase, axis = 1)
feature_group_1.add_to(m)

if option == 'By city': 
    
    feature_group_2 = folium.FeatureGroup(name='Negril', show=True)
    feature_group_3 = folium.FeatureGroup(name='Port Antonio', show=True)
    feature_group_4 = folium.FeatureGroup(name='St. Ann Parish', show=True)


    negril_gdf = places[(places.Dove == 'NEGRIL') & (places.Cosa != 'CASA')]
    negril_gdf.apply(plotnegril, axis = 1)
    
    anthony_gdf = places[(places.Dove == 'PORT ANTONIO') & (places.Cosa != 'CASA')]
    anthony_gdf.apply(plotantonio, axis = 1)
    
    anna_gdf = places[(places.Dove == 'ST. ANN PARISH') & (places.Cosa != 'CASA')]
    anna_gdf.apply(plotanna, axis = 1)
    
    
    feature_group_2.add_to(m)
    feature_group_3.add_to(m)
    feature_group_4.add_to(m)



elif option == 'By type': 
    type_of_option = st.sidebar.selectbox('Which one', list(places.Cosa.unique())[1:], index=1)
    # type_of_option = 'SPIAGGIA'
    
    feature_group_2 = folium.FeatureGroup(name=type_of_option, show=True)
    
    plot_gdf = places[places.Cosa == type_of_option]
    plot_gdf.apply(plotnegril, axis = 1)

    feature_group_2.add_to(m)
    
elif option == 'By day': 

    start_date = dt.date(year=2022,month=8,day=7) 
    end_date = dt.date(year=2022,month=8,day=18) 
    max_days = end_date-start_date

    st.write('Per questa visualizzazione bisogna prima che fissiamo il giorno in cui vogliamo visitare ciascuna delle attivitá')

    day = st.sidebar.slider('Select date', min_value=start_date, value=start_date, max_value=end_date)

    # day = 'SPIAGGIA'
    
    # feature_group_2 = folium.FeatureGroup(name=day, show=True)
    
    # plot_gdf = places[places.Cosa == day]
    # plot_gdf.apply(plotnegril, axis = 1)  

    # feature_group_2.add_to(m)  

m.fit_bounds(m.get_bounds())
           
                    
folium.plugins.Draw(export=True, filename='data.geojson', position='topleft', draw_options=None,
                    edit_options=None).add_to(m)
folium.plugins.Fullscreen(position='topleft', title='Full Screen', title_cancel='Exit Full Screen',
                          force_separate_button=False).add_to(m)
folium.plugins.MeasureControl(position='bottomleft', primary_length_unit='meters', secondary_length_unit='miles',
                              primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(m)
folium.LayerControl().add_to(m)



# Displaying a map         
# m.save('map.html')
folium_static(m)

                 