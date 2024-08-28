# Import the required libraries
import streamlit as st
import json
import requests

# Define the endpoint of the FastAPI application
endpoint = "https://ricardo-chacon93--prediccion-propinas-app-fastapi-app.modal.run/predict"

# Set the title of the Streamlit application
st.title("🚕💰 Predicción de Propinas en Viajes en Taxi")

# Create input fields for the user to input the features of the taxi trip
st.write("Por favor, ingresa las siguientes características de tu viaje en taxi:")

# Agrupación de la información general del viaje
with st.expander("🗓️ Información General del Viaje", expanded=True):
    pickup_weekday = st.selectbox("Día de la semana de recogida", 
                                  options=["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"], 
                                  index=0)
    pickup_hour = st.slider("Hora de recogida", min_value=0, max_value=23, value=12)
    pickup_minute = st.slider("Minuto de recogida", min_value=0, max_value=59, value=30)
    work_hours = st.radio("¿Es durante horas laborales?", options=["No", "Sí"], index=1)

# Información sobre los pasajeros y la duración del viaje
with st.expander("🧑‍🤝‍🧑 Información de Pasajeros y Duración", expanded=True):
    passenger_count = st.slider("Cantidad de pasajeros", min_value=1, max_value=6, value=1)
    trip_distance = st.slider("Distancia del viaje (en millas)", min_value=0.0, max_value=50.0, value=5.0, step=0.1)
    trip_time = st.slider("Tiempo del viaje (en segundos)", min_value=0, max_value=10000, value=600, step=10)
    trip_speed = st.slider("Velocidad promedio del viaje (en millas por segundo)", min_value=0.0, max_value=30.0, value=15.0, step=0.1)

# Información de las ubicaciones y tarifa
with st.expander("📍 Información de Ubicaciones y Tarifa", expanded=True):
    PULocationID = st.number_input("ID de la ubicación de recogida", min_value=1, max_value=263, step=1)
    DOLocationID = st.number_input("ID de la ubicación de destino", min_value=1, max_value=263, step=1)
    RatecodeID = st.selectbox("ID del código de tarifa", options=range(1, 7))

# Preparar los datos de entrada para la solicitud a la API
input_data = {
    "pickup_weekday": ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"].index(pickup_weekday),
    "pickup_hour": pickup_hour,
    "work_hours": 1 if work_hours == "Sí" else 0,
    "pickup_minute": pickup_minute,
    "passenger_count": passenger_count,
    "trip_distance": trip_distance,
    "trip_time": trip_time,
    "trip_speed": trip_speed,
    "PULocationID": PULocationID,
    "DOLocationID": DOLocationID,
    "RatecodeID": RatecodeID
}
print(input_data)
# Si se hace clic en el botón "Predecir", enviar una solicitud a la aplicación FastAPI y mostrar la respuesta
if st.button("Predecir"):
    with st.spinner("Realizando predicción..."):
        res = requests.post(url=endpoint, data=json.dumps(input_data))
    if res.status_code == 200:
        res_json = res.json()
        prediction = res_json.get("prediction", "No se devolvió ninguna predicción")
        st.subheader("Resultado de la Predicción")
        if prediction == 1:
            st.success("El modelo predice que el pasajero **dejará** una propina alta. 💵")
        else:
            st.warning("El modelo predice que el pasajero **no dejará** una propina alta. ❌")
    else:
        st.error("Hubo un error en la solicitud de predicción. Por favor, inténtalo nuevamente.")