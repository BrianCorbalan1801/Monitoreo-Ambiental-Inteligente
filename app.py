import streamlit as st
import pandas as pd
from PIL import Image

#df = pd.read_csv('dataframe')

def main():
    st.title("Monitoreo del Clima")
    st.write("Holaaaasdas")
    #st.dataframe(df)

    img = Image.open("xd.png")
    st.image(img, use_column_width=True)

if __name__ == '__main__':
    main()
