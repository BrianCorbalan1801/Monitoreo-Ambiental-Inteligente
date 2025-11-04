import streamlit as st
import folium 


def mapa_interactivo():
    st.subheader("Mapa interactivo")
    st.write("En este mapa se podra ver las distintas ubicaciones donde se encuentra los sensores tomando datos")


    m = folium.Map(location=[-34.679725714625725, -58.45085487390574], zoom_start=14)

    tooltip = "Haz click"
    folium.Marker(
        [-34.679725714625725, -58.45085487390574],
        popup="ETEC",
        tooltip=tooltip,
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

    folium.Circle(
        radius=250,
        location=[-34.679725714625725, -58.45085487390574],
        popup="Zona de medición",
        color="#3186cc",
        fill=True,
        fill_color="#3186cc"
    ).add_to(m)

    mapa_html = m._repr_html_()

    st.components.v1.html(mapa_html, height=500)