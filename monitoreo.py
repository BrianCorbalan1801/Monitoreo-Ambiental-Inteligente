import streamlit as st
import json
import paho.mqtt.client as mqtt
import threading
import time

MQTT_BROKER = "10.9.120.5" 
MQTT_PORT = 1883
MQTT_TOPIC = "monitoreo/lecturas"

latest_data = {"temperatura": 0, "humedad": 0, "co2": 0}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT")
        client.subscribe(MQTT_TOPIC)
    else:
        print("Error de conexión con MQTT:", rc)

def on_message(client, userdata, msg):
    global latest_data
    try:
        payload = json.loads(msg.payload.decode())
        latest_data = payload
    except Exception as e:
        print("Error procesando mensaje:", e)

def mqtt_thread():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

def real():
    st.write("Los valores se actualizan automáticamente cada 30 segundos.")

    if "mqtt_thread" not in st.session_state:
        st.session_state.mqtt_thread = threading.Thread(target=mqtt_thread, daemon=True)
        st.session_state.mqtt_thread.start()

    placeholder = st.empty()

    def color_por_co2(co2):
        if co2 < 800:
            return "🟢 Bueno"
        elif co2 < 1200:
            return "🟠 Moderado"
        else:
            return "🔴 Malo"

    while True:
        with placeholder.container():
            temp = latest_data["temperatura"]
            hum = latest_data["humedad"]
            co2 = latest_data["co2"]

            st.metric("🌡️ Temperatura", f"{temp:.1f} °C")
            st.metric("💧 Humedad", f"{hum:.1f} %")
            st.metric("🌫 CO₂", f"{co2} ppm")

            calidad = color_por_co2(co2)
            st.markdown(f"### Calidad del aire: {calidad}")
            st.progress(min(co2 / 2000, 1.0))

        time.sleep(30)
