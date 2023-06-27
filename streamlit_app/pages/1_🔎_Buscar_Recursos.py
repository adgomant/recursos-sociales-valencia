# -*- coding: utf-8 -*-

import streamlit as st

import sys
sys.path.append("streamlit_app")
from utils import (
    load_index, 
    index_search, 
    search_result_template, 
    truncate_text,
    chat_gpt,
    display_map
)

def search_app():
    # sideabar
    num_results = st.sidebar.number_input('Número de resultados:', 10, 40)
    want_recomendation = st.sidebar.radio('Obtener recomendación?', ['Sí', 'No'])
    st.sidebar.write("Si desea recomendaciones inteligentes, ingrese su clave de OpenAI.")
    openaiapikey = st.sidebar.text_input("Your openai API key:")
    set_openai_apikey(openaiapikey)

    #body
    st.title('Búsca Recursos Sociales')
    search = st.text_input('Ingresa tu consulta:')
    chat_response = st.empty()
    search_results = st.container()

    # Load index
    ix = load_index("social_centres_index")

    # Logic
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
                    st.write(search_result_template(i, **res), unsafe_allow_html=True)
            if st.button("Ver en el mapa"):
                display_map(st.session_state.ubi_data, 
                            asociaciones=st.session_state.most_recent_results_from_search)
    else:
        st.markdown("""
        ## 
        
        Estamos aquí para ayudarte a encontrar los recursos y servicios sociales que necesitas. Nuestro buscador te permitirá acceder a información relevante y actualizada sobre una amplia variedad de recursos disponibles en la ciudad de Valencia.

        Para comenzar, puedes ingresar tu consulta en el campo de búsqueda más arriba. Por ejemplo, si estás buscando actividades para personas sin hogar :house_with_garden:, simplemente escribe "actividades para personas sin hogar" y presiona Enter.

        ¡Explora los resultados y encuentra opciones que se ajusten a tus necesidades! Estamos comprometidos en proporcionarte información precisa y valiosa para que puedas acceder a los recursos sociales que necesitas.

        ¡Adelante, comienza tu búsqueda ahora mismo y descubre cómo podemos ayudarte! :rocket:
        """)

if __name__ == '__main__':
    search_app()
