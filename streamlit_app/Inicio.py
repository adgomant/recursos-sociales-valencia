import streamlit as st
import pandas as pd

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
    
def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                content: "Recursos Sociales Valencia";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def set_session_state():
    if "ubi_data" not in st.session_state:
        st.session_state.ubi_data = load_data()
    if "most_recent_results_from_search" not in st.session_state:
        st.session_state.most_recent_results_from_search = []

def main():
    st.set_page_config(
        page_title="Recursos Sociales Valencia",
        page_icon="👋",
    )
    set_session_state()
    add_logo()
    st.markdown(
        """
        # ¡Bienvenido a Recursos Sociales Valencia! 👋

        Queremos ayudarte a encontrar los recursos y servicios sociales que necesitas en la ciudad de Valencia. Nuestra aplicación está diseñada para facilitar el acceso a información relevante y actualizada sobre una amplia variedad de recursos sociales en tu comunidad. 🏘

        ## Descubre Recursos Relevantes 🔎

        Utiliza nuestro buscador para introducir tus consultas y obtener resultados precisos. Nuestro algoritmo de búsqueda avanzado te proporcionará los recursos más relevantes que se ajusten a tus necesidades. Además, basándonos en los documentos recopilados, te ofreceremos recomendaciones personalizadas de servicios sociales que podrían ser de interés para ti.🫂

        ## Explora en el Mapa 🌍

        ¿Prefieres visualizar los recursos sociales en un mapa interactivo? En nuestra pestaña de Mapa, podrás explorar los diferentes centros, recursos y asociaciones disponibles en la ciudad de Valencia. Filtra por código postal o tema para encontrar exactamente lo que estás buscando. Ya sea que necesites recursos relacionados con mujeres, adicciones, personas mayores u otros temas, nuestro mapa te mostrará opciones cercanas y relevantes.

        ## Tu Fuente Confiable

        Recursos Sociales Valencia se esfuerza por ofrecerte información precisa y actualizada 📊. Garantizamos que los recursos sean verificados y estén disponibles cuando más los necesites. Nuestra misión es brindarte la información necesaria para mejorar tu calidad de vida 🚀 y ayudarte a conectarte con los servicios sociales que mejor se adapten a tus necesidades. 

        ¡Comienza tu búsqueda de recursos sociales hoy mismo y descubre cómo Recursos Sociales Valencia puede marcar la diferencia en tu vida y en tu comunidad! ✨
        """
    )

if __name__=="__main__":
    main()
