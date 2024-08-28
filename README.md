# Tarea 3 - Desarrollo de Proyectos y Producto de Datos

**Alumno: Ricardo Chacón Acosta**

## Descripción del Proyecto

Este proyecto consiste en la implementación de un sistema de predicción utilizando un modelo de Machine Learning. Se estructura en tres componentes principales:

### 1. Backend en FastAPI:
- Implementar un backend utilizando FastAPI para procesar las solicitudes del cliente.
- Preparar el backend para su despliegue en un entorno serverless utilizando Modal.

### 2. Interfaz de Usuario en Streamlit:
- Crear una interfaz gráfica de usuario utilizando Streamlit.
- La interfaz permitirá a los usuarios interactuar fácilmente con la aplicación, enviando datos al backend para obtener predicciones.

### 3. Despliegue Serverless:
- Configurar el proyecto para ser desplegado en Modal como un servicio serverless.

## Comenzando

Antes de empezar a ejecutar este proyecto, hay algunos requisitos previos que debes tener en cuenta:

✅ **Cuenta en Modal:** La aplicación está encapsulada en un contenedor para su despliegue utilizando la plataforma Modal. Visita el sitio web de [Modal](https://modal.com/signup) para registrarte si aún no tienes una cuenta.

✅ **Cuenta de Streamlit (Opcional):** Aunque puedes ejecutar aplicaciones de Streamlit localmente sin una cuenta, tener una cuenta de Streamlit te permite desplegar y compartir tus aplicaciones, lo cual puede ser útil para demostrar tu proyecto a otros. Si deseas utilizar esta función, [regístrate para obtener una cuenta de Streamlit](https://share.streamlit.io/signup).


Adicionalmete debes haber bajado todos los archivos a una carpeta y en el terminal de Anaconda llegar a "este directorio".

```
.
└── producto-datos-lab (este directorio)
    ├── app (acá se encuentran los archivos para implementar el sistema de predicción)
    ├──── backend (Carpeta que contiene archivo Backend)
    ├────── main.py (Backend FastAPI con modelo de predicción serverless.)
    ├──── apply.py (Interfaz Streamlit para predicción de propinas.)
    └──── requirements.txt (dependencias de Python)
```
  
## Pasos previos usando Conda
 
### Prerequisito: Tener [conda](https://docs.conda.io/en/latest/) instalado en tu computador.
 
Vamos a usar Conda para construir un entorno virtual nuevo.
 
### 1. Creando el entorno virtual (Virtual Environment)
 
Asumiremos que tenemos instalado conda. El primer paso es crear un nuevo enviroment para desarrollar. Para crear uno usando Python 3.8 debemos ejecutar el siguiente comando:
 
```bash
conda create --name producto-datos-lab python=3.8
```
 
Luego debemos activarlo usando el comando:
 
```bash
conda activate producto-datos-lab
```
 
Todo el trabajo que realicemos con este código será en este entorno. Así que al trabajar con estos archivos siempre tiene que estar activo el `producto-datos-lab`.
 
### 2. Instalando las dependencias usando PIP 
 
Antes de seguir, verifica que en el terminal de Anaconda estés dentro del directorio `producto-datos-lab`, el cual incluye el archivo `./app/requirements.txt`. Este archivo enlista todas las dependencias necesarias y podemos usarlo para instalarlas todas:
 
```bash
pip install -r ./app/requirements.txt
```
 
Este comando puede demorar un rato dependiendo de la velocidad del computador y la de la conexión a Internet.


### 3. [SERVIDOR] Despliegue en Modal

Comenzando
Lo más agradable de todo esto es que no tienes que configurar ninguna infraestructura. Simplemente:

- Crea una cuenta en modal.com
- Instala el paquete modal-client:

```bash
pip install modal-client
```

- Configura un token usando:

```bash
modal token new
```


Y podrás comenzar a ejecutar trabajos de inmediato.


```
modal deploy ./app/backend/main.py
```
### 4. Actualización de la url del endpoint

Después de desplegar la aplicación en FastAPI en Modal, recibirás una URL única para tu aplicación. Esta URL es el endpoint al que la aplicación de Streamlit enviará las solicitudes.

En el archivo `apply.py`, encontrarás una línea de código que define la URL del endpoint:

```python
endpoint = "https://ricardo-chacon93--prediccion-propinas-app-fastapi-app.modal.run/predict"
```
Debes reemplazar esta URL con la URL que recibiste después de tu despliegue en Modal. Esto asegura que la aplicación de Streamlit se comunique correctamente con tu aplicación FastAPI desplegada.

Finalmente inicia la aplicación Streamlit desde el archivo apply.py

```bash
streamlit run ./app/apply.py
```
El proceso ha concluido. Ahora puedes validar la aplicación en la ventana que se abrirá. La documentación adicional está disponible para que explores el modelo de entrenamiento. En caso de ser necesario, puedes realizar pruebas, reentrenar el modelo y desplegarlo nuevamente.