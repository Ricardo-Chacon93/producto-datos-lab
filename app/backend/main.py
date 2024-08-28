import modal
import numpy as np
from fastapi import FastAPI, HTTPException
from modal import App, Image, asgi_app, Secret
from pydantic import BaseModel
import joblib  # Necesario para cargar el modelo

# Ruta del modelo
model_path = '/model/random_forest.joblib'

# Configurar la aplicación Modal
web_app = FastAPI(title='Implementando un modelo de Machine Learning usando FastAPI')
app = modal.App("prediccion-propinas-app")

# Definir la imagen para el despliegue, instalando las bibliotecas necesarias
image = modal.Image.debian_slim(python_version="3.8").pip_install(
        "fastapi",
        "pydantic",
        "joblib",
        "scikit-learn==1.3.2",
        "numpy",
        "uvicorn",       # Añadir uvicorn
        "nest_asyncio",  # Añadir nest_asyncio
    ).copy_local_file('/RutaLocal/producto-datos-lab/app/model/random_forest.joblib', model_path)

# Creamos una clase para el vector de features de entrada
class Item(BaseModel):
    pickup_weekday: float
    pickup_hour: float
    work_hours: float
    pickup_minute: float
    passenger_count: float
    trip_distance: float
    trip_time: float
    trip_speed: float
    PULocationID: float
    DOLocationID: float
    RatecodeID: float

# Cargar el modelo globalmente para evitar recargarlo en cada solicitud
rfc = None

def load_model():
    global rfc
    if rfc is None:
        rfc = joblib.load(model_path)  # Cargar el modelo usando joblib

# Función de predicción usando el modelo cargado
def predict_taxi_trip(features_trip, confidence=0.5):
    """Recibe un vector de características de un viaje en taxi en NYC y predice 
       si el pasajero dejará o no una propina alta.
    """
    load_model()  # Asegurar que el modelo está cargado
    pred_value = rfc.predict_proba(features_trip.reshape(1, -1))[0][1]
    return 1 if pred_value >= confidence else 0

# Ruta para el endpoint raíz
@web_app.get("/")
async def home():
    return "¡Felicitaciones! Tu API está funcionando según lo esperado."

# Ruta para predecir la propina basada en los datos recibidos
@web_app.post("/predict")
async def handle_prediction(item: Item, confidence: float = 0.5):
    try:
        features_trip = np.array([
            item.pickup_weekday, item.pickup_hour, item.work_hours, item.pickup_minute, 
            item.passenger_count, item.trip_distance, item.trip_time, item.trip_speed, 
            item.PULocationID, item.DOLocationID, item.RatecodeID
        ])
        prediction = predict_taxi_trip(features_trip, confidence)
        return {"predicted_class": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error haciendo la predicción: {str(e)}")

# Configurar los detalles del despliegue en la plataforma Modal
@app.function(image=image, secrets=[Secret.from_dotenv()])
@asgi_app()
def fastapi_app():
    return web_app

# Desplegar la aplicación si este script se ejecuta directamente
if __name__ == "__main__":
    app.deploy("webapp")