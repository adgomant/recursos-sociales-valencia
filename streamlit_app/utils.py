# -*- coding: utf-8 -*-

import re
import openai
import folium
import pandas as pd
import numpy as np
import streamlit as st
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from streamlit_folium import st_folium

###############################################################################
# General
###############################################################################

@st.cache_data
def load_data():
    sc = pd.read_json("data/social_centres.json", orient="index")
    df = pd.read_csv("data/datos_sociales1.csv", index_col=0)
    df.geo_point_2d=df.geo_point_2d.apply(lambda x: eval(x))
    df.dropna(subset="telefono", inplace=True)
    df.telefono = df.telefono.astype(int).astype(str)
    df.index = list(range(len(df)))
    new_cols = list(sc.columns) + list(df.columns)
    new_idx, new_rows = [], []
    for i, row in sc.iterrows():
        #print(df.telefono.isin(row.phone))
        if row.phone:
            candidate = df[df.telefono.isin(row.phone)]
            #print(candidate)
            if len(candidate) == 1:
                new_idx.append(i)
                new_rows.append(list(row.values)+list(candidate.iloc[0].values))
    data = pd.DataFrame(new_rows, index=new_idx, columns=new_cols)
    return data

###############################################################################
# Buscador
###############################################################################

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

def search_result_template(i: int, url: str, title: str, highlights: str,
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
    
@st.cache_data
def set_openai_apikey(key):
    openai.apikey = apikey
    
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

###############################################################################
# Mapa
###############################################################################

@st.cache_data
def get_asociaciones(data):
    return sorted(list(data.equipamien.unique()))

@st.cache_data
def get_max_postcode(data):
    min_cp, max_cp = float("inf"), 0
    for cp in data.postcode:
        try: 
            icp = int(cp)
            if icp > max_cp:
                max_cp = icp
        except:
            continue
    return max_cp

@st.cache_data
def get_themes(data):
    return sorted(list(data.theme.dropna().unique()))

def display_map(df, asociaciones, code=0, themes=['Todos']):
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
                      icon=folium.Icon(color="red", icon=str(df['icono'][i]))
                      ).add_to(map) 
    return st_folium(map, width=725, returned_objects=[])
