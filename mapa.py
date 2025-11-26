import streamlit as st
import folium
import pandas as pd
import mysql.connector
import time


def obtener_datos_sensores():
    try:
        conn = mysql.connector.connect(
            host="10.56.2.71",    
            user="brian",
            password="47495864",
            database="monitoreo"      
        )

        query = """
            SELECT zona, latitud, longitud, temperatura, humedad, co2
            FROM mediciones
            ORDER BY fecha_hora DESC
        """

        df = pd.read_sql(query, conn)
        conn.close()

        def calcular_estado(co2):
            if co2 < 800:
                return "Bueno"
            elif co2 < 1200:
                return "Moderado"
            else:
                return "Malo"

        df["estado"] = df["co2"].apply(calcular_estado)

        return df

    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return pd.DataFrame()
    

def mapa_interactivo():
    st.subheader("Mapa interactivo")
    st.write("En este mapa se pueden ver las ubicaciones de los sensores y sus valores actualizados.")

    st.write("🔄 El mapa se actualiza automáticamente cada **30 segundos**.")

    time.sleep(30)
    st.rerun()


    df = obtener_datos_sensores()

    if df.empty:
        st.warning("No se pudieron cargar datos desde la base.")
        return

    m = folium.Map(location=[df["latitud"].mean(), df["longitud"].mean()], zoom_start=14)

    for _, fila in df.iterrows():

        popup_html = f"""
        <b>Zona:</b> {fila['zona']}<br>
        <b>Temperatura:</b> {fila['temperatura']} °C<br>
        <b>Humedad:</b> {fila['humedad']} %<br>
        <b>CO₂:</b> {fila['co2']} ppm<br>
        <b>Estado:</b> {fila['estado']}
        """

        folium.Marker(
            [fila["latitud"], fila["longitud"]],
            popup=popup_html,
            tooltip=fila["zona"],
            icon=folium.Icon(
                color="red" if fila["estado"] == "Malo" else 
                      "orange" if fila["estado"] == "Moderado" else "green"
            )
        ).add_to(m)

    # Render HTML del mapa
    mapa_html = m._repr_html_()
    st.components.v1.html(mapa_html, height=500)
