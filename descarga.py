import streamlit as st
import pandas as pd
import mysql.connector
from datetime import datetime
from reportlab.pdfgen import canvas
import io
import sqlite3


SwitchDB = True

def obtener_datos_fecha_db(fecha_inicio, fecha_fin):
    try:
        conn = mysql.connector.connect(
            host="10.56.2.71",
            user="brian",
            password="47495864",
            database="monitoreo"
        )

        query = f"""
            SELECT fecha_hora, zona, temperatura, humedad, co2
            FROM mediciones
            WHERE DATE(fecha_hora) BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
            ORDER BY fecha_hora ASC;
        """

        df = pd.read_sql(query, conn)
        conn.close()
        return df

    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return pd.DataFrame()
    
def obtener_datos_fecha_fk(fecha_inicio, fecha_fin):

    conn = sqlite3.connect('data/monitoreo.db')
    query = f"""
            SELECT fecha_hora, zona, temperatura, humedad, co2
            FROM mediciones
            WHERE DATE(fecha_hora) BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
            ORDER BY fecha_hora ASC;
        """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def crear_registro():
    st.subheader("Descarga de registros")
    st.write("Seleccione un rango de fechas para exportar los registros de los sensores.")

    col1, col2 = st.columns(2)

    with col1:
        fecha_inicio = st.date_input("Fecha inicio")
    with col2:
        fecha_fin = st.date_input("Fecha fin")

    if st.button("Buscar registros") and SwitchDB == True:
        df = obtener_datos_fecha_db(fecha_inicio, fecha_fin)
        

        if df.empty:    
            st.warning("No hay registros para el rango seleccionado.")
            return

        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")

        nombre_csv = f"Registros_{datetime.now().strftime('%Y-%m-%d')}.csv"

        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name=nombre_csv,
            mime="text/csv"
        )

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer)

        c.setFont("Helvetica", 12)
        c.drawString(20, 800, "Reporte de registros de sensores")
        c.drawString(20, 780, f"Fecha de exportación: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        y = 750
        for index, row in df.iterrows():
            texto = f"{row['fecha_hora']} | {row['zona']} | T={row['temperatura']}°C | H={row['humedad']}% | CO₂={row['co2']} ppm"
            c.drawString(20, y, texto)
            y -= 20
            if y < 40:
                c.showPage()
                y = 800

        c.save()

        nombre_pdf = f"Registros_{datetime.now().strftime('%Y-%m-%d')}.pdf"

        st.download_button(
            label="Descargar PDF",
            data=buffer.getvalue(),
            file_name=nombre_pdf,
            mime="application/pdf"
        )
    else:
        df = obtener_datos_fecha_fk(fecha_inicio, fecha_fin)
        

        if df.empty:    
            st.warning("No hay registros para el rango seleccionado.")
            return

        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")

        nombre_csv = f"Registros_{datetime.now().strftime('%Y-%m-%d')}.csv"

        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name=nombre_csv,
            mime="text/csv"
        )

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer)

        c.setFont("Helvetica", 12)
        c.drawString(20, 800, "Reporte de registros de sensores")
        c.drawString(20, 780, f"Fecha de exportación: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

        y = 750
        for index, row in df.iterrows():
            texto = f"{row['fecha_hora']} | {row['zona']} | T={row['temperatura']}°C | H={row['humedad']}% | CO₂={row['co2']} ppm"
            c.drawString(20, y, texto)
            y -= 20
            if y < 40:
                c.showPage()
                y = 800

        c.save()

        nombre_pdf = f"Registros_{datetime.now().strftime('%Y-%m-%d')}.pdf"

        st.download_button(
            label="Descargar PDF",
            data=buffer.getvalue(),
            file_name=nombre_pdf,
            mime="application/pdf"
        )

def descarga_registro():

    if SwitchDB == True:
        st.warning("Se realizo una vinculacion con la Base de datos ficticia.")
        df = obtener_datos_fecha_db()
        crear_registro()

    else: 
        st.success("Se realizo una conexion a la Base de datos mysql")
        df = obtener_datos_fecha_fk()
        crear_registro()