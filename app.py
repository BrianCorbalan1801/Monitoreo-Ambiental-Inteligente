import streamlit as st
import pandas as pd
from PIL import Image
from registros import cargar_datos
from descarga import descarga_registro
from mapa import mapa_interactivo
from monitoreo import real

#df = pd.read_csv('dataframe')

st.set_page_config(page_title='Monitoreo Ambiental', page_icon='sunrise', layout='wide', initial_sidebar_state='collapsed')

def main():
    st.title("Aplicacion principal")

    menu = ["Inicio", "Descarga registros", "Mapa interactivo", "Registros historicos"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Inicio":
        st.subheader("Inicio")
        real()

    elif choice == "Descarga registros":
        descarga_registro()
    elif choice == "Mapa interactivo":
        mapa_interactivo()
    else:
        st.subheader("Registros historicos")
        cargar_datos()

    #st.dataframe(df)

if __name__ == '__main__':
    main()