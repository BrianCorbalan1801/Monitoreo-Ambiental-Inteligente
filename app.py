import streamlit as st
import pandas as pd
from PIL import Image

#df = pd.read_csv('dataframe')

st.set_page_config(page_title='Monitoreo Ambiental', page_icon='sunrise', layout='wide', initial_sidebar_state='collapsed')

def main():
    st.title("Monitoreo del Clima")
    st.write("Holaaaasdas")
    st.sidebar.header("Navegacion")

    #st.dataframe(df)

    img = Image.open("xd.png")
    st.image(img, use_column_width=True)

if __name__ == '__main__':
    main()
