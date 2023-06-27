# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import streamlit as st
import folium
from streamlit_folium import st_folium

MAP_TITLE= "Recursos Sociales en Valencia"
DESCRIPTION= """No estás solo/a. Estamos contigo. :sparkles:

Esta página te brinda recursos y apoyo en tu camino personal. :woman_climbing:

Cada punto en el mapa representa un lugar donde encontrarás comunidad y ayuda. Los cambios requieren tiempo, pero cada paso, por pequeño que sea, es un gran avance. Y pedir ayuda es el primer paso hacia tu bienestar.

Explora el mapa y encuentra el apoyo que necesitas. Estamos aquí para ti. :yellow_heart:"""
COLABORATION= "En colaboración con"


@st.cache_data
def get_asociaciones():
    return sorted(list(st.session_state.ubi_data['equipamien'].unique()))

@st.cache_data
def get_postcode_info():
    min_cp, max_cp = float("inf"), 0
    for cp in st.session_state.ubi_data.postcode:
        try: 
            icp = int(cp)
            if icp < min_cp:
                min_cp = icp
            if icp > max_cp:
                max_cp = icp
        except:
            continue
    return min_cp, max_cp

@st.cache_data
def get_themes():
    return sorted(list(st.session_state.ubi_data.theme.dropna().unique()))

def display_map(asociaciones=[], code=0, themes=[]):
    df = st.session_state.ubi_data
    if asociaciones:
        df = df[df['equipamien'].isin(asociaciones)]
    if code:
        df = df[df["postcode"] == str(code)]
    if themes:
        df = df[df["theme"].isin(themes)]
    map = folium.Map(location=(39.479, -0.37), 
                     zoom_start= 12.5, 
                     scrollWheelZoom=False, 
                     tiles='CartoDB positron')
    for i, row in df.iterrows():
        folium.Marker([row.geo_point_2d[0], row.geo_point_2d[1]], 
                      popup=row.equipamien.capitalize(),
                      icon=folium.Icon(color="red", icon=str(row.icono))
                      ).add_to(map) 
    return st_folium(map, width=725, returned_objects=[])
   
def map_app():
    #st.set_page_config(
    #    page_icon="🌍",
    #)
    st.title(MAP_TITLE)
    st.markdown(DESCRIPTION)
    lista_asociaciones = get_asociaciones()
    defasoc = st.session_state.most_recent_results_from_search
    asoc = st.sidebar.multiselect('Asociación/Centro/Servicio', 
                                  lista_asociaciones, defasoc)
    min_cp, max_cp = get_postcode_info()
    postcode = st.sidebar.number_input('Código postal', 0, max_cp) #min, max cod postal
    lista_themes = get_themes()
    group = st.sidebar.multiselect('Tema Social: ', lista_themes, [])
    display_map(asoc, postcode, group)

if __name__ == "__main__":
    map_app()
