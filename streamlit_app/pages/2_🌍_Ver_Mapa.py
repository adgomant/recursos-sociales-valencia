# -*- coding: utf-8 -*-

import streamlit as st

import sys
sys.path.append("streamlit_app")
from utils import (
    get_asociaciones,
    get_max_postcode,
    get_themes,
    display_map
)
   
def map_app():
    # sidebar
    lista_asociaciones = get_asociaciones(st.session_state.ubi_data)
    defasoc = st.session_state.most_recent_results_from_search
    asoc = st.sidebar.multiselect('Asociación/Centro/Servicio', lista_asociaciones, defasoc)
    #min_cp, max_cp = get_max_postcode(st.session_state.ubi_data)
    max_cp = get_max_postcode(st.session_state.ubi_data)
    postcode = st.sidebar.number_input('Código postal', 0, max_cp) #min, max cod postal
    lista_themes = get_themes(st.session_state.ubi_data)
    group = st.sidebar.multiselect('Tema Social: ', lista_themes, [])
    
    # body
    st.title("Recursos Sociales en Valencia")
    st.markdown("""
    No estás solo/a. Estamos contigo. :sparkles:

    Esta página te brinda recursos y apoyo en tu camino personal. :woman_climbing:

    Cada punto en el mapa representa un lugar donde encontrarás comunidad y ayuda. Los cambios requieren tiempo, pero cada paso, por pequeño que sea, es un gran avance. Y pedir ayuda es el primer paso hacia tu bienestar.

    Explora el mapa y encuentra el apoyo que necesitas. Estamos aquí para ti. :yellow_heart:
    """)

    # logic
    display_map(st.session_state.ubi_data, asoc, postcode, group)

if __name__ == "__main__":
    map_app()
