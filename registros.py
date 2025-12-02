import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import sqlite3
    

SwitchDB = True

def cargar_datos_db():

    conn = mysql.connector.connect(
        host="10.56.2.71",
        user="brian",
        password="47495864",
        database="monitoreo"  
    )

    query = "SELECT zona, latitud, longitud, temperatura, humedad, co2, fecha_hora FROM mediciones;"
    df = pd.read_sql(query, conn)
    conn.close()

    df["fecha_hora"] = pd.to_datetime(df["fecha_hora"])

    st.sidebar.header("Filtros")

    zonas = df["zona"].unique()
    zona_seleccionada = st.sidebar.selectbox("Selecciona la zona:", zonas)

    fecha_inicio = st.sidebar.date_input("Desde:", df["fecha_hora"].min().date())
    fecha_fin = st.sidebar.date_input("Hasta:", df["fecha_hora"].max().date())

    # Filtrado
    df_filtrado = df[
        (df["zona"] == zona_seleccionada)
        & (df["fecha_hora"].dt.date >= fecha_inicio)
        & (df["fecha_hora"].dt.date <= fecha_fin)
    ]

    st.subheader(f"Datos de {zona_seleccionada} entre {fecha_inicio} y {fecha_fin}")
    st.dataframe(df_filtrado)

    if not df_filtrado.empty:
        st.subheader("📊 Estadísticas del período seleccionado")
        st.write(f"**Temperatura máxima:** {df_filtrado['temperatura'].max():.2f} °C")
        st.write(f"**Temperatura promedio:** {df_filtrado['temperatura'].mean():.2f} °C")
        st.write(f"**Temperatura mínima:** {df_filtrado['temperatura'].min():.2f} °C")
        st.write(f"**CO₂ promedio:** {df_filtrado['co2'].mean():.2f} ppm")

        fig, ax = plt.subplots()
        ax.plot(df_filtrado["fecha_hora"], df_filtrado["co2"], label="CO₂ (ppm)", marker="o")
        ax.plot(df_filtrado["fecha_hora"], df_filtrado["temperatura"], label="Temperatura (°C)", marker="s")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Valores")
        ax.legend()
        st.pyplot(fig)

    else:
        st.warning("No hay datos en el rango seleccionado.")

def cargar_datos_fk():

    conn = sqlite3.connect('data/monitoreo.db')
    df_fake = pd.read_sql_query("SELECT * FROM mediciones", conn)
    conn.close()

    df_fake["fecha_hora"] = pd.to_datetime(df_fake["fecha_hora"])

    st.header("Filtros")

    zonas = df_fake["zona"].unique()
    zona_seleccionada = st.selectbox("Selecciona la zona:", zonas)

    fecha_inicio = st.date_input("Desde:", df_fake["fecha_hora"].min().date())
    fecha_fin = st.date_input("Hasta:", df_fake["fecha_hora"].max().date())

    # Filtrado
    df_filtrado = df_fake[
        (df_fake["zona"] == zona_seleccionada)
        & (df_fake["fecha_hora"].dt.date >= fecha_inicio)
        & (df_fake["fecha_hora"].dt.date <= fecha_fin)
    ]

    st.subheader(f"Datos de {zona_seleccionada} entre {fecha_inicio} y {fecha_fin}")
    st.dataframe(df_filtrado)

    if not df_filtrado.empty:
        st.subheader("📊 Estadísticas del período seleccionado")
        st.write(f"**Temperatura máxima:** {df_filtrado['temperatura'].max():.2f} °C")
        st.write(f"**Temperatura promedio:** {df_filtrado['temperatura'].mean():.2f} °C")
        st.write(f"**Temperatura mínima:** {df_filtrado['temperatura'].min():.2f} °C")
        st.write(f"**CO₂ promedio:** {df_filtrado['co2'].mean():.2f} ppm")

        fig, ax = plt.subplots()
        ax.plot(df_filtrado["fecha_hora"], df_filtrado["co2"], label="CO₂ (ppm)", marker="o")
        ax.plot(df_filtrado["fecha_hora"], df_filtrado["temperatura"], label="Temperatura (°C)", marker="s")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Valores")
        ax.legend()
        st.pyplot(fig)

    else:
        st.warning("No hay datos en el rango seleccionado.")




def cargar_datos():

    if SwitchDB == True:
        st.warning("Se realizo una vinculacion con la Base de datos ficticia.")
        df_fake = cargar_datos_fk()
        st.dataframe(df_fake)

    else: 
        st.success("Se realizo una conexion a la Base de datos mysql")
        df = cargar_datos_db()
        st.dataframe(df)