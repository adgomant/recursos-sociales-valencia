# -*- coding: utf-8 -*-

import json
import re
import openai
import folium
import pandas as pd
import numpy as np
import streamlit as st
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from streamlit_folium import st_folium

def display_map(asociaciones, code=0, themes=['Todos']):
    df = st.session_state.ubi_data
    if 'Todas' not in asociaciones:
        df = df[df['equipamien'].isin(asociaciones)]
    if code:
        df = df[df["postcode"] == str(code)]
    if 'Todos' not in themes:
        df = df[df["theme"].isin(themes)]
    map = folium.Map(location=(39.479, -0.37), 
                     zoom_start= 12.5, 
                     scrollWheelZoom=False, 
                     tiles='CartoDB positron')
    for i, row in df.iterrows():
        folium.Marker([row.geo_point_2d[0], row.geo_point_2d[1]], 
                      popup=row.equipamien.capitalize(),
                      icon=folium.Icon(color="red", icon=str(df['icono'][i]))
                      ).add_to(map) 
    return st_folium(map, width=725, returned_objects=[])


def search_result(i: int, url: str, title: str, highlights: str,
                  address: str, phone: str, mail: str, theme:str, **kwargs) -> str:
    """ HTML scripts to display search results. """
    return f"""
        <div style="font-size:120%;">
            {i + 1}.
            <a href="{url}">
                {title}
            </a>
        </div>
        <div style="font-size:95%;">
            <div style="color:grey;font-size:95%;">
                {address}
            </div>
            <div style="float:left;font-style:italic;">
                {theme} ·&nbsp;
            </div>
            <div style="color:grey;float:left;">
                {phone} ·&nbsp;
            </div>
            <div style="color:grey;float:left;">
                {mail}
            </div>
            <br>{highlights}</br>
        </div>
    """

@st.cache_resource
def load_index(idx_dir):
    ix = open_dir(idx_dir)
    return ix

def index_search(ix, q, num_docs=-1):
    parser = QueryParser(fieldname="content", schema=ix.schema)
    query = parser.parse(q)
    with ix.searcher() as searcher:
        results = searcher.search(query)
        if not results: return
        ans = []
        for hit in results[:num_docs]:
            res = {}
            res["id"] = hit["Id"]
            #res["content"] = hit["content"]
            res["url"] = hit["website"][0]
            res["title"] = hit["name"].capitalize()
            short_desc = re.sub(r"M[eaá]s informaci[oó]n?\.?", "", hit["short_desc"])
            short_desc = re.sub(r"\s{2,}", " ", short_desc)
            res["highlights"] = short_desc
            author = hit["phone"]
            if author:
              res["phone"] = author[0]
            else:
              res["phone"] = "N/A"
            res["address"] = hit["address"]
            mail = hit["mail"]
            if mail:
                res["mail"] = mail[0]
            else:
                res["mail"] = "N/A"
            res["theme"] = hit["theme"]
            ans.append(res)
    return ans

@st.cache_data
def truncate_text(text, max_tokens):
    tokens = text.split()
    if len(tokens) <= max_tokens:
        return text
    return ' '.join(tokens[:max_tokens])

# Generate a response from ChatGPT based on the given prompt
@st.cache_data(show_spinner=False)
def chat_gpt(prompt, model="gpt-3.5-turbo", max_tokens=1024, max_context_tokens=4000, safety_margin=5):
    # Truncate the prompt content to fit within the model's context length
    truncated_prompt = truncate_text(prompt, max_context_tokens - max_tokens - safety_margin)
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "Eres un assitente entrenado para recomendar servicios sociales. Entiendes castellano y valenciano perfectamente."},
            {"role": "user", "content": truncated_prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

def search_app():
    #st.set_page_config(
    #    page_icon="🔎",
    #)

    #st.write(load_css(), unsafe_allow_html=True)
    
    num_results = st.sidebar.number_input('Número de resultados:', 10, 40)
    want_recomendation = st.sidebar.radio('Obtener recomendación?', ['Sí', 'No'])
    st.sidebar.write("Si desea recomendaciones inteligentes, ingrese su clave de OpenAI.")
    openaiapikey = st.sidebar.text_input("Your openai API key:")
    openai.api_key = openaiapikey
    model = "gpt-3.5-turbo-0301"
    st.title('Búsca Recursos Sociales')
    search = st.text_input('Enter search words:')
    chat_response = st.empty()
    search_results = st.container()

    # Load data and models
    #data = read_data()
    ix = load_index("social_centres_index")

    if search:
        query = " OR ".join(search.split())
        hits = index_search(ix, query, num_results)
        resp = "\n\n".join([
          f"NOMBRE:{hit['title']}\nDESCRIPCION:{hit['highlights']}"
          for hit in hits
        ])
        if want_recomendation == "Sí" and openaiapikey:
            with st.spinner("Obteniendo recomendación..."):
              negResponse = f"No parece que haya ninún centro para tus necesidades"
              prompt = f"Dada la siguiente consulta: {search}\nOfrece al ususario la mejor recomendación de entre los siguientes servicios: {resp}\nSi no puedes responder basandote en la lista proporcionada, responde '{negResponse}' y nada más"
              answer = chat_gpt(prompt)

            with chat_response:
                if negResponse in answer:
                    st.write(f"{answer.strip()}")
                else:
                    st.write(f"{answer.strip()}\n\nOtros servicios recomendados:")
        else:
            with chat_response:
                st.write("Servicios recomendados:")
        st.session_state.most_recent_results_from_search = []
        # search results
        with search_results:
            for i, res in enumerate(hits):
                candidate = st.session_state.ubi_data.query(f"id == {int(res['id'])}")
                if len(candidate) == 1:
                    st.session_state.most_recent_results_from_search.append(candidate.iloc[0].at["equipamien"])
                with st.expander(res["title"].upper()):
                    st.write(search_result(i, **res), unsafe_allow_html=True)
            if st.button("Ver en el mapa"):
                display_map(asociaciones=st.session_state.most_recent_results_from_search)
    else:
        st.markdown("""
        ## 
        
        Estamos aquí para ayudarte a encontrar los recursos y servicios sociales que necesitas. Nuestro buscador te permitirá acceder a información relevante y actualizada sobre una amplia variedad de recursos disponibles en la ciudad de Valencia.

        Para comenzar, puedes ingresar tu consulta en el campo de búsqueda a continuación. Por ejemplo, si estás buscando actividades para personas sin hogar :house_with_garden:, simplemente escribe "actividades para personas sin hogar" y presiona Enter.

        ¡Explora los resultados y encuentra opciones que se ajusten a tus necesidades! Estamos comprometidos en proporcionarte información precisa y valiosa para que puedas acceder a los recursos sociales que necesitas.

        ¡Adelante, comienza tu búsqueda ahora mismo y descubre cómo podemos ayudarte! :rocket:
        """)

if __name__ == '__main__':
    search_app()
